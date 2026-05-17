import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests


PLANNER_URL = "http://127.0.0.1:8000/v1/chat/completions"
CODER_URL = "http://127.0.0.1:8001/v1/chat/completions"
REVIEWER_URL = "http://127.0.0.1:8002/v1/chat/completions"

PLANNER_MODEL = "planner"
CODER_MODEL = "coder"
REVIEWER_MODEL = "reviewer"

STATE_FILE = Path("AI_STATE.json")
PHASES_FILE = Path("PHASES.md")
TASK_QUEUE_FILE = Path("TASK_QUEUE.md")
RUN_LOG_FILE = Path("AI_RUN_LOG.md")
REVIEW_LOG_FILE = Path("REVIEW_LOG.md")
TEST_RESULTS_FILE = Path("TEST_RESULTS.md")

MAX_RETRIES = 2


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: str, required: bool = True) -> str:
    file_path = Path(path)
    if not file_path.exists():
        if required:
            raise FileNotFoundError(f"Missing required file: {path}")
        return ""
    return file_path.read_text(encoding="utf-8")


def write_text(path: str, content: str) -> None:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content.rstrip() + "\n", encoding="utf-8")


def append_text(path: str, content: str) -> None:
    file_path = Path(path)
    with file_path.open("a", encoding="utf-8") as f:
        f.write(content.rstrip() + "\n")


def clean_model_output(text: str) -> str:
    clean = text.strip()
    if clean.startswith("```"):
        clean = re.sub(r"^```[a-zA-Z0-9_-]*\n", "", clean)
        clean = re.sub(r"\n```$", "", clean)
    return clean.strip()


def ask_model(url: str, model: str, system: str, user: str, max_tokens: int = 4000) -> str:
    response = requests.post(
        url,
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "max_tokens": max_tokens,
            "temperature": 0,
        },
        timeout=240,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]


def extract_json(text: str) -> dict[str, Any]:
    clean = clean_model_output(text)

    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", clean, re.DOTALL)
    if not match:
        raise ValueError(f"Planner did not return JSON:\n{clean}")

    return json.loads(match.group(0))


def load_state() -> dict[str, Any]:
    if not STATE_FILE.exists():
        raise FileNotFoundError("AI_STATE.json does not exist. Run: python3 run_manager.py init")
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def save_state(state: dict[str, Any]) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def get_repo_context() -> dict[str, str]:
    return {
        "handoff": read_text("HANDOFF.md"),
        "agent_instructions": read_text("AGENT_INSTRUCTIONS.md"),
        "task": read_text("TASK.md"),
        "project_rules": read_text("PROJECT_RULES.md", required=False),
        "acceptance": read_text("ACCEPTANCE.md", required=False),
        "do_not_touch": read_text("DO_NOT_TOUCH.md", required=False),
        "test_commands": read_text("TEST_COMMANDS.md", required=False),
    }


def render_context(ctx: dict[str, str]) -> str:
    parts = [
        "# HANDOFF.md",
        ctx["handoff"],
        "# AGENT_INSTRUCTIONS.md",
        ctx["agent_instructions"],
        "# TASK.md",
        ctx["task"],
    ]

    optional_files = [
        ("PROJECT_RULES.md", ctx.get("project_rules", "")),
        ("ACCEPTANCE.md", ctx.get("acceptance", "")),
        ("DO_NOT_TOUCH.md", ctx.get("do_not_touch", "")),
        ("TEST_COMMANDS.md", ctx.get("test_commands", "")),
    ]

    for name, content in optional_files:
        if content.strip():
            parts.extend([f"# {name}", content])

    return "\n\n".join(parts)


def normalize_state(raw_state: dict[str, Any]) -> dict[str, Any]:
    phases = raw_state.get("phases")
    if not isinstance(phases, list) or not phases:
        raise ValueError("Planner JSON must include a non-empty phases list.")

    for p_index, phase in enumerate(phases):
        phase.setdefault("id", f"phase_{p_index}")
        phase.setdefault("title", f"Phase {p_index}")
        phase.setdefault("description", "")
        phase.setdefault("status", "pending")

        tasks = phase.get("tasks")
        if not isinstance(tasks, list) or not tasks:
            raise ValueError(f"{phase['id']} must include a non-empty tasks list.")

        for t_index, task in enumerate(tasks):
            task.setdefault("id", f"task_{t_index}")
            task.setdefault("title", f"Task {t_index}")
            task.setdefault("type", "code")
            task.setdefault("target_file", "")
            task.setdefault("instructions", task.get("title", ""))
            task.setdefault("status", "pending")
            task.setdefault("attempts", 0)
            task.setdefault("review", "")
            task.setdefault("last_error", "")

    return {
        "status": "running",
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "current_phase_index": 0,
        "current_task_index": 0,
        "phases": phases,
    }


