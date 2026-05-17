#!/usr/bin/env python3
"""
AI Frontend Manager — 3‑model pipeline for React + Vite + TypeScript projects.
Adapted from run_manager.py for frontend conventions.
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
# Config
# ---------------------------------------------------------------------------
PLANNER_URL = os.getenv("PLANNER_URL", "http://127.0.0.1:8001/v1/chat/completions")
CODER_URL = os.getenv("CODER_URL", "http://127.0.0.1:8002/v1/chat/completions")
REVIEWER_URL = os.getenv("REVIEWER_URL", "http://127.0.0.1:8003/v1/chat/completions")
PLANNER_MODEL = os.getenv("PLANNER_MODEL", "planner")
CODER_MODEL = os.getenv("CODER_MODEL", "coder")
REVIEWER_MODEL = os.getenv("REVIEWER_MODEL", "reviewer")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "300"))

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def load_text(path: Path, missing_ok: bool = False) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    if missing_ok:
        return ""
    raise FileNotFoundError(f"Required file not found: {path}")

def save_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")

def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def extract_json(text: str) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    fence_pattern = re.compile(r"```(?:json)?\s*\n?(.*?)\n?```", re.DOTALL)
    matches = fence_pattern.findall(text)
    if matches:
        for match in matches:
            try:
                return json.loads(match.strip())
            except json.JSONDecodeError:
                continue
    for pattern in [r'\{.*\}', r'\[.*\]']:
        found = re.search(pattern, text, re.DOTALL)
        if found:
            try:
                return json.loads(found.group(0))
            except json.JSONDecodeError:
                continue
    return None

def append_log(path: Path, line: str) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"[{now_iso()}] {line}\n")

# ---------------------------------------------------------------------------
# Model client
# ---------------------------------------------------------------------------
class ModelClient:
    def __init__(self, url: str, model: str):
        self.url = url
        self.model = model

    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.2) -> str:
        payload = {"model": self.model, "messages": messages, "temperature": temperature, "stream": False}
        try:
            resp = requests.post(self.url, json=payload, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            raise RuntimeError(f"API call to {self.model} at {self.url} failed: {e}")

    def ready_check(self) -> Tuple[bool, str]:
        try:
            self.chat([{"role": "user", "content": "READY"}], temperature=0.0)
            return True, "PASS"
        except Exception as e:
            return False, f"FAIL: {e}"

# ---------------------------------------------------------------------------
# State files (written inside whichever directory the manager runs from)
# ---------------------------------------------------------------------------
STATE_FILE = Path("AI_STATE.json")
PHASES_MD = Path("PHASES.md")
TASK_QUEUE_MD = Path("TASK_QUEUE.md")
RUN_LOG = Path("AI_RUN_LOG.md")
REVIEW_LOG = Path("REVIEW_LOG.md")
TEST_RESULTS = Path("TEST_RESULTS.md")
RAW_PLAN = Path("IMPLEMENTATION_PLAN_RAW.md")

REQUIRED_FILES = ["HANDOFF.md", "AGENT_INSTRUCTIONS.md", "TASK.md"]
OPTIONAL_FILES = ["PROJECT_RULES.md", "DO_NOT_TOUCH.md"]

def load_state() -> Dict[str, Any]:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {"phases": [], "last_updated": now_iso()}

def save_state(state: Dict[str, Any]) -> None:
    state["last_updated"] = now_iso()
    save_text(STATE_FILE, json.dumps(state, indent=2))

def build_global_context() -> str:
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
    You are a Planner for a 3-model frontend coding pipeline (React + Vite + TypeScript + TailwindCSS).
    - NEVER write code.
    - Return STRICT JSON ONLY.
    - Do NOT wrap JSON in markdown fences unless absolutely necessary, but output the JSON first.
    - Keep instructions short and direct.
    - Do NOT repeat the full project description inside JSON.
    - For file-level tasks, prefer exactly one target file per task.
    """)

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

def write_phases_md(state: Dict[str, Any]) -> None:
    lines = ["# Project Phases\n"]
    for p in state["phases"]:
        status = p["status"].upper()
        lines.append(f"- **{p['id']}** [{status}] {p['title']}")
        lines.append(f"  Scope: {p['scope']}")
    save_text(PHASES_MD, "\n".join(lines))

def write_task_queue_md(state: Dict[str, Any]) -> None:
    lines = ["# Task Queue\n"]
    for p in state["phases"]:
        status = p["status"]
        lines.append(f"## {p['id']}: {p['title']} [{status}]")
        if p.get("tasks"):
            for t in p["tasks"]:
                t_status = t["status"]
                target = t.get("target_file", "(none)")
                lines.append(f"- `{t['id']}` [{t_status}] `{target}` — {t['title']}")
        else:
            lines.append("  (no file-level tasks planned yet)")
        lines.append("")
    save_text(TASK_QUEUE_MD, "\n".join(lines))

