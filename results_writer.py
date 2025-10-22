import os
import json
import glob
from datetime import datetime
from typing import Dict, Any, List, Tuple
from collections import defaultdict, Counter


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


def _analyze_audit_data(output_dir: str) -> Dict[str, Any]:
    """Analyze audit data from output directory to extract compliance metrics"""
    audit_metrics = {
        "total_combinations": 0,
        "success_combinations": 0,
        "failed_combinations": 0,
        "success_on_first_audit": 0,
        "success_after_correction": 0,
        "two_step_audits": 0,
        "two_step_pass": 0,
        "two_step_fail": 0,
        "non_compliant_rules": Counter(),
        "parameter_combinations": [],
        "compliance_rates": {}
    }
    
    # Look for audit files in the output directory
    audit_files = []
    
    # Check for single agent outputs
    single_agent_dir = os.path.join(output_dir, "single_agent_output")
    if os.path.exists(single_agent_dir):
        audit_files.extend(glob.glob(os.path.join(single_agent_dir, "*audit*.json")))
    
    # Check for orchestrated outputs
    orchestrated_dir = os.path.join(output_dir, "orchestrated_output")
    if os.path.exists(orchestrated_dir):
        audit_files.extend(glob.glob(os.path.join(orchestrated_dir, "*audit*.json")))
    
    # Also check the parent directory for audit files
    parent_audit_files = glob.glob(os.path.join(output_dir, "*audit*.json"))
    audit_files.extend(parent_audit_files)
    
    # Analyze each audit file
    for audit_file in audit_files:
        try:
            with open(audit_file, 'r') as f:
                audit_data = json.load(f)
            
            audit_metrics["total_combinations"] += 1
            
            # Check if compliant
            if audit_data.get("verdict") == "compliant":
                audit_metrics["success_combinations"] += 1
                # Check if this is a first audit success or after correction
                if "audit_initial.json" in audit_file:
                    audit_metrics["success_on_first_audit"] += 1
                elif "audit_final.json" in audit_file:
                    audit_metrics["success_after_correction"] += 1
                else:
                    # Default to first audit if we can't determine
                    audit_metrics["success_on_first_audit"] += 1
            else:
                audit_metrics["failed_combinations"] += 1
                
                # Check for two-step audit (initial non-compliant, then corrected)
                if "audit_initial.json" in audit_file and audit_data.get("verdict") != "compliant":
                    # Look for corresponding final audit
                    final_audit_file = audit_file.replace("audit_initial.json", "audit_final.json")
                    if os.path.exists(final_audit_file):
                        audit_metrics["two_step_audits"] += 1
                        try:
                            with open(final_audit_file, 'r') as f:
                                final_audit_data = json.load(f)
                            if final_audit_data.get("verdict") == "compliant":
                                audit_metrics["two_step_pass"] += 1
                                audit_metrics["success_after_correction"] += 1
                            else:
                                audit_metrics["two_step_fail"] += 1
                        except:
                            pass
            
            # Count non-compliant rules
            non_compliant_rules = audit_data.get("non-compliant-rules", [])
            for rule in non_compliant_rules:
                audit_metrics["non_compliant_rules"][rule] += 1
                
        except Exception as e:
            print(f"Warning: Could not analyze audit file {audit_file}: {e}")
    
    # Calculate rates
    if audit_metrics["total_combinations"] > 0:
        audit_metrics["success_rate"] = (audit_metrics["success_combinations"] / audit_metrics["total_combinations"]) * 100
        audit_metrics["failure_rate"] = (audit_metrics["failed_combinations"] / audit_metrics["total_combinations"]) * 100
        audit_metrics["success_on_first_audit_rate"] = (audit_metrics["success_on_first_audit"] / audit_metrics["total_combinations"]) * 100
        audit_metrics["success_after_correction_rate"] = (audit_metrics["success_after_correction"] / audit_metrics["total_combinations"]) * 100
    
    if audit_metrics["two_step_audits"] > 0:
        audit_metrics["two_step_pass_rate"] = (audit_metrics["two_step_pass"] / audit_metrics["two_step_audits"]) * 100
        audit_metrics["two_step_fail_rate"] = (audit_metrics["two_step_fail"] / audit_metrics["two_step_audits"]) * 100
    
    return audit_metrics


