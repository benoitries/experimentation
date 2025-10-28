#!/usr/bin/env python3
"""
Automated test script for experimentation with default values
"""
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

# Set up paths
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
EXPERIMENTATION_DIR = os.path.join(REPO_ROOT, 'experimentation')

def run_automated_test():
    """Run automated test with default values"""
    print("=== Automated Experimentation Test ===")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test both modes with default values
    test_cases = [
        {
            "mode": "without",  # Single agent
            "persona": "persona-v1",
            "case": "3d-solids",
            "model": "gpt-5-nano-2025-08-07",
            "reasoning": "medium",
            "verbosity": "medium"
        },
        {
            "mode": "with",    # Orchestrated
            "persona": "persona-v1", 
            "case": "3d-solids",
            "model": "gpt-5-nano-2025-08-07",
            "reasoning": "medium",
            "verbosity": "medium"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"TEST {i}/{len(test_cases)}: {test_case['mode'].upper()} MODE")
        print(f"{'='*60}")
        print(f"Persona: {test_case['persona']}")
        print(f"Case: {test_case['case']}")
        print(f"Model: {test_case['model']}")
        print(f"Reasoning: {test_case['reasoning']}")
        print(f"Verbosity: {test_case['verbosity']}")
        
        try:
            # Import the appropriate runner
            if test_case['mode'] == 'without':
                from runner_single_agent import run_without_orchestration_imports
                exit_code = run_without_orchestration_imports(
                    REPO_ROOT, 
                    test_case['persona'], 
                    test_case['case'], 
                    test_case['model'], 
                    test_case['reasoning'], 
                    test_case['verbosity'],
                    os.path.join(EXPERIMENTATION_DIR, 'output', 'automated-test')
                )
            else:  # with orchestration
                from runner_orchestrated import run_with_orchestration_imports
                exit_code = run_with_orchestration_imports(
                    REPO_ROOT,
                    test_case['persona'],
                    test_case['case'],
                    test_case['model'],
                    test_case['reasoning'],
                    test_case['verbosity'],
                    os.path.join(EXPERIMENTATION_DIR, 'output', 'automated-test')
                )
            
            result = {
                "test_case": test_case,
                "exit_code": exit_code,
                "status": "SUCCESS" if exit_code == 0 else "FAILED",
                "timestamp": datetime.now().isoformat()
            }
            results.append(result)
            
            print(f"Exit code: {exit_code}")
            print(f"Status: {result['status']}")
            
        except Exception as e:
            result = {
                "test_case": test_case,
                "exit_code": -1,
                "status": "ERROR",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            results.append(result)
            print(f"Error: {e}")
            print(f"Status: {result['status']}")
    
    # Generate summary report
    print(f"\n{'='*80}")
    print("TEST SUMMARY")
    print(f"{'='*80}")
    
    success_count = sum(1 for r in results if r['status'] == 'SUCCESS')
    total_count = len(results)
    
    print(f"Total tests: {total_count}")
    print(f"Successful: {success_count}")
    print(f"Failed: {total_count - success_count}")
    
    print(f"\nDetailed Results:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result['test_case']['mode'].upper()} mode: {result['status']} (exit code: {result['exit_code']})")
        if result['status'] == 'ERROR':
            print(f"     Error: {result['error']}")
    
    # Write results to file
    output_file = os.path.join(EXPERIMENTATION_DIR, 'output', 'automated-test-results.json')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    import json
    with open(output_file, 'w') as f:
        json.dump({
            "test_summary": {
                "total_tests": total_count,
                "successful": success_count,
                "failed": total_count - success_count,
                "timestamp": datetime.now().isoformat()
            },
            "results": results
        }, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
    
    return success_count == total_count

if __name__ == "__main__":
    success = run_automated_test()
    sys.exit(0 if success else 1)