# ---------------------------------------------------------------------------
# AIManager
# ---------------------------------------------------------------------------
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
        print("=== AI Frontend Manager Doctor ===")
        roles = [("Planner", self.planner), ("Coder", self.coder), ("Reviewer", self.reviewer)]
        for name, client in roles:
            ok, msg = client.ready_check()
            print(f"{name} ({client.model} @ {client.url}): {msg}")
        # Also check npm/node
        try:
            node_v = subprocess.run(["node", "--version"], capture_output=True, text=True)
            print(f"Node.js: {node_v.stdout.strip()}")
        except Exception:
            print("Node.js: NOT FOUND")
        try:
            npm_v = subprocess.run(["npm", "--version"], capture_output=True, text=True)
            print(f"npm: {npm_v.stdout.strip()}")
        except Exception:
            print("npm: NOT FOUND")
        print("Doctor check complete.")

    # ------------------------------------------------------------------
    # Clean
    # ------------------------------------------------------------------
    def clean(self) -> None:
        print("Cleaning __pycache__ and *.pyc files...")
        for root, dirs, files in os.walk("."):
            if "__pycache__" in dirs:
                for f in (Path(root) / "__pycache__").glob("*.pyc"):
                    f.unlink()
        print("Clean complete.")

    # ------------------------------------------------------------------
    # Init
    # ------------------------------------------------------------------
    def init(self, force: bool = False) -> None:
        state = load_state()
        if state["phases"] and not force:
            print("Already initialised. Use --force to re-initialise.")
            return
        print("Planning high-level phases...")
        messages = [
            {"role": "system", "content": make_planner_system_prompt()},
            {"role": "user", "content": (
                f"Full project context:\n{self.global_context}\n\n"
                "Create high-level implementation phases for this project. "
                "Return a JSON object with a 'phases' array. Each phase has: "
                "'id' (e.g. phase_0), 'title', 'scope' (brief).\n"
                "Do NOT create setup/configuration phases. Every phase must produce application code.\n"
                "Example: {\"phases\": [{\"id\": \"phase_0\", \"title\": \"Types\", \"scope\": \"Define TypeScript interfaces\"}]}"
            )},
        ]
        raw = self.planner.chat(messages)
        with open(RAW_PLAN, "w", encoding="utf-8") as f:
            f.write(f"# Raw Planner Output – Phases\n\n{raw}\n")
        parsed = extract_json(raw)
        if not parsed or "phases" not in parsed:
            print("ERROR: Planner did not return valid phase JSON. Raw output saved to IMPLEMENTATION_PLAN_RAW.md")
            return
        state["phases"] = [{"id": p["id"], "title": p["title"], "scope": p["scope"], "status": "pending", "tasks_planned": False, "tasks": []} for p in parsed["phases"]]
        save_state(state)
        write_phases_md(state)
        write_task_queue_md(state)
        print("Initialised with high-level phases. Run 'next' to start planning tasks for phase 0.")

    # ------------------------------------------------------------------
    # Next step
    # ------------------------------------------------------------------
    def next(self) -> None:
        state = load_state()
        for idx, phase in enumerate(state["phases"]):
            if phase["status"] in ("pending", "running"):
                if phase["status"] == "pending":
                    phase["status"] = "running"
                    save_state(state)
                if not phase["tasks_planned"]:
                    if not self._plan_phase_tasks(state, idx):
                        return
                    save_state(state)
                    write_task_queue_md(state)
                # Find next pending task
                for task in phase["tasks"]:
                    if task["status"] == "pending":
                        if task["type"] == "code":
                            self._handle_code_task(state, task)
                        elif task["type"] == "test":
                            self._handle_test_task(state, task)
                        elif task["type"] == "log":
                            self._handle_log_task(state, task)
                        save_state(state)
                        write_task_queue_md(state)
                        write_phases_md(state)
                        return
                # All tasks done
                phase["status"] = "done"
                save_state(state)
                write_phases_md(state)
                write_task_queue_md(state)
                print(f"Phase {phase['id']} completed.")
                return
        print("All phases completed.")

    # ------------------------------------------------------------------
    # Run loop
    # ------------------------------------------------------------------
    def run(self, max_steps: int = 50) -> None:
        for step in range(1, max_steps + 1):
            print(f"\n--- Step {step}/{max_steps} ---")
            state = load_state()
            all_done = all(p["status"] == "done" for p in state["phases"])
            if all_done:
                print("All phases completed.")
                return
            self.next()
        print(f"Reached max steps ({max_steps}).")

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------
    def status(self) -> None:
        state = load_state()
        print(json.dumps(state, indent=2))
        if PHASES_MD.exists():
            print("\nPHASES.md:")
            print(PHASES_MD.read_text())

    # ------------------------------------------------------------------
    # Reset failed
    # ------------------------------------------------------------------
    def reset_failed(self) -> None:
        state = load_state()
        for p in state["phases"]:
            for t in p.get("tasks", []):
                if t["status"] == "failed":
                    t["status"] = "pending"
                    t["attempts"] = 0
                    t["review"] = ""
                    t["last_error"] = ""
        save_state(state)
        write_phases_md(state)
        write_task_queue_md(state)
        print("Reset all failed tasks/phases to pending.")

    # ------------------------------------------------------------------
    # Plan phase tasks
    # ------------------------------------------------------------------
    def _plan_phase_tasks(self, state: Dict[str, Any], phase_idx: int) -> bool:
        phase = state["phases"][phase_idx]
        if phase["tasks_planned"]:
            return True
        print(f"Planning file-level tasks for {phase['id']}...")
        messages = [
            {"role": "system", "content": make_planner_system_prompt()},
            {"role": "user", "content": (
                "We are working on this phase ONLY:\n"
                f"Phase ID: {phase['id']}\nTitle: {phase['title']}\nScope: {phase['scope']}\n\n"
                f"Full project context:\n{self.global_context}\n\n"
                "Create file-level implementation tasks for THIS PHASE ONLY. "
                "Return a JSON object with a 'tasks' array. Each task has: "
                "'id', 'title', 'type' (code/test/log), 'target_file' (relative path from project root), "
                "'instructions' (brief).\n"
                "Prefer one target file per task.\n\n"
                "Example:\n"
                '{"tasks": [{"id": "phase_0_task_0", "title": "Create hospital types", '
                '"type": "code", "target_file": "src/types/hospital.ts", '
                '"instructions": "Define Hospital, HospitalCreate interfaces according to TASK.md."}]}'
            )},
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
        return True

    # ------------------------------------------------------------------
    # Handle code task
    # ------------------------------------------------------------------
    def _handle_code_task(self, state: Dict[str, Any], task: Dict[str, Any]) -> None:
        target_file = task["target_file"]
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            task["attempts"] = attempt
            print(f"Coder attempt {attempt} for {task['id']} -> {target_file}")
            prompt = self._build_coder_prompt(task, attempt)
            raw_code = self.coder.chat([{"role": "user", "content": prompt}])
            code = self._strip_code_fences(raw_code)
            # Ensure directory exists
            Path(target_file).parent.mkdir(parents=True, exist_ok=True)
            # Write proposed content
            save_text(Path(target_file), code)
            # Review
            review = self._review_file(task, code, target_file)
            task["review"] = review
            append_log(REVIEW_LOG, f"Task {task['id']} attempt {attempt}: {review[:200]}")
            if review.strip().upper().startswith("PASS"):
                task["status"] = "done"
                task["last_error"] = ""
                print(f"Review PASS for {target_file}")
                return
            else:
                task["last_error"] = review
                print(f"Review FAIL, retrying ({attempt}/{max_retries})...")
        task["status"] = "failed"
        print(f"Task {task['id']} failed after {max_retries} attempts.")

    # ------------------------------------------------------------------
    # Build coder prompt
    # ------------------------------------------------------------------
    def _build_coder_prompt(self, task: Dict[str, Any], attempt: int) -> str:
        target_file = task["target_file"]
        instructions = task["instructions"]
        existing_content = ""
        if Path(target_file).exists():
            existing_content = Path(target_file).read_text(encoding="utf-8")

        prompt = (
            f"{self.global_context}\n\n"
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

    # ------------------------------------------------------------------
    # Strip code fences
    # ------------------------------------------------------------------
    def _strip_code_fences(self, text: str) -> str:
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

    # ------------------------------------------------------------------
    # Review file
    # ------------------------------------------------------------------
    def _review_file(self, task: Dict[str, Any], proposed_content: str, target_file: str) -> str:
        review_prompt = (
            f"{self.global_context}\n\n"
            f"You are the Reviewer. Check the file `{target_file}` against the requirements.\n\n"
            f"Task instructions:\n{task['instructions']}\n\n"
            f"Proposed file content:\n```\n{proposed_content}\n```\n\n"
            "Reply with either 'PASS' if everything is correct, or 'FAIL' followed by specific, "
            "actionable feedback on what to fix.\n"
            "Check: imports are correct, types match TASK.md, uses useApi() for data fetching, "
            "uses Tailwind classes only, no 'any' types, follows the template conventions."
        )
        return self.reviewer.chat([{"role": "user", "content": review_prompt}])

    # ------------------------------------------------------------------
    # Handle test task
    # ------------------------------------------------------------------
    def _handle_test_task(self, state: Dict[str, Any], task: Dict[str, Any]) -> None:
        commands = ["npx tsc --noEmit"]
        outputs = []
        for cmd in commands:
            if not cmd.strip():
                continue
            print(f"Running: {cmd}")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
            outputs.append(f"$ {cmd}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}\nreturncode: {result.returncode}")
        output_text = "\n\n".join(outputs)
        save_text(TEST_RESULTS, f"# Test Results for {task['id']}\n\n{output_text}\n")
        task["status"] = "done"
        append_log(RUN_LOG, f"Task {task['id']} tests completed.")

    # ------------------------------------------------------------------
    # Handle log task
    # ------------------------------------------------------------------
    def _handle_log_task(self, state: Dict[str, Any], task: Dict[str, Any]) -> None:
        git_status = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
        save_text(TEST_RESULTS, f"# Log for {task['id']}\n\n## Git Status\n```\n{git_status.stdout}\n```\n")
        task["status"] = "done"
        append_log(RUN_LOG, f"Task {task['id']} completed.")

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="AI Frontend Manager")
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
