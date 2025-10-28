#!/usr/bin/env python3
"""
Fix script to synchronize API key management between single agent and orchestrated pipeline
"""
import os
import sys
import shutil
from pathlib import Path

def fix_api_key_management():
    """Fix API key management inconsistency between single agent and orchestrated pipeline"""
    
    print("🔧 Fixing API key management inconsistency...")
    
    # Paths
    repo_root = Path(__file__).parent.parent
    single_agent_dir = repo_root / "code-netlogo-to-lucim-single-agent"
    orchestrated_dir = repo_root / "code-netlogo-to-lucim-agentic-workflow"
    
    # Copy the robust API key utility from orchestrated to single agent
    source_file = orchestrated_dir / "utils_api_key.py"
    target_file = single_agent_dir / "utils_api_key.py"
    
    if source_file.exists():
        shutil.copy2(source_file, target_file)
        print(f"✅ Copied {source_file} to {target_file}")
    else:
        print(f"❌ Source file not found: {source_file}")
        return False
    
    # Update the single agent's config constants to use the new API key utility
    config_file = single_agent_dir / "utils_config_constants.py"
    
    if config_file.exists():
        # Read the current file
        with open(config_file, 'r') as f:
            content = f.read()
        
        # Add import for the new API key utility at the top
        if "from utils_api_key import get_openai_api_key" not in content:
            # Find the first import statement and add our import after it
            lines = content.split('\n')
            new_lines = []
            added_import = False
            
            for line in lines:
                new_lines.append(line)
                if line.startswith('import ') and not added_import:
                    new_lines.append("from utils_api_key import get_openai_api_key")
                    added_import = True
            
            content = '\n'.join(new_lines)
        
        # Replace the OPENAI_API_KEY definition to use the new utility
        old_def = "OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')"
        new_def = """# Load API key using the robust utility
try:
    OPENAI_API_KEY = get_openai_api_key()
except Exception as e:
    print(f"Warning: Could not load API key: {e}")
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')"""
        
        if old_def in content:
            content = content.replace(old_def, new_def)
        
        # Write the updated file
        with open(config_file, 'w') as f:
            f.write(content)
        
        print(f"✅ Updated {config_file} to use robust API key management")
    else:
        print(f"❌ Config file not found: {config_file}")
        return False
    
    # Update the single agent's main script to use the new validation
    agent_file = single_agent_dir / "agent_netlogo_to_lucim.py"
    
    if agent_file.exists():
        with open(agent_file, 'r') as f:
            content = f.read()
        
        # Replace the validation call to use the new utility
        old_validation = "if not openai_client.validate_openai_key():"
        new_validation = """# Use the robust API key validation
try:
    from utils_api_key import validate_openai_key
    if not validate_openai_key():
        sys.exit(1)
except ImportError:
    # Fallback to old validation
    if not openai_client.validate_openai_key():
        sys.exit(1)"""
        
        if old_validation in content:
            content = content.replace(old_validation, new_validation)
        
        with open(agent_file, 'w') as f:
            f.write(content)
        
        print(f"✅ Updated {agent_file} to use robust API key validation")
    else:
        print(f"❌ Agent file not found: {agent_file}")
        return False
    
    print("🎉 API key management synchronization completed!")
    return True

def test_fix():
    """Test the fix by running a quick validation"""
    print("\n🧪 Testing the fix...")
    
    try:
        # Test importing the new utility
        sys.path.insert(0, str(Path(__file__).parent.parent / "code-netlogo-to-lucim-single-agent"))
        from utils_api_key import validate_openai_key
        
        print("✅ Successfully imported utils_api_key")
        
        # Test API key validation
        if validate_openai_key():
            print("✅ API key validation successful")
            return True
        else:
            print("❌ API key validation failed")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== API Key Management Fix ===")
    
    if fix_api_key_management():
        if test_fix():
            print("\n🎉 Fix completed successfully!")
            print("The single agent pipeline should now work with the same API key management as the orchestrated pipeline.")
        else:
            print("\n⚠️  Fix applied but test failed. Check your API key configuration.")
    else:
        print("\n❌ Fix failed. Check the error messages above.")
    
    sys.exit(0)
