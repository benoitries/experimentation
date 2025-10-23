#!/usr/bin/env python3
import os
import sys
import glob
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Set up environment variables BEFORE importing modules
os.environ['INPUT_PERSONA_DIR'] = os.path.join(REPO_ROOT, "experimentation", "input", "input-persona")
os.environ['INPUT_NETLOGO_DIR'] = os.path.join(REPO_ROOT, "experimentation", "input", "input-netlogo")
os.environ['INPUT_VALID_EXAMPLES_DIR'] = os.path.join(REPO_ROOT, "experimentation", "input", "input-valid-examples")

# Add the code-netlogo-to-messir directory to the Python path
sys.path.insert(0, os.path.join(REPO_ROOT, 'code-netlogo-to-messir'))

# Import UI utilities from the orchestrator
try:
    from utils_orchestrator_ui import OrchestratorUI
    from utils_config_constants import AVAILABLE_MODELS, DEFAULT_MODEL, INPUT_PERSONA_DIR
    from utils_logging import format_parameter_bundle
    from utils_format import FormatUtils
except ImportError as e:
    print(f"Warning: Could not import orchestrator utilities: {e}")
    print("Some advanced features may not be available.")
    OrchestratorUI = None
    AVAILABLE_MODELS = ["gpt-5-nano-2025-08-07"]
    DEFAULT_MODEL = "gpt-5-nano-2025-08-07"
    INPUT_PERSONA_DIR = os.path.join(REPO_ROOT, "experimentation", "input", "input-persona")


def print_banner() -> None:
    print("=== Experimentation Runner ===")


def ensure_dirs() -> None:
    for rel in ("output", "templates", "input"):
        os.makedirs(os.path.join(os.path.dirname(__file__), rel), exist_ok=True)


def list_netlogo_cases() -> List[str]:
    """List available NetLogo cases from experimentation/input/input-netlogo/"""
    netlogo_dir = os.path.join(REPO_ROOT, "experimentation", "input", "input-netlogo")
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
    """Interactive persona set selection with validation"""
    if OrchestratorUI and INPUT_PERSONA_DIR:
        ui = OrchestratorUI()
        return ui.select_persona_set()
    else:
        # Fallback to simple input
        return input("Persona set [persona-v1]: ").strip() or "persona-v1"


def choose_label() -> str:
    return input("Optional label (e.g., quick-test) [blank for none]: ").strip()


def choose_advanced_parameters() -> Dict[str, Any]:
    """Interactive selection of advanced parameters (models, reasoning, verbosity, etc.)"""
    if not OrchestratorUI:
        # Fallback to defaults
        return {
            "models": [DEFAULT_MODEL],
            "reasoning_levels": [{"effort": "medium", "summary": "auto"}],
            "verbosity_levels": ["medium"]
        }
    
    ui = OrchestratorUI()
    params = {}
    
    # Model selection
    print("\n" + "="*60)
    print("AI MODEL SELECTION")
    print("="*60)
    models = ui.select_models()
    if not models:
        print("No models selected, using default")
        models = [DEFAULT_MODEL]
    params["models"] = models
    
    # Reasoning effort selection
    reasoning_levels = ui.select_reasoning_effort()
    if not reasoning_levels:
        print("No reasoning levels selected, using default")
        reasoning_levels = [{"effort": "medium", "summary": "auto"}]
    params["reasoning_levels"] = reasoning_levels
    
    # Text verbosity selection
    verbosity_levels = ui.select_text_verbosity()
    if not verbosity_levels:
        print("No verbosity levels selected, using default")
        verbosity_levels = ["medium"]
    params["verbosity_levels"] = verbosity_levels
    
    
    return params




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


