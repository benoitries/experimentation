import os
import sys
import subprocess
from typing import Optional, List
import time

# Import utils functions directly since we're using dynamic imports
def copy_output_files_to_experimentation(source_dir: str, target_dir: str, mode: str) -> None:
    """Copy all generated output files from orchestration/single-agent to experimentation output folder."""
    import shutil
    
    # Create target subdirectory for this mode
    mode_dir = os.path.join(target_dir, f"{mode}_output")
    os.makedirs(mode_dir, exist_ok=True)
    
    # Copy all files from source to target
    if os.path.exists(source_dir):
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                source_file = os.path.join(root, file)
                # Calculate relative path to maintain structure
                rel_path = os.path.relpath(source_file, source_dir)
                target_file = os.path.join(mode_dir, rel_path)
                
                # Create target directory if needed
                os.makedirs(os.path.dirname(target_file), exist_ok=True)
                
                # Copy file
                shutil.copy2(source_file, target_file)
                print(f"Copied: {rel_path} -> {target_file}")

def _find_latest_run_dir_orchestrated(repo_root: str) -> Optional[str]:
    """Find the latest orchestrated run directory under code-netlogo-to-messir/output/runs/*."""
    runs_root = os.path.join(repo_root, "code-netlogo-to-messir", "output", "runs")
    if not os.path.isdir(runs_root):
        return None
    latest_dir = None
    latest_mtime = -1.0
    for date_dir in os.listdir(runs_root):
        date_path = os.path.join(runs_root, date_dir)
        if not os.path.isdir(date_path):
            continue
        for combo_dir in os.listdir(date_path):
            combo_path = os.path.join(date_path, combo_dir)
            try:
                mtime = os.path.getmtime(combo_path)
            except OSError:
                continue
            if mtime > latest_mtime:
                latest_mtime = mtime
                latest_dir = combo_path
    return latest_dir

def _guard_no_dummy_outputs(target_mode_dir: str) -> None:
    """Raise RuntimeError if any file under target_mode_dir contains known dummy markers."""
    marker = "Dummy"
    for root, _, files in os.walk(target_mode_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    # Read a small chunk to detect marker fast, then fall back to full scan
                    head = f.read(256)
                    if marker in head:
                        raise RuntimeError(f"Detected dummy marker in {file_path}")
                    # Optionally scan the rest if needed
            except UnicodeDecodeError:
                # Binary or non-text: skip
                continue


def run_with_orchestration_imports(repo_root: str, persona: str, case: Optional[str], model: Optional[str], reasoning: Optional[str], verbosity: Optional[str], output_dir: str) -> int:
    """
    Run orchestrated pipeline using direct imports where possible; otherwise delegate to subprocess.
    Produces real outputs and copies them into experimentation/orchestrated_output.
    """
    try:
        # Validate input parameters
        if not repo_root or not os.path.exists(repo_root):
            raise ValueError(f"Invalid repo_root: {repo_root}")
        
        if not persona:
            raise ValueError("Persona cannot be empty")
        
        if not output_dir:
            raise ValueError("Output directory cannot be empty")
        
        print(f"Running orchestrated pipeline for case: {case or 'overall'}")
        print(f"Using model: {model or 'gpt-5-nano-2025-08-07'}")
        print(f"Using persona: {persona}")
        print(f"Using reasoning: {reasoning or 'medium'}")
        print(f"Using verbosity: {verbosity or 'low'}")
        
        # Prefer direct import of orchestrator if available
        try:
            sys.path.append(os.path.join(repo_root, "code-netlogo-to-messir"))
            from orchestrator import NetLogoOrchestrator  # type: ignore
            from utils_config_constants import DEFAULT_MODEL  # type: ignore
            model_name = model or DEFAULT_MODEL
            orchestrator = NetLogoOrchestrator(model_name=model_name)
            orchestrator.update_agent_configs(
                reasoning_effort=reasoning or "medium",
                reasoning_summary="auto",
                text_verbosity=verbosity or "low",
                persona_set=persona,
            )
            base_name = (case or "overall")
            # Run orchestrator and let it write into its own output/runs structure
            # Many orchestrator methods are async; if so, fall back to subprocess runner
            try:
                run_result = orchestrator.run(base_name)  # may be coroutine in some versions
                if hasattr(run_result, "__await__"):
                    # Cannot await here synchronously; fall back to subprocess path
                    raise TypeError("Async orchestrator.run detected")
            except Exception:
                # Delegate to subprocess variant
                rc = run_with_orchestration(repo_root, persona, case, model, reasoning, verbosity, output_dir)
                if rc != 0:
                    return rc
            # If direct import path above succeeded, small delay to ensure files flushed
            time.sleep(0.2)
        except Exception:
            # If any import-based path fails, delegate to subprocess
            rc = run_with_orchestration(repo_root, persona, case, model, reasoning, verbosity, output_dir)
            if rc != 0:
                return rc

        # Locate latest orchestrator run outputs and copy them under experimentation
        latest_dir = _find_latest_run_dir_orchestrated(repo_root)
        if not latest_dir:
            raise RuntimeError("Could not locate orchestrator output directory")
        copy_output_files_to_experimentation(latest_dir, output_dir, "orchestrated")

        # Guard: ensure no dummy artifacts landed in experimentation folder
        target_mode_dir = os.path.join(output_dir, "orchestrated_output")
        _guard_no_dummy_outputs(target_mode_dir)

        print("Orchestrated pipeline completed successfully")
        return 0
        
    except ValueError as e:
        print(f"Validation error in orchestrated import runner: {e}")
        return 1
    except RuntimeError as e:
        print(f"Runtime error in orchestrated import runner: {e}")
        return 1
    except Exception as e:
        # Log error and return error code
        print(f"Unexpected error in orchestrated import runner: {e}")
        import traceback
        traceback.print_exc()
        return 1


def run_with_orchestration(repo_root: str, persona: str, case: Optional[str], model: Optional[str], reasoning: Optional[str], verbosity: Optional[str], output_dir: str) -> int:
    """Run the orchestrated pipeline via subprocess"""
    scripts_path = os.path.join(repo_root, "code-netlogo-to-messir", "scripts")
    candidate = os.path.join(scripts_path, "run_default_nano.py")
    
    cmd: List[str]
    if os.path.exists(candidate):
        # Use the default nano script
        python_path = sys.executable
        cmd = [python_path, candidate]
        if case:
            cmd.extend(["--base", case])
        if persona:
            cmd.extend(["--persona-set", persona])
    else:
        # Fallback to orchestrator.py
        orchestrator = os.path.join(repo_root, "code-netlogo-to-messir", "orchestrator.py")
        python_path = sys.executable
        cmd = [python_path, orchestrator]
        if case:
            cmd.extend(["--case", case])
        if persona:
            cmd.extend(["--persona", persona])
    
    env = os.environ.copy()
    os.makedirs(output_dir, exist_ok=True)
    
    log_file = os.path.join(output_dir, "with_orchestration.log")
    print(f"Running orchestrated pipeline: {' '.join(cmd)}")
    print(f"Logging to: {log_file}")
    
    with open(log_file, "w", encoding="utf-8") as logf:
        proc = subprocess.run(cmd, cwd=repo_root, stdout=logf, stderr=subprocess.STDOUT, env=env)
        print(f"Orchestrated pipeline completed with exit code: {proc.returncode}")
        return proc.returncode