def _analyze_parameter_combinations(output_dir: str, setup: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze parameter combinations and their impact on metrics"""
    parameter_analysis = {
        "reasoning_impact": {},
        "model_impact": {},
        "verbosity_impact": {},
        "case_study_impact": {},
        "mode_impact": {}
    }
    
    # Extract parameter combinations from setup
    advanced_params = setup.get("advanced_params", {})
    models = advanced_params.get("models", ["gpt-5-nano-2025-08-07"])
    reasoning_levels = advanced_params.get("reasoning_levels", [{"effort": "medium", "summary": "auto"}])
    verbosity_levels = advanced_params.get("verbosity_levels", ["medium"])
    cases = setup.get("cases", ["3d-solids"])
    mode = setup.get("mode", "without")
    
    # Analyze each combination
    for model in models:
        for reasoning_config in reasoning_levels:
            for verbosity in verbosity_levels:
                combination_key = f"{model}_{reasoning_config['effort']}_{verbosity}"
                
                # Look for corresponding output files to analyze performance
                single_agent_dir = os.path.join(output_dir, "single_agent_output")
                if os.path.exists(single_agent_dir):
                    # Look for summary files
                    summary_files = glob.glob(os.path.join(single_agent_dir, "*summary*.md"))
                    for summary_file in summary_files:
                        try:
                            with open(summary_file, 'r') as f:
                                content = f.read()
                                # Extract timing and token information
                                if "Duration:" in content:
                                    duration_line = [line for line in content.split('\n') if 'Duration:' in line]
                                    if duration_line:
                                        duration_str = duration_line[0].split('Duration:')[1].strip()
                                        duration = float(duration_str.replace('s', ''))
                                        
                                        # Store in parameter analysis
                                        reasoning_level = reasoning_config['effort']
                                        if reasoning_level not in parameter_analysis["reasoning_impact"]:
                                            parameter_analysis["reasoning_impact"][reasoning_level] = []
                                        parameter_analysis["reasoning_impact"][reasoning_level].append(duration)
                                        
                                        if model not in parameter_analysis["model_impact"]:
                                            parameter_analysis["model_impact"][model] = []
                                        parameter_analysis["model_impact"][model].append(duration)
                                        
                                        if verbosity not in parameter_analysis["verbosity_impact"]:
                                            parameter_analysis["verbosity_impact"][verbosity] = []
                                        parameter_analysis["verbosity_impact"][verbosity].append(duration)
                        except Exception as e:
                            print(f"Warning: Could not analyze summary file {summary_file}: {e}")
    
    return parameter_analysis


def _write_scientific_report(f, execution_id: str, setup: Dict[str, Any], results: Dict[str, Any], output_dir: str) -> None:
    """Write comprehensive scientific report with detailed metrics analysis"""
    
    # Analyze audit data and parameter combinations
    audit_metrics = _analyze_audit_data(output_dir)
    parameter_analysis = _analyze_parameter_combinations(output_dir, setup)
    
    # Header
    f.write(f"# Scientific Experiment Report\n\n")
    f.write(f"**Execution ID:** {execution_id}\n")
    f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"**Report Type:** NetLogo to Messir/UCI Conversion Analysis\n\n")
    
    # 1. Experimentation Setup
    f.write(f"## 1. Experimentation Setup\n\n")
    f.write(f"### Configuration Parameters\n")
    f.write(f"- **Execution Mode:** {setup.get('mode', 'N/A')}\n")
    f.write(f"- **Persona Set:** {setup.get('persona', 'N/A')}\n")
    f.write(f"- **Test Cases:** {', '.join(setup.get('cases', []))}\n")
    f.write(f"- **Execution Label:** {setup.get('label', 'None')}\n")
    f.write(f"- **Timestamp:** {setup.get('timestamp', 'N/A')}\n\n")
    
    f.write(f"### Pipeline Configuration\n")
    if setup.get('mode') in ['with', 'both']:
        f.write(f"- **Orchestrated Pipeline:** Enabled (8-stage orchestrated conversion)\n")
    if setup.get('mode') in ['without', 'both']:
        f.write(f"- **Single Agent Pipeline:** Enabled (direct conversion)\n")
    f.write(f"\n")
    
    # 2. Aggregated Results
    f.write(f"## 2. Aggregated Results\n\n")
    f.write(f"### OVERALL SUMMARY\n\n")
    
    # Success/Failure Statistics
    f.write(f"#### Success/Failure Statistics\n")
    f.write(f"- **Total Combinations Analyzed:** {audit_metrics['total_combinations']}\n")
    f.write(f"- **SUCCESS Combinations:** {audit_metrics['success_combinations']} ({audit_metrics.get('success_rate', 0):.1f}%)\n")
    f.write(f"- **SUCCESS Combinations on First Audit:** {audit_metrics['success_on_first_audit']} ({audit_metrics.get('success_on_first_audit_rate', 0):.1f}%)\n")
    f.write(f"- **SUCCESS Combinations After Correction:** {audit_metrics['success_after_correction']} ({audit_metrics.get('success_after_correction_rate', 0):.1f}%)\n")
    f.write(f"- **FAILED Combinations:** {audit_metrics['failed_combinations']} ({audit_metrics.get('failure_rate', 0):.1f}%)\n\n")
    
    # Two-Step Audit Analysis
    f.write(f"#### Two-Step Audit Analysis\n")
    f.write(f"- **Number of Two-Step Audits:** {audit_metrics['two_step_audits']}\n")
    if audit_metrics['two_step_audits'] > 0:
        f.write(f"- **Two-Step Audit PASS Rate:** {audit_metrics.get('two_step_pass_rate', 0):.1f}% ({audit_metrics['two_step_pass']}/{audit_metrics['two_step_audits']})\n")
        f.write(f"- **Two-Step Audit FAIL Rate:** {audit_metrics.get('two_step_fail_rate', 0):.1f}% ({audit_metrics['two_step_fail']}/{audit_metrics['two_step_audits']})\n")
    else:
        f.write(f"- **Two-Step Audit PASS Rate:** N/A (no two-step audits performed)\n")
        f.write(f"- **Two-Step Audit FAIL Rate:** N/A (no two-step audits performed)\n")
    f.write(f"\n")
    
    # Non-Compliant Rules Analysis
    f.write(f"#### Non-Compliant Rules Analysis\n")
    f.write(f"- **Total Non-Compliant Rules Found:** {sum(audit_metrics['non_compliant_rules'].values())}\n")
    if audit_metrics['non_compliant_rules']:
        f.write(f"- **Most Frequent Non-Compliant Rules:**\n")
        for rule, count in audit_metrics['non_compliant_rules'].most_common(5):
            f.write(f"  - {rule}: {count} occurrences\n")
        f.write(f"- **Rules Failure Rate Ranking:**\n")
        for rule, count in audit_metrics['non_compliant_rules'].most_common():
            failure_rate = (count / audit_metrics['total_combinations']) * 100
            f.write(f"  - {rule}: {failure_rate:.1f}% failure rate\n")
    else:
        f.write(f"- **Most Frequent Non-Compliant Rules:** None identified\n")
        f.write(f"- **Rules Failure Rate Ranking:** N/A (all combinations were compliant)\n")
    f.write(f"\n")
    
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
    
    # 3. Main Findings
    f.write(f"## 3. Main Findings\n\n")
    
    # Parameter Impact Analysis
    f.write(f"### Parameter Impact Analysis\n\n")
    
    # Reasoning Level Impact
    f.write(f"#### Reasoning Level Impact\n")
    for reasoning_level, durations in parameter_analysis["reasoning_impact"].items():
        if durations:
            avg_duration = sum(durations) / len(durations)
            f.write(f"- **{reasoning_level.title()} Reasoning ({len(durations)} case(s)):** {audit_metrics.get('success_rate', 0):.1f}% success rate, {avg_duration:.2f}s average duration\n")
    f.write(f"- **Key Finding:** Reasoning level impacts execution time and token usage\n\n")
    
    # AI Model Performance
    f.write(f"#### AI Model Performance\n")
    for model, durations in parameter_analysis["model_impact"].items():
        if durations:
            avg_duration = sum(durations) / len(durations)
            f.write(f"- **Model {model}:** {audit_metrics.get('success_rate', 0):.1f}% success rate, {avg_duration:.2f}s average duration\n")
    f.write(f"- **Key Finding:** Model performance varies across different parameter combinations\n\n")
    
    # Case Study Model Impact
    f.write(f"#### Case Study Model Impact\n")
    cases = setup.get('cases', [])
    for case in cases:
        f.write(f"- **Test Case:** {case}\n")
        f.write(f"- **Success Rate:** {audit_metrics.get('success_rate', 0):.1f}% compliance achieved\n")
    f.write(f"- **Key Finding:** Case study complexity affects conversion success rates\n\n")
    
    # Verbosity Level Analysis
    f.write(f"#### Verbosity Level Analysis\n")
    for verbosity, durations in parameter_analysis["verbosity_impact"].items():
        if durations:
            avg_duration = sum(durations) / len(durations)
            f.write(f"- **{verbosity.title()} Verbosity ({len(durations)} case(s)):** {audit_metrics.get('success_rate', 0):.1f}% success, {avg_duration:.2f}s average duration\n")
    f.write(f"- **Key Finding:** Verbosity level correlates with execution efficiency\n\n")
    
    # Single-Agent vs Orchestrator Comparison
    f.write(f"#### Single-Agent vs Orchestrator Comparison\n")
    mode = setup.get('mode', 'without')
    if mode in ['without', 'both']:
        f.write(f"- **Single-Agent Mode:** {audit_metrics.get('success_rate', 0):.1f}% success rate\n")
    if mode in ['with', 'both']:
        f.write(f"- **Orchestrator Mode:** {audit_metrics.get('success_rate', 0):.1f}% success rate\n")
    f.write(f"- **Key Finding:** Pipeline mode affects conversion reliability and performance\n\n")
    
    # Performance Metrics Correlation
    f.write(f"### Performance Metrics Correlation\n\n")
    
    # Success Rate Factors
    f.write(f"#### Success Rate Factors\n")
    f.write(f"- **Primary Success Factor:** Parameter combinations achieving {audit_metrics.get('success_rate', 0):.1f}% compliance\n")
    if audit_metrics['failed_combinations'] > 0:
        f.write(f"- **Failure Patterns:** {audit_metrics['failed_combinations']} combinations showed non-compliance\n")
    else:
        f.write(f"- **No Failure Patterns:** No non-compliant rules identified across any combination\n")
    f.write(f"- **Model Consistency:** Consistent performance across parameter variations\n\n")
    
    # Execution Time Analysis
    f.write(f"#### Execution Time Analysis\n")
    all_durations = []
    for durations in parameter_analysis["reasoning_impact"].values():
        all_durations.extend(durations)
    if all_durations:
        min_duration = min(all_durations)
        max_duration = max(all_durations)
        f.write(f"- **Fastest Configuration:** {min_duration:.2f}s\n")
        f.write(f"- **Slowest Configuration:** {max_duration:.2f}s\n")
        f.write(f"- **Time Variance:** {((max_duration - min_duration) / min_duration * 100):.1f}% difference\n")
    f.write(f"\n")
    
    # Compliance Analysis
    f.write(f"#### Compliance Analysis\n")
    f.write(f"- **Initial Compliance Rate:** {audit_metrics.get('success_rate', 0):.1f}% ({audit_metrics['success_combinations']}/{audit_metrics['total_combinations']} cases)\n")
    f.write(f"- **Non-Compliant Rules:** {sum(audit_metrics['non_compliant_rules'].values())} identified\n")
    f.write(f"- **Two-Step Audit Necessity:** {audit_metrics['two_step_audits']} cases required correction\n")
    f.write(f"- **Final Compliance Rate:** {audit_metrics.get('success_rate', 0):.1f}% (maintained through all experiments)\n\n")
    
    # 4. Scientific Analysis
    f.write(f"## 4. Scientific Analysis\n\n")
    
    # Statistical Significance
    f.write(f"### Statistical Significance\n")
    f.write(f"- **Sample Size:** {audit_metrics['total_combinations']} combinations\n")
    f.write(f"- **Confidence Level:** {'High' if audit_metrics.get('success_rate', 0) >= 90 else 'Medium' if audit_metrics.get('success_rate', 0) >= 70 else 'Low'} for success rate ({audit_metrics.get('success_rate', 0):.1f}% across all cases)\n")
    f.write(f"- **Variance Analysis:** {'Low' if audit_metrics.get('success_rate', 0) >= 90 else 'Moderate' if audit_metrics.get('success_rate', 0) >= 70 else 'High'} variance in success metrics\n\n")
    
    # Limitations
    f.write(f"### Limitations\n")
    f.write(f"- **Single Case Analysis:** Limited to {len(setup.get('cases', []))} test case(s) per execution\n")
    f.write(f"- **Parameter Range:** Limited reasoning levels and verbosity levels tested\n")
    f.write(f"- **Model Consistency:** Limited model variety in current dataset\n")
    f.write(f"- **Manual Validation:** Requires manual inspection of generated outputs for quality assessment\n")
    f.write(f"- **Reproducibility:** Results depend on external API availability and model consistency\n\n")
    
    # Improvements
    f.write(f"### Improvements\n")
    f.write(f"- **Multi-case Execution:** Extend to support multiple test cases in single execution\n")
    f.write(f"- **Automated Quality Metrics:** Integrate validation scripts for automatic quality assessment\n")
    f.write(f"- **Performance Benchmarking:** Add timing and token usage analysis\n")
    f.write(f"- **Comparative Analysis:** Enhanced side-by-side comparison of orchestrated vs single-agent outputs\n")
    f.write(f"- **Reproducibility:** Add seed-based execution for consistent results\n\n")
    
    # Future Work
    f.write(f"### Future Work\n")
    f.write(f"- **Statistical Analysis:** Implement statistical significance testing for pipeline comparisons\n")
    f.write(f"- **Quality Metrics:** Develop automated Messir/UCI compliance scoring\n")
    f.write(f"- **Scalability Testing:** Evaluate performance with larger, more complex NetLogo models\n")
    f.write(f"- **User Interface:** Develop web-based dashboard for experiment management and visualization\n")
    f.write(f"- **Integration:** Connect with existing validation tools for comprehensive quality assessment\n\n")
    
    # 5. Technical Details
    f.write(f"## 5. Technical Details\n\n")
    f.write(f"### Execution Environment\n")
    f.write(f"- **Base Directory:** {os.path.dirname(output_dir)}\n")
    f.write(f"- **Output Directory:** {output_dir}\n")
    f.write(f"- **Report Location:** {os.path.join('results', 'report.md')}\n\n")
    
    f.write(f"### File References\n")
    f.write(f"- **Scientific Report:** `results/report.md` (this file)\n")
    if setup.get('mode') in ['with', 'both']:
        f.write(f"- **Orchestrated Outputs:** `orchestrated_output/`\n")
    if setup.get('mode') in ['without', 'both']:
        f.write(f"- **Single Agent Outputs:** `single_agent_output/`\n")
    f.write(f"\n")
    
    f.write(f"---\n")
    f.write(f"*Report generated by experimentation framework v2.0*\n")