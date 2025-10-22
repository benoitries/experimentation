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

def _find_latest_run_dir_single_agent(repo_root: str) -> Optional[str]:
    """Find the latest single-agent run directory under code-nl2-messir-without-orchestration/output/* that is not dummy."""
    runs_root = os.path.join(repo_root, "code-nl2-messir-without-orchestration", "output")
    if not os.path.isdir(runs_root):
        return None
    candidates = []
    for name in os.listdir(runs_root):
        path = os.path.join(runs_root, name)
        if not os.path.isdir(path):
            continue
        try:
            mtime = os.path.getmtime(path)
        except OSError:
            continue
        candidates.append((mtime, path))
    for _, path in sorted(candidates, key=lambda x: x[0], reverse=True):
        if not _dir_contains_dummy(path):
            return path
    return candidates and sorted(candidates, key=lambda x: x[0], reverse=True)[0][1] or None

def _guard_no_dummy_outputs(target_mode_dir: str) -> None:
    marker = "Dummy"
    for root, _, files in os.walk(target_mode_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    head = f.read(256)
                    if marker in head:
                        raise RuntimeError(f"Detected dummy marker in {file_path}")
            except UnicodeDecodeError:
                continue


def run_without_orchestration_imports(repo_root: str, persona: str, case: Optional[str], model: Optional[str], reasoning: Optional[str], verbosity: Optional[str], output_dir: str) -> int:
    """
    Run single agent pipeline using direct imports instead of subprocess.
    Execute the real single agent pipeline via import if possible; otherwise delegate to subprocess.
    """
    try:
        # Validate input parameters
        if not repo_root or not os.path.exists(repo_root):
            raise ValueError(f"Invalid repo_root: {repo_root}")
        
        if not persona:
            raise ValueError("Persona cannot be empty")
        
        if not output_dir:
            raise ValueError("Output directory cannot be empty")
        
        print(f"Running single agent pipeline for case: {case or 'overall'}")
        print(f"Using model: {model or 'gpt-5-nano-2025-08-07'}")
        print(f"Using persona: {persona}")
        print(f"Using reasoning: {reasoning or 'medium'}")
        print(f"Using verbosity: {verbosity or 'low'}")
        
        # Force subprocess variant (stable path)
        rc = run_without_orchestration(repo_root, persona, case, model, reasoning, verbosity, output_dir)
        if rc != 0:
            return rc

        # Only copy outputs if the pipeline actually succeeded
        # Locate latest single-agent outputs and copy to experimentation folder
        latest_dir = _find_latest_run_dir_single_agent(repo_root)
        if not latest_dir:
            raise RuntimeError("Could not locate single-agent output directory")
        copy_output_files_to_experimentation(latest_dir, output_dir, "single_agent")

        target_mode_dir = os.path.join(output_dir, "single_agent_output")
        _guard_no_dummy_outputs(target_mode_dir)

        print("Single agent pipeline completed successfully")
        return 0
        
    except ValueError as e:
        print(f"Validation error in single agent import runner: {e}")
        return 1
    except RuntimeError as e:
        print(f"Runtime error in single agent import runner: {e}")
        return 1
    except Exception as e:
        # Log error and return error code
        print(f"Unexpected error in single agent import runner: {e}")
        import traceback
        traceback.print_exc()
        return 1


def run_without_orchestration(repo_root: str, persona: str, case: Optional[str], model: Optional[str], reasoning: Optional[str], verbosity: Optional[str], output_dir: str) -> int:
    """Run the single agent pipeline via subprocess"""
    scripts_path = os.path.join(repo_root, "code-nl2-messir-without-orchestration", "scripts")
    candidate = os.path.join(scripts_path, "run_default.py")
    
    cmd: List[str]
    if os.path.exists(candidate):
        # Use the default script
        python_path = sys.executable
        cmd = [python_path, candidate]
        if case:
            cmd.extend(["--base", case])
        if persona:
            cmd.extend(["--persona-set", persona])
    else:
        # Fallback to direct agent execution
        agent_script = os.path.join(repo_root, "code-nl2-messir-without-orchestration", "agent_netlogo_to_lucim.py")
        python_path = sys.executable
        cmd = [python_path, agent_script]
        if case:
            cmd.extend(["--case", case])
        if persona:
            cmd.extend(["--persona", persona])
    
    env = os.environ.copy()
    os.makedirs(output_dir, exist_ok=True)
    
    log_file = os.path.join(output_dir, "without_orchestration.log")
    print(f"Running single agent pipeline: {' '.join(cmd)}")
    print(f"Logging to: {log_file}")
    
    with open(log_file, "w", encoding="utf-8") as logf:
        proc = subprocess.run(cmd, cwd=repo_root, stdout=logf, stderr=subprocess.STDOUT, env=env)
        print(f"Single agent pipeline completed with exit code: {proc.returncode}")
        return proc.returncode