def write_phase_files(state: dict[str, Any]) -> None:
    phases_lines = ["# PHASES", ""]
    queue_lines = ["# TASK QUEUE", ""]

    for phase in state["phases"]:
        phases_lines.append(f"## {phase['id']}: {phase['title']}")
        phases_lines.append(f"- Status: {phase['status']}")
        if phase.get("description"):
            phases_lines.append(f"- Description: {phase['description']}")
        phases_lines.append("")

        queue_lines.append(f"## {phase['id']}: {phase['title']}")
        queue_lines.append("")

        for task in phase["tasks"]:
            queue_lines.append(f"### {task['id']}: {task['title']}")
            queue_lines.append(f"- Status: {task['status']}")
            queue_lines.append(f"- Type: {task.get('type', 'code')}")
            queue_lines.append(f"- Target file: {task.get('target_file', '')}")
            queue_lines.append(f"- Attempts: {task.get('attempts', 0)}")
            queue_lines.append("")
            queue_lines.append("Instructions:")
            queue_lines.append(task.get("instructions", "").strip())
            queue_lines.append("")

    write_text(str(PHASES_FILE), "\n".join(phases_lines))
    write_text(str(TASK_QUEUE_FILE), "\n".join(queue_lines))


def init_manager(force: bool = False) -> None:
    if STATE_FILE.exists() and not force:
        print("AI_STATE.json already exists.")
        print("Use: python3 run_manager.py init --force")
        return

    ctx = get_repo_context()
    full_context = render_context(ctx)

    system = (
        "You are the Planner model in a manager-driven AI coding pipeline. "
        "You do not write code. You only break the project task into phases and file-level tasks. "
        "Return strict JSON only. No markdown. No explanation."
    )

    user = f"""
Read the repository protocol files and task below.

{full_context}

Create an execution state for the Manager.

Rules:
- A phase is a feature or major implementation unit.
- A task is a small action, usually one file create/edit.
- For this FastAPI template, tasks should usually be:
  1. create schemas/<feature>.py
  2. create routers/<feature>.py
  3. edit main.py to register router
  4. run tests / compile check
  5. write logs / summary
- Planner must not write code.
- Coder will receive one task at a time.
- Reviewer will review one task at a time.

Return strict JSON with this exact shape:

{{
  "phases": [
    {{
      "id": "phase_0",
      "title": "Short phase title",
      "description": "What this phase achieves",
      "status": "pending",
      "tasks": [
        {{
          "id": "task_0",
          "title": "Short task title",
          "type": "code",
          "target_file": "path/to/file.py",
          "instructions": "Detailed instructions for the Coder for this one task only.",
          "status": "pending",
          "attempts": 0
        }}
      ]
    }}
  ]
}}

Task types allowed:
- code
- test
- log
"""

    print("=== PLANNER: Creating phases and task queue ===")
    response = ask_model(PLANNER_URL, PLANNER_MODEL, system, user, max_tokens=5000)

    write_text("IMPLEMENTATION_PLAN_RAW.md", response)

    raw_state = extract_json(response)
    state = normalize_state(raw_state)
    save_state(state)
    write_phase_files(state)

    append_text(str(RUN_LOG_FILE), f"# AI Run Log\n\n## Init {now_iso()}\n\nManager initialized.\n")
    print("✅ Created AI_STATE.json")
    print("✅ Created PHASES.md")
    print("✅ Created TASK_QUEUE.md")
    print("✅ Created IMPLEMENTATION_PLAN_RAW.md")
    print_status()


def current_phase_and_task(state: dict[str, Any]) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    phases = state["phases"]

    for p_index, phase in enumerate(phases):
        if phase["status"] == "done":
            continue

        state["current_phase_index"] = p_index

        for t_index, task in enumerate(phase["tasks"]):
            if task["status"] not in ("done", "skipped"):
                state["current_task_index"] = t_index
                return phase, task

        phase["status"] = "done"
        state["updated_at"] = now_iso()
        save_state(state)

    return None, None


def get_file_snapshot(path: str) -> str:
    if not path:
        return ""
    file_path = Path(path)
    if not file_path.exists():
        return ""
    return file_path.read_text(encoding="utf-8")


def run_shell_command(cmd: list[str]) -> tuple[int, str]:
    process = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return process.returncode, process.stdout


