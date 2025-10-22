import os
import sys
import subprocess
from typing import Optional, List
from ..utils import copy_output_files_to_experimentation, create_dummy_output_files


def run_without_orchestration_imports(repo_root: str, persona: str, case: Optional[str], model: Optional[str], reasoning: Optional[str], verbosity: Optional[str], output_dir: str) -> int:
    """
    Run single agent pipeline using direct imports instead of subprocess.
    For now, this is a simplified implementation that simulates the single agent process.
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
        
        # For now, we'll simulate the single agent process
        # In a real implementation, we would:
        # 1. Import the single agent modules properly
        # 2. Set up the environment correctly
        # 3. Run the actual single agent pipeline
        
        # Create output directory for this run
        from datetime import datetime
        run_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_output_dir = os.path.join(repo_root, "code-nl2-messir-without-orchestration", "output", "runs", datetime.now().strftime("%Y-%m-%d"), run_name)
        
        try:
            os.makedirs(run_output_dir, exist_ok=True)
        except OSError as e:
            raise RuntimeError(f"Failed to create output directory {run_output_dir}: {e}")
        
        # Create some dummy output files to simulate the process
        try:
            create_dummy_output_files(run_output_dir, case, persona, "single_agent")
        except RuntimeError as e:
            raise RuntimeError(f"Failed to create dummy files: {e}")
        
        # Copy output files to experimentation folder
        try:
            copy_output_files_to_experimentation(run_output_dir, output_dir, "single_agent")
        except Exception as e:
            print(f"Warning: Failed to copy output files: {e}")
            # Don't fail the entire process for copy errors
        
        print("Single agent pipeline completed successfully (simulated)")
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
