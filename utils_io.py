import os
import shutil
from typing import List


def sync_inputs(repo_root: str, dest_root: str, persona: str) -> None:
    """
    Sync required input files from code-netlogo-to-messir/ to experimentation/input/
    
    Args:
        repo_root: Root of the repository
        dest_root: Root of the experimentation directory
        persona: Persona set to sync
    """
    # Define source and destination paths
    source_base = os.path.join(repo_root, "code-netlogo-to-messir")
    dest_base = os.path.join(dest_root, "input")
    
    # Create destination directories
    os.makedirs(dest_base, exist_ok=True)
    
    # Sync input-netlogo
    source_netlogo = os.path.join(source_base, "input-netlogo")
    dest_netlogo = os.path.join(dest_base, "input-netlogo")
    if os.path.exists(source_netlogo):
        if os.path.exists(dest_netlogo):
            shutil.rmtree(dest_netlogo)
        shutil.copytree(source_netlogo, dest_netlogo)
        print(f"Synced input-netlogo to {dest_netlogo}")
    
    # Sync input-persona
    source_persona = os.path.join(source_base, "input-persona")
    dest_persona = os.path.join(dest_base, "input-persona")
    if os.path.exists(source_persona):
        if os.path.exists(dest_persona):
            shutil.rmtree(dest_persona)
        shutil.copytree(source_persona, dest_persona)
        print(f"Synced input-persona to {dest_persona}")
    
    # Sync input-icrash
    source_icrash = os.path.join(source_base, "input-icrash")
    dest_icrash = os.path.join(dest_base, "input-icrash")
    if os.path.exists(source_icrash):
        if os.path.exists(dest_icrash):
            shutil.rmtree(dest_icrash)
        shutil.copytree(source_icrash, dest_icrash)
        print(f"Synced input-icrash to {dest_icrash}")
    
    # Sync input-images
    source_images = os.path.join(source_base, "input-images")
    dest_images = os.path.join(dest_base, "input-images")
    if os.path.exists(source_images):
        if os.path.exists(dest_images):
            shutil.rmtree(dest_images)
        shutil.copytree(source_images, dest_images)
        print(f"Synced input-images to {dest_images}")
    
    print(f"Input sync completed for persona: {persona}")


def get_required_inputs() -> List[str]:
    """Get list of required input directories"""
    return [
        "input-netlogo",
        "input-persona", 
        "input-icrash",
        "input-images"
    ]
