#!/usr/bin/env python3
import os
import sys
import glob
from datetime import datetime
from typing import List, Optional

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def print_banner() -> None:
    print("=== Experimentation Runner ===")


def ensure_dirs() -> None:
    for rel in ("output", "templates", "input"):
        os.makedirs(os.path.join(os.path.dirname(__file__), rel), exist_ok=True)


def list_netlogo_cases() -> List[str]:
    """List available NetLogo cases from code-netlogo-to-messir/input-netlogo/"""
    netlogo_dir = os.path.join(REPO_ROOT, "code-netlogo-to-messir", "input-netlogo")
    if not os.path.exists(netlogo_dir):
        return []
    pattern = os.path.join(netlogo_dir, "*-netlogo-code.md")
    files = glob.glob(pattern)
    cases = []
    for f in files:
        basename = os.path.basename(f)
        case_name = basename.replace("-netlogo-code.md", "")
        cases.append(case_name)
    return sorted(cases)


def choose_cases() -> List[str]:
    """Interactive case selection"""
    cases = list_netlogo_cases()
    if not cases:
        print("No NetLogo cases found in code-netlogo-to-messir/input-netlogo/")
        return []
    
    print("Available NetLogo cases:")
    for i, case in enumerate(cases, 1):
        print(f"  {i}) {case}")
    print(f"  {len(cases) + 1}) All cases")
    
    choice = input(f"Select case(s) [1-{len(cases) + 1}]: ").strip()
    if not choice:
        return [cases[0]]  # Default to first case
    
    try:
        idx = int(choice)
        if idx == len(cases) + 1:
            return cases
        elif 1 <= idx <= len(cases):
            return [cases[idx - 1]]
    except ValueError:
        pass
    
    return [cases[0]]  # Fallback to first case


def choose_mode() -> str:
    print("Select pipeline mode:")
    print("  1) With orchestration")
    print("  2) Without orchestration")
    print("  3) Both")
    choice = input("Enter choice [1-3]: ").strip() or "1"
    return {"1": "with", "2": "without", "3": "both"}.get(choice, "with")


def choose_persona() -> str:
    return input("Persona set [persona-v1]: ").strip() or "persona-v1"


def choose_label() -> str:
    return input("Optional label (e.g., quick-test) [blank for none]: ").strip()


def compute_execution_id(persona: str, mode: str, label: str) -> str:
    now = datetime.now()
    date_part = now.strftime("%Y-%m-%d")
    time_part = now.strftime("%H%M")
    base = f"{time_part}-{persona}-{mode}"
    if label:
        base += f"-{label}"
    return os.path.join(date_part, base)


def _import_module(module_path: str, module_name: str):
    """Helper function to import modules dynamically"""
    import importlib.util
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sync_inputs(persona: str) -> None:
    """Sync required inputs from code-netlogo-to-messir/"""
    module_path = os.path.join(os.path.dirname(__file__), "utils_io.py")
    input_sync_module = _import_module(module_path, "input_sync")
    
    dest_root = os.path.dirname(__file__)
    input_sync_module.sync_inputs(REPO_ROOT, dest_root, persona)
    print(f"Synced inputs for persona: {persona}")


def run_pipeline(mode: str, persona: str, cases: List[str], execution_id: str) -> dict:
    """Run selected pipeline(s) and return results"""
    # Import orchestrated runner
    orchestrated_path = os.path.join(os.path.dirname(__file__), "runner_orchestrated.py")
    orchestrated_module = _import_module(orchestrated_path, "orchestrated")
    
    # Import single agent runner
    single_agent_path = os.path.join(os.path.dirname(__file__), "runner_single_agent.py")
    single_agent_module = _import_module(single_agent_path, "single_agent")
    
    output_dir = os.path.join(os.path.dirname(__file__), "output", execution_id)
    results = {"mode": mode, "persona": persona, "cases": cases}
    
    if mode in ["with", "both"]:
        print("Running with orchestration (using imports)...")
        # For now, use first case; extend later for multiple cases
        case = cases[0] if cases else "overall"
        exit_code = orchestrated_module.run_with_orchestration_imports(REPO_ROOT, persona, case, None, None, None, output_dir)
        results["orchestrated"] = {"exit_code": exit_code, "case": case}
    
    if mode in ["without", "both"]:
        print("Running without orchestration (using imports)...")
        case = cases[0] if cases else "overall"
        exit_code = single_agent_module.run_without_orchestration_imports(REPO_ROOT, persona, case, None, None, None, output_dir)
        results["single_agent"] = {"exit_code": exit_code, "case": case}
    
    return results


def generate_report(execution_id: str, setup: dict, results: dict) -> str:
    """Generate results report"""
    import sys
    import importlib.util
    
    # Import results writer
    writer_path = os.path.join(os.path.dirname(__file__), "results_writer.py")
    spec = importlib.util.spec_from_file_location("writer", writer_path)
    writer_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(writer_module)
    
    base_dir = os.path.dirname(__file__)
    return writer_module.write_results(base_dir, execution_id, setup, results)


def main() -> int:
    print_banner()
    ensure_dirs()
    
    # Collect setup parameters
    mode = choose_mode()
    persona = choose_persona()
    cases = choose_cases()
    label = choose_label()
    
    execution_id = compute_execution_id(persona, mode, label)
    print(f"Execution ID: {execution_id}")
    
    # Sync inputs
    sync_inputs(persona)
    
    # Run pipeline(s)
    setup = {
        "mode": mode,
        "persona": persona,
        "cases": cases,
        "label": label,
        "execution_id": execution_id,
        "timestamp": datetime.now().isoformat()
    }
    
    results = run_pipeline(mode, persona, cases, execution_id)
    
    # Generate report
    report_path = generate_report(execution_id, setup, results)
    print(f"Report generated: {report_path}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
