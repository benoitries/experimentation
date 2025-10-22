#!/usr/bin/env python3
"""
Final performance comparison between subprocess and import-based approaches.
This script measures execution time only.
"""

import os
import sys
import time
import tempfile
import shutil
from typing import Dict

# No longer needed - files are now in the same directory

# Import the runner modules using absolute paths
orchestrated_path = os.path.join(os.path.dirname(__file__), "runner_orchestrated.py")
single_agent_path = os.path.join(os.path.dirname(__file__), "runner_single_agent.py")

import importlib.util

# Load orchestrated module
orchestrated_spec = importlib.util.spec_from_file_location("orchestrated", orchestrated_path)
orchestrated_module = importlib.util.module_from_spec(orchestrated_spec)
orchestrated_spec.loader.exec_module(orchestrated_module)

# Load single_agent module
single_agent_spec = importlib.util.spec_from_file_location("single_agent", single_agent_path)
single_agent_module = importlib.util.module_from_spec(single_agent_spec)
single_agent_spec.loader.exec_module(single_agent_module)


def run_performance_test(test_name: str, test_func, *args, **kwargs) -> Dict:
    """Run a performance test and return metrics."""
    print(f"\n🧪 Running performance test: {test_name}")
    
    start_time = time.time()
    
    try:
        # Run the test function
        result = test_func(*args, **kwargs)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        metrics = {
            "execution_time": execution_time,
            "success": result == 0,
            "exit_code": result
        }
        
        print(f"✅ {test_name} completed in {execution_time:.3f}s")
        return metrics
        
    except Exception as e:
        end_time = time.time()
        execution_time = end_time - start_time
        
        metrics = {
            "execution_time": execution_time,
            "success": False,
            "error": str(e)
        }
        print(f"❌ {test_name} failed: {e}")
        return metrics


def compare_approaches():
    """Compare subprocess vs import-based approaches."""
    print("🚀 Starting Performance Comparison")
    print("=" * 60)
    
    # Setup test environment
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # Go up to project root
        persona = "persona-v1"
        case = "overall"
        model = "gpt-5-nano-2025-08-07"
        reasoning = "medium"
        verbosity = "low"
        output_dir = os.path.join(temp_dir, "output")
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"📁 Test environment: {temp_dir}")
        print(f"📁 Repo root: {repo_root}")
        print(f"📁 Output dir: {output_dir}")
        
        # Test results storage
        results = {}
        
        # Test 1: Orchestrated Subprocess
        results["orchestrated_subprocess"] = run_performance_test(
            "Orchestrated (Subprocess)",
            orchestrated_module.run_with_orchestration,
            repo_root, persona, case, model, reasoning, verbosity, output_dir
        )
        
        # Test 2: Orchestrated Import
        results["orchestrated_import"] = run_performance_test(
            "Orchestrated (Import)",
            orchestrated_module.run_with_orchestration_imports,
            repo_root, persona, case, model, reasoning, verbosity, output_dir
        )
        
        # Test 3: Single Agent Subprocess
        results["single_agent_subprocess"] = run_performance_test(
            "Single Agent (Subprocess)",
            single_agent_module.run_without_orchestration,
            repo_root, persona, case, model, reasoning, verbosity, output_dir
        )
        
        # Test 4: Single Agent Import
        results["single_agent_import"] = run_performance_test(
            "Single Agent (Import)",
            single_agent_module.run_without_orchestration_imports,
            repo_root, persona, case, model, reasoning, verbosity, output_dir
        )
        
        # Generate comparison report
        generate_comparison_report(results)


def generate_comparison_report(results: Dict):
    """Generate a detailed comparison report."""
    print("\n" + "=" * 60)
    print("📊 PERFORMANCE COMPARISON REPORT")
    print("=" * 60)
    
    # Orchestrated comparison
    print("\n🔄 ORCHESTRATED PIPELINE COMPARISON:")
    print("-" * 40)
    
    subprocess_metrics = results["orchestrated_subprocess"]
    import_metrics = results["orchestrated_import"]
    
    if subprocess_metrics["success"] and import_metrics["success"]:
        time_diff = import_metrics["execution_time"] - subprocess_metrics["execution_time"]
        time_improvement = (time_diff / subprocess_metrics["execution_time"]) * 100
        
        print(f"⏱️  Execution Time:")
        print(f"   Subprocess: {subprocess_metrics['execution_time']:.3f}s")
        print(f"   Import:     {import_metrics['execution_time']:.3f}s")
        print(f"   Difference: {time_diff:+.3f}s ({time_improvement:+.1f}%)")
    
    # Single Agent comparison
    print("\n🤖 SINGLE AGENT PIPELINE COMPARISON:")
    print("-" * 40)
    
    subprocess_metrics = results["single_agent_subprocess"]
    import_metrics = results["single_agent_import"]
    
    if subprocess_metrics["success"] and import_metrics["success"]:
        time_diff = import_metrics["execution_time"] - subprocess_metrics["execution_time"]
        time_improvement = (time_diff / subprocess_metrics["execution_time"]) * 100
        
        print(f"⏱️  Execution Time:")
        print(f"   Subprocess: {subprocess_metrics['execution_time']:.3f}s")
        print(f"   Import:     {import_metrics['execution_time']:.3f}s")
        print(f"   Difference: {time_diff:+.3f}s ({time_improvement:+.1f}%)")
    
    # Summary
    print("\n📋 SUMMARY:")
    print("-" * 40)
    
    all_successful = all(result["success"] for result in results.values())
    if all_successful:
        print("✅ All tests completed successfully")
        
        # Calculate overall improvements
        orchestrated_time_improvement = ((import_metrics["execution_time"] - subprocess_metrics["execution_time"]) / subprocess_metrics["execution_time"]) * 100
        single_agent_time_improvement = ((import_metrics["execution_time"] - subprocess_metrics["execution_time"]) / subprocess_metrics["execution_time"]) * 100
        
        print(f"🚀 Import-based approach shows:")
        print(f"   - Orchestrated: {orchestrated_time_improvement:+.1f}% time change")
        print(f"   - Single Agent: {single_agent_time_improvement:+.1f}% time change")
        
        if orchestrated_time_improvement < 0 and single_agent_time_improvement < 0:
            print("🎉 Import-based approach is FASTER!")
        elif orchestrated_time_improvement > 0 and single_agent_time_improvement > 0:
            print("⚠️  Import-based approach is SLOWER (expected for simulation)")
        else:
            print("📊 Mixed results - depends on implementation")
    else:
        print("❌ Some tests failed - check error messages above")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    try:
        compare_approaches()
    except KeyboardInterrupt:
        print("\n⏹️  Performance comparison interrupted by user")
    except Exception as e:
        print(f"\n❌ Performance comparison failed: {e}")
        import traceback
        traceback.print_exc()
