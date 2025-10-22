import os
import json
from datetime import datetime
from typing import Dict, Any


def write_results(base_dir: str, execution_id: str, setup: Dict[str, Any], results: Dict[str, Any]) -> str:
    """
    Write experiment results to files
    
    Args:
        base_dir: Base directory of experimentation project
        execution_id: Execution identifier
        setup: Setup parameters
        results: Results data
        
    Returns:
        Path to the generated report
    """
    # Create results directory in output folder
    results_dir = os.path.join(base_dir, "output", execution_id)
    os.makedirs(results_dir, exist_ok=True)
    
    # Write setup data
    setup_file = os.path.join(results_dir, "setup.json")
    with open(setup_file, "w") as f:
        json.dump(setup, f, indent=2)
    
    # Write results data
    results_file = os.path.join(results_dir, "results.json")
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)
    
    # Generate markdown report
    report_file = os.path.join(results_dir, "report.md")
    with open(report_file, "w") as f:
        f.write(f"# Experiment Report\n\n")
        f.write(f"**Execution ID:** {execution_id}\n")
        f.write(f"**Timestamp:** {setup.get('timestamp', 'N/A')}\n")
        f.write(f"**Mode:** {setup.get('mode', 'N/A')}\n")
        f.write(f"**Persona:** {setup.get('persona', 'N/A')}\n")
        f.write(f"**Cases:** {', '.join(setup.get('cases', []))}\n")
        f.write(f"**Label:** {setup.get('label', 'N/A')}\n\n")
        
        f.write(f"## Results\n\n")
        
        if "orchestrated" in results:
            orchestrated = results["orchestrated"]
            f.write(f"### Orchestrated Pipeline\n")
            f.write(f"- **Exit Code:** {orchestrated.get('exit_code', 'N/A')}\n")
            f.write(f"- **Case:** {orchestrated.get('case', 'N/A')}\n\n")
        
        if "single_agent" in results:
            single_agent = results["single_agent"]
            f.write(f"### Single Agent Pipeline\n")
            f.write(f"- **Exit Code:** {single_agent.get('exit_code', 'N/A')}\n")
            f.write(f"- **Case:** {single_agent.get('case', 'N/A')}\n\n")
        
        f.write(f"## Files Generated\n\n")
        f.write(f"- Setup: `{os.path.basename(setup_file)}`\n")
        f.write(f"- Results: `{os.path.basename(results_file)}`\n")
        f.write(f"- Report: `{os.path.basename(report_file)}`\n")
    
    print(f"Results written to: {results_dir}")
    return report_file