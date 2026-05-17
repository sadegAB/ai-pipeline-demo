#!/usr/bin/env python3
"""
AI Runner Manager v2 — deterministic state machine for a 3‑model coding pipeline.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import textwrap
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests

# ---------------------------------------------------------------------------
# Environment & defaults
# ---------------------------------------------------------------------------
PLANNER_URL = os.getenv("PLANNER_URL", "http://127.0.0.1:8000/v1/chat/completions")
PLANNER_MODEL = os.getenv("PLANNER_MODEL", "planner")

CODER_URL = os.getenv("CODER_URL", "http://127.0.0.1:8001/v1/chat/completions")
CODER_MODEL = os.getenv("CODER_MODEL", "coder")

REVIEWER_URL = os.getenv("REVIEWER_URL", "http://127.0.0.1:8002/v1/chat/completions")
REVIEWER_MODEL = os.getenv("REVIEWER_MODEL", "reviewer")

MAX_RETRIES = 2
REQUEST_TIMEOUT = 600

# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------
def load_text(path: Path, missing_ok: bool = False) -> str:
    """Return content of a file or empty string if missing_ok."""
    if path.exists():
        return path.read_text(encoding="utf-8")
    if missing_ok:
        return ""
    raise FileNotFoundError(f"Required file missing: {path}")

def save_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def extract_json(text: str) -> Optional[Dict[str, Any]]:
    """Robust JSON extraction from model output (handles fences, extra text)."""
    # Try raw first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Strip markdown fences
    fence_pattern = re.compile(r"```(?:json)?\s*\n?(.*?)\n?```", re.DOTALL)
    matches = fence_pattern.findall(text)
    if matches:
        for match in matches:
            try:
                return json.loads(match.strip())
            except json.JSONDecodeError:
                continue

    # Find first JSON object/array
    for pattern in [r'\{.*\}', r'\[.*\]']:
        found = re.search(pattern, text, re.DOTALL)
        if found:
            try:
                return json.loads(found.group(0))
            except json.JSONDecodeError:
                continue
    return None

def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

# ---------------------------------------------------------------------------
# Model client
# ---------------------------------------------------------------------------
class ModelClient:
    def __init__(self, url: str, model: str):
        self.url = url
        self.model = model

    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.1) -> str:
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": False,
        }
        try:
            resp = requests.post(self.url, json=payload, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            raise RuntimeError(f"API call to {self.model} at {self.url} failed: {e}")

    def ready_check(self) -> Tuple[bool, str]:
        """Send a minimal prompt to see if the model responds."""
        try:
            self.chat([{"role": "user", "content": "READY"}], temperature=0.0)
            return True, "PASS"
        except Exception as e:
            return False, f"FAIL: {e}"

# ---------------------------------------------------------------------------
# State management
# ---------------------------------------------------------------------------
STATE_FILE = Path("AI_STATE.json")
PHASES_MD = Path("PHASES.md")
TASK_QUEUE_MD = Path("TASK_QUEUE.md")
RUN_LOG = Path("AI_RUN_LOG.md")
REVIEW_LOG = Path("REVIEW_LOG.md")
TEST_RESULTS = Path("TEST_RESULTS.md")
RAW_PLAN = Path("IMPLEMENTATION_PLAN_RAW.md")

REQUIRED_FILES = ["HANDOFF.md", "AGENT_INSTRUCTIONS.md", "TASK.md"]
OPTIONAL_FILES = [
    "PROJECT_RULES.md",
    "ACCEPTANCE.md",
    "DO_NOT_TOUCH.md",
    "TEST_COMMANDS.md",
]

def load_state() -> Dict[str, Any]:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {
        "phases": [],
        "last_updated": now_iso(),
    }

def save_state(state: Dict[str, Any]) -> None:
    state["last_updated"] = now_iso()
    save_text(STATE_FILE, json.dumps(state, indent=2))

def write_phases_md(state: Dict[str, Any]) -> None:
    lines = ["# Project Phases", ""]
    for phase in state.get("phases", []):
        status = phase["status"].upper()
        lines.append(f"- **{phase['id']}** [{status}] {phase['title']}")
        lines.append(f"  Scope: {phase['scope']}")
    save_text(PHASES_MD, "\n".join(lines) + "\n")

def write_task_queue_md(state: Dict[str, Any]) -> None:
    lines = ["# Task Queue", ""]
    for phase in state.get("phases", []):
        lines.append(f"## {phase['id']}: {phase['title']} [{phase['status']}]")
        if phase.get("tasks_planned") and phase.get("tasks"):
            for task in phase["tasks"]:
                status = task.get("status", "pending")
                file_info = task.get("target_file", "") or "—"
                lines.append(f"- `{task['id']}` [{status}] `{file_info}` — {task['title']}")
        else:
            lines.append("  (no file-level tasks planned yet)")
        lines.append("")
    save_text(TASK_QUEUE_MD, "\n".join(lines) + "\n")

def append_log(file: Path, entry: str) -> None:
    timestamp = now_iso()
    content = f"### {timestamp}\n{entry}\n\n"
    with open(file, "a", encoding="utf-8") as f:
        f.write(content)

def append_review(task_id: str, review: str) -> None:
    append_log(REVIEW_LOG, f"**Task:** {task_id}\n\n{review}")

# ---------------------------------------------------------------------------
# Prompt builders
# ---------------------------------------------------------------------------
def build_global_context() -> str:
    """Gather HANDOFF.md, AGENT_INSTRUCTIONS.md, TASK.md and any optional files."""
    parts = []
    for fname in REQUIRED_FILES:
        path = Path(fname)
        if path.exists():
            parts.append(f"## {fname}\n{load_text(path)}")
    for fname in OPTIONAL_FILES:
        path = Path(fname)
        if path.exists():
            parts.append(f"## {fname}\n{load_text(path)}")
    return "\n\n".join(parts)

def make_planner_system_prompt() -> str:
    return textwrap.dedent("""\
    You are a Planner for a 3-model coding pipeline.
    - NEVER write code.
    - Return STRICT JSON ONLY.
    - Do NOT wrap JSON in markdown fences unless absolutely necessary, but output the JSON first.
    - Keep instructions short and direct.
    - Do NOT repeat the full project description inside JSON.
    - For file-level tasks, prefer exactly one target file per task.
    - Only create test files if the user's TASK.md explicitly asks for tests.
    """)

# ---------------------------------------------------------------------------
# Manager class
# ---------------------------------------------------------------------------


def _extract_rules_from_taskmd() -> str:
    """Extract all rule sections from TASK.md."""
    task_path = Path('TASK.md')
    if not task_path.exists():
        return ''
    lines = task_path.read_text(encoding='utf-8').splitlines()
    rules = []
    collecting = False
    for line in lines:
        if line.startswith('## ') and 'Rules' in line:
            collecting = True
            rules.append(line)
        elif collecting:
            if line.startswith('## ') and 'Rules' not in line:
                collecting = False
            elif line.strip() == '':
                if rules and rules[-1] != '':
                    rules.append('')
            else:
                rules.append(line)
    return '\n'.join(rules).strip()


def _validate_imports(target_file: str, file_content: str) -> list[str]:
    """Check that all imports in a file point to existing modules/classes."""
    import re
    import ast
    errors = []
    try:
        tree = ast.parse(file_content)
    except SyntaxError:
        return ["Syntax error - cannot parse imports"]
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module is None:
                continue
            # Convert relative import to file path
            module_path = node.module
            if node.level > 0:  # relative import
                target_dir = Path(target_file).parent
                for _ in range(node.level - 1):
                    target_dir = target_dir.parent
                parts = module_path.split('.') if module_path else []
                file_path = target_dir / ('/'.join(parts) + '.tsx')
            else:
                parts = module_path.split('.')
                file_path = Path('/'.join(parts) + '.tsx')
            
            if not file_path.exists():
                # Try .tsx for frontend
                tsx_path = file_path.with_suffix('.tsx')
                ts_path = file_path.with_suffix('.ts')
                if not tsx_path.exists() and not ts_path.exists():
                    errors.append(f"Import not found: {node.module} (from {target_file})")
                continue
            
            # Check imported names exist in the module
            if file_path.exists():
                module_content = file_path.read_text(encoding='utf-8')
                for alias in node.names:
                    name = alias.name
                    if name == '*':
                        continue
                    if not re.search(rf'\b(export |def |class ){name}\b', module_content):
                        errors.append(f"'{name}' not exported from {node.module} (imported in {target_file})")
    return errors



def _load_skill(role: str) -> str:
    """Load skill file + QWEN prefix for a model role."""
    skill_path = Path("/root/vllm-test/skills") / f"{role}.md"
    base = "You are Qwen, created by Alibaba Cloud. You are a helpful assistant.\n\n"
    if skill_path.exists():
        return base + skill_path.read_text(encoding="utf-8")
    return base


class AIManager:
    def __init__(self):
        self.planner = ModelClient(PLANNER_URL, PLANNER_MODEL)
        self.coder = ModelClient(CODER_URL, CODER_MODEL)
        self.reviewer = ModelClient(REVIEWER_URL, REVIEWER_MODEL)
        self.global_context = build_global_context()

    # ------------------------------------------------------------------
    # Doctor
    # ------------------------------------------------------------------
    def doctor(self) -> None:
        print("=== AI Runner Manager Doctor ===")
        roles = [
            ("Planner", self.planner),
            ("Coder", self.coder),
            ("Reviewer", self.reviewer),
        ]
        for name, client in roles:
            ok, msg = client.ready_check()
            print(f"{name} ({client.model} @ {client.url}): {msg}")
        print("Doctor check complete.")

    # ------------------------------------------------------------------
    # Clean
    # ------------------------------------------------------------------
    def clean(self) -> None:
        print("Cleaning __pycache__ and *.pyc files...")
        for root, dirs, files in os.walk("."):
            for d in dirs:
                if d == "__pycache__":
                    full = Path(root) / d
                    for f in full.iterdir():
                        f.unlink()
                    full.rmdir()
            for f in files:
                if f.endswith(".pyc"):
                    (Path(root) / f).unlink()
        print("Clean complete.")

    # ------------------------------------------------------------------
    # Init
    # ------------------------------------------------------------------
    def init(self, force: bool = False) -> None:
        if STATE_FILE.exists() and not force:
            print("AI_STATE.json already exists. Use --force to overwrite.")
            return

        # Phase 1: high-level phases
        print("Planning high-level phases...")
        messages = [
            {"role": "system", "content": _load_skill("planner") + "\n\n" + make_planner_system_prompt()},
            {
                "role": "user",
                "content": (
                    "Based on the following project information, create high-level implementation phases.\n\n"
                    f"{self.global_context}\n\n"
                    "Return a JSON object with a 'phases' array. Each phase has 'id', 'title', 'scope'. "
                    "Keep phases broad. Do NOT include file-level tasks.\n\n"
                    'Example:\n{"phases": [{"id": "phase_0", "title": "Database schema", "scope": "Define core models"}]}'
                ),
            },
        ]

        raw = self.planner.chat(messages)
        save_text(RAW_PLAN, f"# Raw Planner Output – High-Level Phases\n\n{raw}\n")
        parsed = extract_json(raw)
        if not parsed or "phases" not in parsed:
            print("ERROR: Planner did not return valid phase JSON. Raw output saved to IMPLEMENTATION_PLAN_RAW.md")
            return

        phases = []
        for idx, phase_data in enumerate(parsed["phases"]):
            phase = {
                "id": phase_data.get("id", f"phase_{idx}"),
                "title": phase_data.get("title", f"Phase {idx}"),
                "scope": phase_data.get("scope", ""),
                "status": "pending",
                "tasks_planned": False,
                "tasks": [],
            }
            phases.append(phase)

        state = {"phases": phases, "last_updated": now_iso()}
        save_state(state)
        write_phases_md(state)
        write_task_queue_md(state)
        print("Initialised with high-level phases. Run 'next' to start planning tasks for phase 0.")

    # ------------------------------------------------------------------
    # Plan tasks for one phase
    # ------------------------------------------------------------------
    def _plan_phase_tasks(self, state: Dict[str, Any], phase_idx: int) -> bool:
        phase = state["phases"][phase_idx]
        if phase["tasks_planned"]:
            return True

        print(f"Planning file-level tasks for {phase['id']}...")
        messages = [
            {"role": "system", "content": _load_skill("planner") + "\n\n" + make_planner_system_prompt()},
            {
                "role": "user",
                "content": (
                    "We are working on this phase ONLY:\n"
                    f"Phase ID: {phase['id']}\nTitle: {phase['title']}\nScope: {phase['scope']}\n\n"
                    f"Full project context:\n{self.global_context}\n\n"
                    "Create file-level implementation tasks for THIS PHASE ONLY. "
                    "Return a JSON object with a 'tasks' array. Each task has: "
                    "'id', 'title', 'type' (code/test/log), 'target_file' (filename, or empty for test/log), "
                    "'instructions' (brief).\n"
                    "Prefer one target file per task. Only use type='test' if the project explicitly asks for tests; "
                    "otherwise use type='code' for implementation.\n\n"
                    "Example:\n"
                    '{"tasks": [{"id": "phase_0_task_0", "title": "Create customer schema", '
                    '"type": "code", "target_file": "schemas/customers.tsx", '
                    '"instructions": "Create CustomerCreate and Customer schemas according to TASK.md."}]}'
                ),
            },
        ]

        raw = self.planner.chat(messages)
        with open(RAW_PLAN, "a", encoding="utf-8") as f:
            f.write(f"\n\n# Raw Planner Output – Tasks for {phase['id']}\n\n{raw}\n")
        parsed = extract_json(raw)
        if not parsed or "tasks" not in parsed:
            print(f"ERROR: Planner did not return valid tasks for {phase['id']}. Raw output appended to IMPLEMENTATION_PLAN_RAW.md")
            return False

        tasks = []
        for idx, t in enumerate(parsed["tasks"]):
            task = {
                "id": t.get("id", f"{phase['id']}_task_{idx}"),
                "title": t.get("title", f"Task {idx}"),
                "type": t.get("type", "code"),
                "target_file": t.get("target_file", ""),
                "instructions": t.get("instructions", ""),
                "status": "pending",
                "attempts": 0,
                "review": "",
                "last_error": "",
            }
            tasks.append(task)

        phase["tasks"] = tasks
        phase["tasks_planned"] = True
        save_state(state)
        write_task_queue_md(state)
        return True

    # ------------------------------------------------------------------
    # Next task processing
    # ------------------------------------------------------------------
    def next(self) -> bool:
        state = load_state()
        if not state["phases"]:
            print("No phases found. Run 'init' first.")
            return False

        # Find first phase not done/failed
        current_phase_idx = None
        for i, phase in enumerate(state["phases"]):
            if phase["status"] in ("pending", "running"):
                current_phase_idx = i
                break
        if current_phase_idx is None:
            # Check if any failed tasks/phases can be retried
            for i, phase in enumerate(state["phases"]):
                if phase["status"] == "failed":
                    print(f"Phase {phase['id']} is failed. Use 'reset-failed' first.")
                    return False
            print("All phases completed.")
            return True

        phase = state["phases"][current_phase_idx]
        if not phase["tasks_planned"]:
            if not self._plan_phase_tasks(state, current_phase_idx):
                return False

        # Mark phase as running
        phase["status"] = "running"
        save_state(state)
        write_phases_md(state)

        # Find first pending task
        task = None
        for t in phase["tasks"]:
            if t["status"] in ("pending", "failed"):  # reset-failed will set to pending
                task = t
                break
        if task is None:
            # All tasks done in this phase
            phase["status"] = "done"
            save_state(state)
            write_phases_md(state)
            write_task_queue_md(state)
            print(f"Phase {phase['id']} completed.")
            return True

        return self._process_task(state, current_phase_idx, task)

    def _process_task(self, state: Dict[str, Any], phase_idx: int, task: Dict[str, Any]) -> bool:
        task["status"] = "running"
        save_state(state)

        try:
            if task["type"] == "code":
                success = self._handle_code_task(state, task)
            elif task["type"] == "test":
                success = self._handle_test_task(state, task)
            elif task["type"] == "log":
                success = self._handle_log_task(state, task)
            else:
                task["status"] = "skipped"
                task["last_error"] = f"Unknown task type: {task['type']}"
                success = False
        except Exception as e:
            task["status"] = "failed"
            task["last_error"] = str(e)
            success = False

        state["phases"][phase_idx] = state["phases"][phase_idx]  # keep updated reference
        save_state(state)
        write_task_queue_md(state)

        if not success:
            print(f"Task {task['id']} failed: {task.get('last_error', 'Unknown error')}")
            return False
        return True

    def _handle_code_task(self, state: Dict[str, Any], task: Dict[str, Any]) -> bool:
        target_file = task["target_file"]
        if not target_file:
            raise ValueError("Code task missing target_file")

        # Build coder prompt
        for attempt in range(1, MAX_RETRIES + 2):  # initial + retries
            task["attempts"] = attempt
            save_state(state)

            print(f"Coder attempt {attempt} for {task['id']} -> {target_file}")

            coder_prompt = self._build_coder_prompt(task, attempt)
            raw_code = self.coder.chat([{"role": "user", "content": coder_prompt}])
            # Strip any accidental markdown fences
            raw_code = self._strip_code_fences(raw_code)

            # Send to reviewer
            review = self._review_file(task, raw_code, target_file)
            task["review"] = review
            append_review(task["id"], review)

            if review.strip().upper().startswith("PASS"):
                # Save file
                file_path = Path(target_file)
                file_path.parent.mkdir(parents=True, exist_ok=True)
                save_text(file_path, raw_code)
                task["status"] = "done"
                append_log(RUN_LOG, f"Task {task['id']} PASS – wrote {target_file}")
                return True
            else:
                # FAIL – feedback will be passed on next attempt
                task["last_error"] = review
                if attempt <= MAX_RETRIES:
                    print(f"Review FAIL, retrying ({attempt}/{MAX_RETRIES})...")
                else:
                    task["status"] = "failed"
                    append_log(RUN_LOG, f"Task {task['id']} FAIL after {attempt} attempts: {review}")
                    return False
        return False

    def _build_coder_prompt(self, task: Dict[str, Any], attempt: int) -> str:
        target_file = task["target_file"]
        instructions = task["instructions"]
        existing_content = ""
        if Path(target_file).exists():
            existing_content = Path(target_file).read_text(encoding="utf-8")

        prompt = (
            f"{_load_skill('coder')}\n\n" + f"{self.global_context}\n\n"
            f"You are the Coder. Write exactly ONE file: {target_file}\n\n"
            f"Instructions:\n{instructions}\n\n"
        )
        if existing_content:
            prompt += f"Current content of {target_file}:\n```\n{existing_content}\n```\n\n"

        if attempt > 1 and task.get("review"):
            prompt += (
                f"PREVIOUS REVIEWER FEEDBACK (you MUST fix these issues):\n"
                f"{task['review']}\n\n"
            )

        # Append mandatory project rules from TASK.md
        rules = _extract_rules_from_taskmd()
        if rules:
            prompt += (
                "MANDATORY PROJECT RULES (follow exactly):\n"
                f"{rules}\n\n"
            )

        prompt += (
            "IMPORTANT: Return ONLY the complete raw file content. "
            "No markdown fences, no explanation, no conversation. Just the code.\n"
        )
        return prompt

    def _strip_code_fences(self, text: str) -> str:
        # Remove leading/trailing ``` fences
        text = text.strip()
        if text.startswith("```"):
            first_newline = text.find("\n")
            if first_newline != -1:
                text = text[first_newline + 1:]
            else:
                text = ""
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()

    def _review_file(self, task: Dict[str, Any], proposed_content: str, target_file: str) -> str:
        # Run global import validation first
        import_errors = _validate_imports(target_file, proposed_content)
        import_feedback = ""
        if import_errors:
            import_feedback = "\n".join(f"- {e}" for e in import_errors)
        
        review_prompt = (
            f"{_load_skill('reviewer')}\n\n" + f"{self.global_context}\n\n"
            f"You are the Reviewer. Check the file `{target_file}` against the requirements.\n\n"
            f"Task instructions:\n{task['instructions']}\n\n"
        )
        if import_feedback:
            review_prompt += (
                f"IMPORT VALIDATION ERRORS (fix these first):\n{import_feedback}\n\n"
            )
        review_prompt += (
            f"Proposed file content:\n```\n{proposed_content}\n```\n\n"
            "Reply with either 'PASS' if everything is correct, or 'FAIL' followed by specific, "
            "actionable feedback on what to fix.\n"
            "Check: imports exist at specified paths, all classes/functions are exported by their modules, "
            "field names match the API response, arrays of objects are never joined directly, "
            "no 'any' types unless absolutely necessary."
        )
        return self.reviewer.chat([{"role": "user", "content": review_prompt}])

    def _handle_test_task(self, state: Dict[str, Any], task: Dict[str, Any]) -> bool:
        test_commands_path = Path("TEST_COMMANDS.md")
        if test_commands_path.exists():
            commands = test_commands_path.read_text(encoding="utf-8").strip().splitlines()
        else:
            commands = ["python3 -m compileall ."]

        outputs = []
        for cmd in commands:
            if not cmd.strip():
                continue
            print(f"Running: {cmd}")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            outputs.append(f"$ {cmd}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}\nreturncode: {result.returncode}")

        output_text = "\n\n".join(outputs)
        save_text(TEST_RESULTS, f"# Test Results for {task['id']}\n\n{output_text}\n")
        task["status"] = "done"
        append_log(RUN_LOG, f"Task {task['id']} tests completed.")
        return True

    def _handle_log_task(self, state: Dict[str, Any], task: Dict[str, Any]) -> bool:
        git_status = subprocess.run(
            ["git", "status", "--short"], capture_output=True, text=True
        ).stdout.strip()
        current_phase = state["phases"][self._current_phase_idx(state)] if state["phases"] else {}
        summary = (
            f"Git status:\n{git_status}\n\n"
            f"Current phase: {current_phase.get('id', 'none')} [{current_phase.get('status', '')}]\n"
            f"Task: {task['id']} - {task['title']}"
        )
        append_log(RUN_LOG, summary)
        task["status"] = "done"
        return True

    def _current_phase_idx(self, state: Dict[str, Any]) -> int:
        for i, phase in enumerate(state["phases"]):
            if phase["status"] in ("pending", "running"):
                return i
        return -1

    # ------------------------------------------------------------------
    # Run loop
    # ------------------------------------------------------------------
    def run(self, max_steps: int = 50) -> None:
        for step in range(1, max_steps + 1):
            print(f"\n--- Step {step}/{max_steps} ---")
            success = self.next()
            if success is False:
                print("Stopping due to failure or no work.")
                return
            if success is True:
                # True means all done or finished current phase; check if any phases remain
                state = load_state()
                if all(p["status"] == "done" for p in state["phases"]):
                    print("All phases completed.")
                    return
        print(f"Reached max steps ({max_steps}).")

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------
    def status(self) -> None:
        state = load_state()
        print(json.dumps(state, indent=2))
        if Path(PHASES_MD).exists():
            print(f"\n{PHASES_MD.name}:")
            print(Path(PHASES_MD).read_text(encoding="utf-8"))

    # ------------------------------------------------------------------
    # Reset failed
    # ------------------------------------------------------------------
    def reset_failed(self) -> None:
        state = load_state()
        for phase in state["phases"]:
            if phase["status"] == "failed":
                phase["status"] = "pending"
            for task in phase.get("tasks", []):
                if task["status"] == "failed":
                    task["status"] = "pending"
                    task["attempts"] = 0
                    task["last_error"] = ""
        save_state(state)
        write_phases_md(state)
        write_task_queue_md(state)
        print("Reset all failed tasks/phases to pending.")

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="AI Runner Manager v2")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init").add_argument("--force", action="store_true")
    sub.add_parser("next")
    run_p = sub.add_parser("run")
    run_p.add_argument("--max-steps", type=int, default=50)
    sub.add_parser("status")
    sub.add_parser("doctor")
    sub.add_parser("clean")
    sub.add_parser("reset-failed")

    args = parser.parse_args()
    manager = AIManager()

    if args.command == "init":
        manager.init(force=args.force)
    elif args.command == "next":
        manager.next()
    elif args.command == "run":
        manager.run(max_steps=args.max_steps)
    elif args.command == "status":
        manager.status()
    elif args.command == "doctor":
        manager.doctor()
    elif args.command == "clean":
        manager.clean()
    elif args.command == "reset-failed":
        manager.reset_failed()

if __name__ == "__main__":
    main()