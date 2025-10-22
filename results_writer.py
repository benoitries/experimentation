import os
import json
from datetime import datetime
from typing import Dict, Any


def write_results(base_dir: str, execution_id: str, setup: Dict[str, Any], results: Dict[str, Any]) -> str:
    """
    Write experiment results to a scientific report in dedicated subfolder
    
    Args:
        base_dir: Base directory of experimentation project
        execution_id: Execution identifier
        setup: Setup parameters
        results: Results data
        
    Returns:
        Path to the generated scientific report
    """
    # Create main output directory
    output_dir = os.path.join(base_dir, "output", execution_id)
    os.makedirs(output_dir, exist_ok=True)
    
    # Create dedicated results subfolder
    results_subfolder = os.path.join(output_dir, "results")
    os.makedirs(results_subfolder, exist_ok=True)
    
    # Generate scientific report
    report_file = os.path.join(results_subfolder, "report.md")
    with open(report_file, "w") as f:
        _write_scientific_report(f, execution_id, setup, results, output_dir)
    
    print(f"Scientific report written to: {results_subfolder}")
    return report_file


def _write_scientific_report(f, execution_id: str, setup: Dict[str, Any], results: Dict[str, Any], output_dir: str) -> None:
    """Write comprehensive scientific report following task 078 structure"""
    
    # Header
    f.write(f"# Scientific Experiment Report\n\n")
    f.write(f"**Execution ID:** {execution_id}\n")
    f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"**Report Type:** NetLogo to Messir/UCI Conversion Analysis\n\n")
    
    # 1. Experimentation Setup
    f.write(f"## 1. Experimentation Setup\n\n")
    f.write(f"### Configuration Parameters\n")
    f.write(f"- **Execution Mode:** {setup.get('mode', 'N/A')}\n")
    f.write(f"**Persona Set:** {setup.get('persona', 'N/A')}\n")
    f.write(f"**Test Cases:** {', '.join(setup.get('cases', []))}\n")
    f.write(f"**Execution Label:** {setup.get('label', 'None')}\n")
    f.write(f"**Timestamp:** {setup.get('timestamp', 'N/A')}\n\n")
    
    f.write(f"### Pipeline Configuration\n")
    if setup.get('mode') in ['with', 'both']:
        f.write(f"- **Orchestrated Pipeline:** Enabled (8-stage orchestrated conversion)\n")
    if setup.get('mode') in ['without', 'both']:
        f.write(f"- **Single Agent Pipeline:** Enabled (direct conversion)\n")
    f.write(f"\n")
    
    # 2. Aggregated Results
    f.write(f"## 2. Aggregated Results\n\n")
    f.write(f"### OVERALL SUMMARY\n\n")
    
    # Pipeline execution results
    if "orchestrated" in results:
        orchestrated = results["orchestrated"]
        f.write(f"#### Orchestrated Pipeline Results\n")
        f.write(f"- **Exit Code:** {orchestrated.get('exit_code', 'N/A')}\n")
        f.write(f"- **Test Case:** {orchestrated.get('case', 'N/A')}\n")
        f.write(f"- **Status:** {'✅ SUCCESS' if orchestrated.get('exit_code') == 0 else '❌ FAILED'}\n\n")
    
    if "single_agent" in results:
        single_agent = results["single_agent"]
        f.write(f"#### Single Agent Pipeline Results\n")
        f.write(f"- **Exit Code:** {single_agent.get('exit_code', 'N/A')}\n")
        f.write(f"- **Test Case:** {single_agent.get('case', 'N/A')}\n")
        f.write(f"- **Status:** {'✅ SUCCESS' if single_agent.get('exit_code') == 0 else '❌ FAILED'}\n\n")
    
    # Output structure information
    f.write(f"### Output Structure\n")
    f.write(f"Results are organized in the following structure:\n")
    f.write(f"```\n")
    f.write(f"{os.path.basename(output_dir)}/\n")
    if setup.get('mode') in ['with', 'both']:
        f.write(f"├── orchestrated_output/     # Orchestrated pipeline outputs\n")
    if setup.get('mode') in ['without', 'both']:
        f.write(f"├── single_agent_output/     # Single agent pipeline outputs\n")
    f.write(f"└── results/\n")
    f.write(f"    └── report.md              # This scientific report\n")
    f.write(f"```\n\n")
    
    # 3. Scientific Analysis
    f.write(f"## 3. Scientific Analysis\n\n")
    
    # Findings
    f.write(f"### Findings\n\n")
    success_count = 0
    total_pipelines = 0
    
    if "orchestrated" in results:
        total_pipelines += 1
        if results["orchestrated"].get('exit_code') == 0:
            success_count += 1
    
    if "single_agent" in results:
        total_pipelines += 1
        if results["single_agent"].get('exit_code') == 0:
            success_count += 1
    
    success_rate = (success_count / total_pipelines * 100) if total_pipelines > 0 else 0
    
    f.write(f"- **Pipeline Success Rate:** {success_rate:.1f}% ({success_count}/{total_pipelines} pipelines completed successfully)\n")
    f.write(f"- **Execution Mode:** {setup.get('mode', 'N/A')} (comparing orchestrated vs single-agent approaches)\n")
    f.write(f"- **Test Case Coverage:** {len(setup.get('cases', []))} case(s) analyzed\n\n")
    
    # Limitations
    f.write(f"### Limitations\n\n")
    f.write(f"- **Single Case Analysis:** Currently limited to one test case per execution\n")
    f.write(f"- **Manual Validation:** Requires manual inspection of generated outputs for quality assessment\n")
    f.write(f"- **Comparative Analysis:** Limited to exit codes; detailed performance metrics not yet integrated\n")
    f.write(f"- **Reproducibility:** Results depend on external API availability and model consistency\n\n")
    
    # Improvements
    f.write(f"### Improvements\n\n")
    f.write(f"- **Multi-case Execution:** Extend to support multiple test cases in single execution\n")
    f.write(f"- **Automated Quality Metrics:** Integrate validation scripts for automatic quality assessment\n")
    f.write(f"- **Performance Benchmarking:** Add timing and token usage analysis\n")
    f.write(f"- **Comparative Analysis:** Enhanced side-by-side comparison of orchestrated vs single-agent outputs\n")
    f.write(f"- **Reproducibility:** Add seed-based execution for consistent results\n\n")
    
    # Future Work
    f.write(f"### Future Work\n\n")
    f.write(f"- **Statistical Analysis:** Implement statistical significance testing for pipeline comparisons\n")
    f.write(f"- **Quality Metrics:** Develop automated Messir/UCI compliance scoring\n")
    f.write(f"- **Scalability Testing:** Evaluate performance with larger, more complex NetLogo models\n")
    f.write(f"- **User Interface:** Develop web-based dashboard for experiment management and visualization\n")
    f.write(f"- **Integration:** Connect with existing validation tools for comprehensive quality assessment\n\n")
    
    # Technical Details
    f.write(f"## 4. Technical Details\n\n")
    f.write(f"### Execution Environment\n")
    f.write(f"- **Base Directory:** {os.path.dirname(output_dir)}\n")
    f.write(f"**Output Directory:** {output_dir}\n")
    f.write(f"**Report Location:** {os.path.join('results', 'report.md')}\n\n")
    
    f.write(f"### File References\n")
    f.write(f"- **Scientific Report:** `results/report.md` (this file)\n")
    if setup.get('mode') in ['with', 'both']:
        f.write(f"- **Orchestrated Outputs:** `orchestrated_output/`\n")
    if setup.get('mode') in ['without', 'both']:
        f.write(f"- **Single Agent Outputs:** `single_agent_output/`\n")
    f.write(f"\n")
    
    f.write(f"---\n")
    f.write(f"*Report generated by experimentation framework v1.0*\n")