def run_tests_for_task(task: dict[str, Any]) -> bool:
    test_commands = read_text("TEST_COMMANDS.md", required=False).strip()

    if test_commands:
        commands = [
            line.strip()
            for line in test_commands.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
    else:
        commands = ["python3 -m compileall ."]

    outputs = []
    success = True

    for command in commands:
        outputs.append(f"$ {command}")
        result = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        outputs.append(f"Exit code: {result.returncode}")
        outputs.append(result.stdout)

        if result.returncode != 0:
            success = False

    write_text(str(TEST_RESULTS_FILE), "\n".join(outputs))
    task["status"] = "done" if success else "failed"
    task["last_error"] = "" if success else "Tests failed. See TEST_RESULTS.md."
    return success


def write_log_task(state: dict[str, Any], phase: dict[str, Any], task: dict[str, Any]) -> None:
    changed_files = []

    code, output = run_shell_command(["git", "status", "--short"])
    if output.strip():
        changed_files = output.strip().splitlines()

    log = [
        f"## Log Task {now_iso()}",
        "",
        f"Phase: {phase['id']} - {phase['title']}",
        f"Task: {task['id']} - {task['title']}",
        "",
        "Changed files:",
    ]

    if changed_files:
        log.extend([f"- {line}" for line in changed_files])
    else:
        log.append("- No changed files detected.")

    append_text(str(RUN_LOG_FILE), "\n".join(log))
    task["status"] = "done"


def run_code_task(ctx: dict[str, str], phase: dict[str, Any], task: dict[str, Any]) -> bool:
    target_file = task.get("target_file", "").strip()
    if not target_file:
        task["status"] = "failed"
        task["last_error"] = "Code task has no target_file."
        return False

    full_context = render_context(ctx)
    current_file = get_file_snapshot(target_file)

    for attempt in range(1, MAX_RETRIES + 2):
        task["attempts"] = attempt
        task["status"] = "running"

        coder_system = (
            "You are the Coder model in a manager-driven AI coding pipeline. "
            "You write or edit exactly one target file. "
            "Return ONLY the complete raw file content. "
            "No markdown. No explanation. No code fences."
        )

        coder_user = f"""
Repository context:

{full_context}

Current phase:
{phase["id"]}: {phase["title"]}
{phase.get("description", "")}

Current task:
{task["id"]}: {task["title"]}

Task instructions:
{task["instructions"]}

Target file:
{target_file}

Current target file content, if it exists:
{current_file}

Rules:
- Work only on the target file.
- Return the complete final content for the target file.
- Do not return patches.
- Do not return markdown.
- Do not explain.
"""

        print(f"=== CODER: {phase['id']} / {task['id']} -> {target_file} ===")
        code = ask_model(CODER_URL, CODER_MODEL, coder_system, coder_user, max_tokens=5000)
        code = clean_model_output(code)

        reviewer_system = (
            "You are the Reviewer model in a manager-driven AI coding pipeline. "
            "You are strict. Reply PASS if the code fully satisfies the task and repo rules. "
            "Reply FAIL if anything is wrong, then list exact fixes. "
            "Do not rewrite the whole file unless necessary."
        )

        reviewer_user = f"""
Repository context:

{full_context}

Current phase:
{phase["id"]}: {phase["title"]}

Current task:
{task["id"]}: {task["title"]}

Task instructions:
{task["instructions"]}

Target file:
{target_file}

Proposed file content:
{code}

Review requirements:
- Check against HANDOFF.md.
- Check against AGENT_INSTRUCTIONS.md.
- Check against TASK.md.
- Check that only this target file content is being produced.
- Check imports.
- Check missing required fields/endpoints.
- Check that the code does not switch frameworks.
- Reply PASS or FAIL.
"""

        print(f"=== REVIEWER: attempt {attempt} ===")
        review = ask_model(REVIEWER_URL, REVIEWER_MODEL, reviewer_system, reviewer_user, max_tokens=1500)
        task["review"] = review

        append_text(
            str(REVIEW_LOG_FILE),
            f"## {now_iso()} - {phase['id']} / {task['id']} / attempt {attempt}\n\n"
            f"Target file: {target_file}\n\n"
            f"Review:\n{review}\n",
        )

        print(review[:700])

        review_upper = review.upper()
        passed = "PASS" in review_upper and "FAIL" not in review_upper

        if passed:
            write_text(target_file, code)
            task["status"] = "done"
            task["last_error"] = ""
            append_text(
                str(RUN_LOG_FILE),
                f"## {now_iso()}\n\nCompleted {phase['id']} / {task['id']} -> {target_file}\n",
            )
            print(f"✅ Saved {target_file}")
            return True

        task["last_error"] = review

        if attempt <= MAX_RETRIES:
            print("❌ Review failed. Retrying with reviewer feedback.")
            current_file = code
        else:
            task["status"] = "failed"
            print("❌ Max retries reached.")
            return False

    return False


def mark_phase_statuses(state: dict[str, Any]) -> None:
    for phase in state["phases"]:
        tasks = phase["tasks"]
        if any(task["status"] == "failed" for task in tasks):
            phase["status"] = "failed"
        elif all(task["status"] in ("done", "skipped") for task in tasks):
            phase["status"] = "done"
        elif any(task["status"] in ("running", "done") for task in tasks):
            phase["status"] = "running"
        else:
            phase["status"] = "pending"


def run_next() -> None:
    state = load_state()
    ctx = get_repo_context()

    phase, task = current_phase_and_task(state)
    if phase is None or task is None:
        state["status"] = "done"
        state["updated_at"] = now_iso()
        save_state(state)
        write_phase_files(state)
        print("✅ All phases and tasks are done.")
        return

    print(f"Current phase: {phase['id']} - {phase['title']}")
    print(f"Current task: {task['id']} - {task['title']}")

    task_type = task.get("type", "code")

    if task_type == "test":
        success = run_tests_for_task(task)
    elif task_type == "log":
        write_log_task(state, phase, task)
        success = True
    else:
        success = run_code_task(ctx, phase, task)

    mark_phase_statuses(state)

    if success:
        print("✅ Task completed.")
    else:
        print("❌ Task failed.")

    state["updated_at"] = now_iso()
    save_state(state)
    write_phase_files(state)
    print_status()


def print_status() -> None:
    if not STATE_FILE.exists():
        print("No AI_STATE.json found.")
        print("Run: python3 run_manager.py init")
        return

    state = load_state()
    phases = state["phases"]

    total_tasks = 0
    done_tasks = 0

    print("\n=== STATUS ===")
    print(f"Pipeline status: {state.get('status')}")
    print(f"Updated at: {state.get('updated_at')}")

    for phase in phases:
        tasks = phase["tasks"]
        total_tasks += len(tasks)
        done_tasks += sum(1 for task in tasks if task["status"] == "done")

        print(f"\n{phase['id']} - {phase['title']}")
        print(f"Status: {phase['status']}")

        for task in tasks:
            marker = "✅" if task["status"] == "done" else "❌" if task["status"] == "failed" else "⏳"
            print(
                f"  {marker} {task['id']} - {task['title']} "
                f"[{task['status']}] attempts={task.get('attempts', 0)} target={task.get('target_file', '')}"
            )

    print(f"\nProgress: {done_tasks}/{total_tasks} tasks done")



def run_all(max_steps: int = 50) -> None:
    """
    Auto-run tasks until completion, failure, or safety limit.
    """
    steps = 0

    while steps < max_steps:
        steps += 1

        state = load_state()

        if state.get("status") == "done":
            print("✅ Pipeline already done.")
            print_status()
            return

        phase, task = current_phase_and_task(state)

        if phase is None or task is None:
            state["status"] = "done"
            state["updated_at"] = now_iso()
            save_state(state)
            write_phase_files(state)
            print("✅ All phases and tasks are done.")
            print_status()
            return

        if task.get("status") == "failed" or phase.get("status") == "failed":
            print("❌ Pipeline stopped because a phase/task failed.")
            print_status()
            return

        print(f"\n=== AUTO STEP {steps}/{max_steps} ===")
        print(f"Phase: {phase['id']} - {phase['title']}")
        print(f"Task: {task['id']} - {task['title']}")

        run_next()

        updated = load_state()

        failed = any(
            t.get("status") == "failed"
            for ph in updated["phases"]
            for t in ph["tasks"]
        )

        if failed:
            print("❌ Auto-run stopped after failure.")
            print_status()
            return

        all_done = all(
            ph.get("status") == "done"
            for ph in updated["phases"]
        )

        if all_done:
            updated["status"] = "done"
            updated["updated_at"] = now_iso()
            save_state(updated)
            write_phase_files(updated)
            print("✅ Auto-run completed all phases.")
            print_status()
            return

    print(f"⚠️ Auto-run stopped after max_steps={max_steps}.")
    print_status()


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 run_manager.py init")
        print("  python3 run_manager.py init --force")
        print("  python3 run_manager.py next")
        print("  python3 run_manager.py run")
        print("  python3 run_manager.py status")
        sys.exit(1)

    command = sys.argv[1]

    if command == "init":
        init_manager(force="--force" in sys.argv)
    elif command == "next":
        run_next()
    elif command == "run":
        max_steps = 50
        if "--max-steps" in sys.argv:
            i = sys.argv.index("--max-steps")
            max_steps = int(sys.argv[i + 1])
        run_all(max_steps=max_steps)
    elif command == "status":
        print_status()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
