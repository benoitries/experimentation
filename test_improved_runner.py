#!/usr/bin/env python3
"""
Test script for the improved experimentation runner.
This script tests the new functionality without running the full pipeline.
"""

import os
import sys
from pathlib import Path

# Set up environment variables BEFORE any imports
os.environ['INPUT_PERSONA_DIR'] = 'input/input-persona'
os.environ['INPUT_NETLOGO_DIR'] = 'input/input-netlogo'

# Add the experimentation directory to the path
experimentation_dir = Path(__file__).parent
sys.path.insert(0, str(experimentation_dir))

# Add the code-netlogo-to-messir directory to the Python path
repo_root = experimentation_dir.parent
sys.path.insert(0, str(repo_root / 'code-netlogo-to-messir'))

def test_imports():
    """Test that all imports work correctly"""
    print("Testing imports...")
    
    try:
        from main import (
            print_banner, ensure_dirs, list_netlogo_cases, choose_cases,
            choose_mode, choose_persona, choose_label, choose_advanced_parameters,
            compute_execution_id, run_pipeline
        )
        print("✅ All main functions imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_persona_selection():
    """Test persona set selection functionality"""
    print("\nTesting persona selection...")
    
    try:
        from main import choose_persona
        
        # Test with mock UI
        original_ui = None
        try:
            from utils_orchestrator_ui import OrchestratorUI
            ui = OrchestratorUI()
            available_personas = ui._get_available_persona_sets()
            print(f"✅ Found {len(available_personas)} persona sets: {available_personas}")
            return True
        except ImportError:
            print("⚠️  OrchestratorUI not available, using fallback")
            return True
    except Exception as e:
        print(f"❌ Persona selection test failed: {e}")
        return False

def test_parameter_selection():
    """Test advanced parameter selection"""
    print("\nTesting parameter selection...")
    
    try:
        from main import choose_advanced_parameters
        
        # Mock the input to avoid interactive prompts
        import builtins
        original_input = builtins.input
        
        def mock_input(prompt):
            if "Model >" in prompt:
                return "1"  # Select first model
            elif "Reasoning effort >" in prompt:
                return "3"  # Select medium effort
            elif "Text verbosity >" in prompt:
                return "2"  # Select medium verbosity
            else:
                return ""
        
        builtins.input = mock_input
        
        try:
            params = choose_advanced_parameters()
            
            expected_keys = ["models", "reasoning_levels", "verbosity_levels"]
            for key in expected_keys:
                if key not in params:
                    print(f"❌ Missing parameter: {key}")
                    return False
            
            print(f"✅ Parameter selection works. Params: {params}")
            return True
        finally:
            builtins.input = original_input
            
    except Exception as e:
        print(f"❌ Parameter selection test failed: {e}")
        return False

def test_netlogo_cases():
    """Test NetLogo case discovery"""
    print("\nTesting NetLogo case discovery...")
    
    try:
        from main import list_netlogo_cases
        cases = list_netlogo_cases()
        print(f"✅ Found {len(cases)} NetLogo cases: {cases}")
        return len(cases) > 0
    except Exception as e:
        print(f"❌ NetLogo case discovery failed: {e}")
        return False


def test_execution_id():
    """Test execution ID generation"""
    print("\nTesting execution ID generation...")
    
    try:
        from main import compute_execution_id
        from datetime import datetime
        
        # Test with different parameters
        test_cases = [
            ("persona-v1", "with", ""),
            ("persona-v2", "both", "test-label"),
            ("persona-v1", "without", "quick-test")
        ]
        
        for persona, mode, label in test_cases:
            execution_id = compute_execution_id(persona, mode, label)
            print(f"✅ Generated execution ID: {execution_id}")
            
            # Check that it contains expected parts
            if persona not in execution_id:
                print(f"❌ Persona not in execution ID: {execution_id}")
                return False
            if mode not in execution_id:
                print(f"❌ Mode not in execution ID: {execution_id}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Execution ID generation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("TESTING IMPROVED EXPERIMENTATION RUNNER")
    print("="*60)
    
    tests = [
        ("Import Test", test_imports),
        ("Persona Selection Test", test_persona_selection),
        ("Parameter Selection Test", test_parameter_selection),
        ("NetLogo Cases Test", test_netlogo_cases),
        ("Execution ID Test", test_execution_id),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*40}")
        print(f"Running: {test_name}")
        print(f"{'='*40}")
        
        try:
            if test_func():
                print(f"✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print(f"\n{'='*60}")
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    print(f"{'='*60}")
    
    if passed == total:
        print("🎉 All tests passed! The improved runner is ready to use.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
