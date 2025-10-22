import os
import shutil
from typing import Optional


def copy_output_files_to_experimentation(source_dir: str, target_dir: str, mode: str) -> None:
    """
    Copy all generated output files from orchestration/single-agent to experimentation output folder.
    
    Args:
        source_dir: Source directory where files were generated
        target_dir: Target experimentation output directory
        mode: "orchestrated" or "single_agent"
    """
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


def create_dummy_output_files(output_dir: str, case: Optional[str], persona: str, mode: str) -> None:
    """
    Create dummy output files for testing purposes.
    
    Args:
        output_dir: Directory to create files in
        case: Case name
        persona: Persona name
        mode: "orchestrated" or "single_agent"
    """
    from datetime import datetime
    
    if mode == "orchestrated":
        dummy_files = [
            "01-syntax_parser/output-response.json",
            "01-syntax_parser/output-reasoning.md",
            "01-syntax_parser/output-data.json",
            "02-semantics_parser/output-response.json",
            "02-semantics_parser/output-reasoning.md",
            "02-semantics_parser/output-data.json",
            "03-messir_concepts_mapper/output-response.json",
            "03-messir_concepts_mapper/output-reasoning.md",
            "03-messir_concepts_mapper/output-data.json",
            "04-scenario_writer/output-response.json",
            "04-scenario_writer/output-reasoning.md",
            "04-scenario_writer/output-data.json",
            "05-plantuml_writer/output-response.json",
            "05-plantuml_writer/output-reasoning.md",
            "05-plantuml_writer/output-data.json",
            "05-plantuml_writer/diagram.puml",
            "06-plantuml_auditor/output-response.json",
            "06-plantuml_auditor/output-reasoning.md",
            "06-plantuml_auditor/output-data.json",
            "07-plantuml_corrector/output-response.json",
            "07-plantuml_corrector/output-reasoning.md",
            "07-plantuml_corrector/output-data.json",
            "07-plantuml_corrector/diagram.puml",
            "08-plantuml_final_auditor/output-response.json",
            "08-plantuml_final_auditor/output-reasoning.md",
            "08-plantuml_final_auditor/output-data.json"
        ]
    else:  # single_agent
        dummy_files = [
            "agent_run.log",
            "output-response.json",
            "output-reasoning.md",
            "output-data.json"
        ]
    
    try:
        for filename in dummy_files:
            dummy_file = os.path.join(output_dir, filename)
            os.makedirs(os.path.dirname(dummy_file), exist_ok=True)
            with open(dummy_file, "w") as f:
                f.write(f"# Dummy {filename} for testing\n")
                f.write(f"Generated at: {datetime.now().isoformat()}\n")
                f.write(f"Case: {case or 'overall'}\n")
                f.write(f"Persona: {persona}\n")
    except (OSError, IOError) as e:
        raise RuntimeError(f"Failed to create dummy files: {e}")
