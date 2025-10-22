#!/usr/bin/env python3
"""
Test script for the experimentation import runners.
This script tests the import-based runners without requiring full pipeline execution.
"""

import os
import sys
import tempfile
import shutil
from datetime import datetime

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def test_orchestrated_imports():
    """Test the orchestrated import runner"""
    print("Testing orchestrated import runner...")
    
    try:
        from src.runner.orchestrated import run_with_orchestration_imports
        
        # Create temporary output directory
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = os.path.join(temp_dir, "test_output")
            os.makedirs(output_dir, exist_ok=True)
            
            # Test parameters
            repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            persona = "persona-v1"
            case = "overall"
            
            print(f"Running orchestrated imports with:")
            print(f"  Repo root: {repo_root}")
            print(f"  Persona: {persona}")
            print(f"  Case: {case}")
            print(f"  Output dir: {output_dir}")
            
            # Run the test
            exit_code = run_with_orchestration_imports(
                repo_root=repo_root,
                persona=persona,
                case=case,
                model=None,
                reasoning=None,
                verbosity=None,
                output_dir=output_dir
            )
            
            print(f"Orchestrated import runner completed with exit code: {exit_code}")
            return exit_code == 0
            
    except Exception as e:
        print(f"Error testing orchestrated imports: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_single_agent_imports():
    """Test the single agent import runner"""
    print("Testing single agent import runner...")
    
    try:
        from src.runner.single_agent import run_without_orchestration_imports
        
        # Create temporary output directory
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = os.path.join(temp_dir, "test_output")
            os.makedirs(output_dir, exist_ok=True)
            
            # Test parameters
            repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            persona = "persona-v1"
            case = "overall"
            
            print(f"Running single agent imports with:")
            print(f"  Repo root: {repo_root}")
            print(f"  Persona: {persona}")
            print(f"  Case: {case}")
            print(f"  Output dir: {output_dir}")
            
            # Run the test
            exit_code = run_without_orchestration_imports(
                repo_root=repo_root,
                persona=persona,
                case=case,
                model=None,
                reasoning=None,
                verbosity=None,
                output_dir=output_dir
            )
            
            print(f"Single agent import runner completed with exit code: {exit_code}")
            return exit_code == 0
            
    except Exception as e:
        print(f"Error testing single agent imports: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_input_sync():
    """Test the input synchronization"""
    print("Testing input synchronization...")
    
    try:
        import importlib.util
        import sys
        
        # Import the module directly like in main.py
        module_path = os.path.join(os.path.dirname(__file__), "io", "input_sync.py")
        spec = importlib.util.spec_from_file_location("input_sync", module_path)
        input_sync_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(input_sync_module)
        sync_inputs = input_sync_module.sync_inputs
        
        # Create temporary directories
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            dest_root = temp_dir
            persona = "persona-v1"
            
            print(f"Testing input sync with:")
            print(f"  Repo root: {repo_root}")
            print(f"  Dest root: {dest_root}")
            print(f"  Persona: {persona}")
            
            # Run the sync
            sync_inputs(repo_root, dest_root, persona)
            
            # Check if input directories were created
            input_dir = os.path.join(dest_root, "input")
            if os.path.exists(input_dir):
                print("Input sync completed successfully")
                return True
            else:
                print("Input sync failed - no input directory created")
                return False
                
    except Exception as e:
        print(f"Error testing input sync: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=== Experimentation Import Runner Tests ===")
    print(f"Test started at: {datetime.now().isoformat()}")
    print()
    
    tests = [
        ("Input Sync", test_input_sync),
        ("Orchestrated Imports", test_orchestrated_imports),
        ("Single Agent Imports", test_single_agent_imports),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Running {test_name} test...")
        print("-" * 50)
        success = test_func()
        results.append((test_name, success))
        print(f"{test_name}: {'PASSED' if success else 'FAILED'}")
        print()
    
    # Summary
    print("=== Test Summary ===")
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "PASSED" if success else "FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! ✅")
        return 0
    else:
        print("Some tests failed! ❌")
        return 1


if __name__ == "__main__":
    sys.exit(main())
