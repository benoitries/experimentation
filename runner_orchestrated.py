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

def _dir_contains_dummy(dir_path: str) -> bool:
    marker = "Dummy"
    for root, _, files in os.walk(dir_path):
        for file in files:
            try:
                with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                    if marker in f.read(512):
                        return True
            except Exception:
                continue
    return False

def _find_latest_run_dir_orchestrated(repo_root: str) -> Optional[str]:
    """Find the latest orchestrated run directory under code-netlogo-to-messir/output/runs/* that is not dummy."""
    runs_root = os.path.join(repo_root, "code-netlogo-to-messir", "output", "runs")
    if not os.path.isdir(runs_root):
        return None
    candidates = []
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
            candidates.append((mtime, combo_path))
    # sort newest first and pick the first non-dummy
    for _, path in sorted(candidates, key=lambda x: x[0], reverse=True):
        if not _dir_contains_dummy(path):
            return path
    # fallback: return newest even if dummy
    return candidates and sorted(candidates, key=lambda x: x[0], reverse=True)[0][1] or None

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
        
        # Always use subprocess variant for consistency and proper error handling
        rc = run_with_orchestration(repo_root, persona, case, model, reasoning, verbosity, output_dir)
        
        # Only copy outputs if the pipeline actually succeeded
        if rc == 0:
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
        else:
            print(f"Orchestrated pipeline failed with exit code: {rc}")
            return rc
        
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
    # Sanitize OPENAI_API_KEY if it was exported/copied with shell syntax
    try:
        raw_key = env.get("OPENAI_API_KEY")
        if raw_key:
            key = raw_key.strip()
            # Remove leading export statements
            if key.lower().startswith("export "):
                key = key[len("export "):].strip()
            # If provided as KEY=VALUE, split and take the value part
            if "=" in key:
                parts = key.split("=", 1)
                # If the left side looks like the key name, use right side
                if parts[0].strip().upper() in {"OPENAI_API_KEY", "API_KEY", "KEY"}:
                    key = parts[1].strip()
            # Strip surrounding quotes
            if (key.startswith('"') and key.endswith('"')) or (key.startswith("'") and key.endswith("'")):
                key = key[1:-1].strip()
            # Final cleanup of stray characters like trailing parentheses or semicolons
            key = key.strip().strip(";")
            env["OPENAI_API_KEY"] = key
    except Exception:
        # Do not fail on sanitization; proceed with original env
        pass
    os.makedirs(output_dir, exist_ok=True)
    
    log_file = os.path.join(output_dir, "with_orchestration.log")
    print(f"Running orchestrated pipeline: {' '.join(cmd)}")
    print(f"Logging to: {log_file}")
    
    with open(log_file, "w", encoding="utf-8") as logf:
        proc = subprocess.Popen(cmd, cwd=repo_root, stdout=subprocess.PIPE, 
                               stderr=subprocess.STDOUT, env=env, text=True, bufsize=1)
        for line in proc.stdout:
            print(f"[ORCHESTRATOR] {line}", end="")
            logf.write(line)
            logf.flush()
        proc.wait()
        print(f"Orchestrated pipeline completed with exit code: {proc.returncode}")
        return proc.returncode