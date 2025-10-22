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