def run_pipeline(mode: str, persona: str, cases: List[str], execution_id: str, 
                 advanced_params: Dict[str, Any] = None) -> dict:
    """Run selected pipeline(s) with advanced parameters and return results"""
    # Import orchestrated runner
    orchestrated_path = os.path.join(os.path.dirname(__file__), "runner_orchestrated.py")
    orchestrated_module = _import_module(orchestrated_path, "orchestrated")
    
    # Import single agent runner
    single_agent_path = os.path.join(os.path.dirname(__file__), "runner_single_agent.py")
    single_agent_module = _import_module(single_agent_path, "single_agent")
    
    output_dir = os.path.join(os.path.dirname(__file__), "output", execution_id)
    results = {
        "mode": mode, 
        "persona": persona, 
        "cases": cases,
        "advanced_params": advanced_params or {}
    }
    
    # Extract parameters with defaults
    models = advanced_params.get("models", [DEFAULT_MODEL]) if advanced_params else [DEFAULT_MODEL]
    reasoning_levels = advanced_params.get("reasoning_levels", [{"effort": "medium", "summary": "auto"}]) if advanced_params else [{"effort": "medium", "summary": "auto"}]
    verbosity_levels = advanced_params.get("verbosity_levels", ["medium"]) if advanced_params else ["medium"]
    
    # Calculate total combinations
    total_combinations = len(models) * len(reasoning_levels) * len(verbosity_levels)
    current_combination = 0
    
    print(f"\n{'='*80}")
    print(f"EXPERIMENTATION CONFIGURATION")
    print(f"{'='*80}")
    print(f"Mode: {mode}")
    print(f"Persona: {persona}")
    print(f"Cases: {', '.join(cases)}")
    print(f"Models: {', '.join(models)}")
    print(f"Reasoning Levels: {len(reasoning_levels)}")
    print(f"Verbosity Levels: {', '.join(verbosity_levels)}")
    print(f"Total Combinations: {total_combinations}")
    print(f"{'='*80}")
    
    # Run all combinations
    for model in models:
        for reasoning_config in reasoning_levels:
            for verbosity in verbosity_levels:
                current_combination += 1
                
                # Print parameter bundle
                if OrchestratorUI:
                    ui = OrchestratorUI()
                    ui.print_combination_header(current_combination, total_combinations)
                    ui.print_parameter_bundle(
                        model=model,
                        base_name=cases[0] if cases else "overall",
                        reasoning_effort=reasoning_config["effort"],
                        reasoning_summary=reasoning_config["summary"],
                        text_verbosity=verbosity
                    )
                else:
                    print(f"\n{'='*60}")
                    print(f"COMBINATION {current_combination}/{total_combinations}")
                    print(f"Model: {model}, Reasoning: {reasoning_config['effort']}, Verbosity: {verbosity}")
                    print(f"{'='*60}")
                
                # Run pipelines for this combination
                combination_results = {}
                
                if mode in ["without", "both"]:
                    print(f"\nRunning without orchestration at {datetime.now().strftime('%H:%M:%S')}")
                    case = cases[0] if cases else "overall"
                    exit_code = single_agent_module.run_without_orchestration_imports(
                        REPO_ROOT, persona, case, model, 
                        reasoning_config["effort"], verbosity, output_dir
                    )
                    combination_results["single_agent"] = {
                        "exit_code": exit_code, 
                        "case": case,
                        "model": model,
                        "reasoning": reasoning_config,
                        "verbosity": verbosity
                    }
                
                if mode in ["with", "both"]:
                    print(f"\nRunning with orchestration at {datetime.now().strftime('%H:%M:%S')}")
                    case = cases[0] if cases else "overall"
                    exit_code = orchestrated_module.run_with_orchestration_imports(
                        REPO_ROOT, persona, case, model, 
                        reasoning_config["effort"], verbosity, output_dir
                    )
                    combination_results["orchestrated"] = {
                        "exit_code": exit_code, 
                        "case": case,
                        "model": model,
                        "reasoning": reasoning_config,
                        "verbosity": verbosity
                    }
                
                # Store results for this combination
                combination_key = f"{model}_{reasoning_config['effort']}_{verbosity}"
                results[combination_key] = combination_results
    
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
    
    # Validate OpenAI API key if available
    if OrchestratorUI:
        ui = OrchestratorUI()
        if not ui.validate_openai_key():
            return 1
    
    # Collect setup parameters
    mode = choose_mode()
    persona = choose_persona()
    cases = choose_cases()
    label = choose_label()
    
    # Advanced parameter selection
    print("\n" + "="*60)
    print("ADVANCED PARAMETER SELECTION")
    print("="*60)
    print("Do you want to configure advanced parameters?")
    print("1. Yes - Full parameter selection (models, reasoning, verbosity, etc.)")
    print("2. No - Use defaults (single model, medium reasoning, medium verbosity)")
    choice = input("Enter choice [1-2]: ").strip() or "2"
    
    advanced_params = None
    
    if choice == "1":
        advanced_params = choose_advanced_parameters()
    else:
        print("Using default parameters")
        advanced_params = {
            "models": [DEFAULT_MODEL],
            "reasoning_levels": [{"effort": "medium", "summary": "auto"}],
            "verbosity_levels": ["medium"]
        }
    
    
    execution_id = compute_execution_id(persona, mode, label)
    print(f"Execution ID: {execution_id}")
    
    # Run pipeline(s)
    setup = {
        "mode": mode,
        "persona": persona,
        "cases": cases,
        "label": label,
        "execution_id": execution_id,
        "timestamp": datetime.now().isoformat(),
        "advanced_params": advanced_params
    }
    
    results = run_pipeline(mode, persona, cases, execution_id, advanced_params)
    
    # Generate report
    report_path = generate_report(execution_id, setup, results)
    print(f"Report generated: {report_path}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
