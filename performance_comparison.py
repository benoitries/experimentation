#!/usr/bin/env python3
"""
Performance comparison between subprocess and import-based approaches.
This script measures execution time, memory usage, and resource consumption.
"""

import os
import sys
import time
import psutil
import tempfile
import shutil
from typing import Dict, List, Tuple
import importlib.util

# Add experimentation directory to path
sys.path.insert(0, os.path.dirname(__file__))

from src.runner.orchestrated import run_with_orchestration, run_with_orchestration_imports
from src.runner.single_agent import run_without_orchestration, run_without_orchestration_imports


class PerformanceMonitor:
    """Monitor system performance during execution."""
    
    def __init__(self):
        self.process = psutil.Process()
        self.start_time = None
        self.start_memory = None
        self.peak_memory = None
        self.cpu_samples = []
    
    def start(self):
        """Start monitoring."""
        self.start_time = time.time()
        self.start_memory = self.process.memory_info().rss
        self.peak_memory = self.start_memory
        self.cpu_samples = []
    
    def sample(self):
        """Take a performance sample."""
        current_memory = self.process.memory_info().rss
        self.peak_memory = max(self.peak_memory, current_memory)
        
        try:
            cpu_percent = self.process.cpu_percent()
            self.cpu_samples.append(cpu_percent)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    def stop(self) -> Dict:
        """Stop monitoring and return results."""
        end_time = time.time()
        end_memory = self.process.memory_info().rss
        
        return {
            "execution_time": end_time - self.start_time,
            "start_memory_mb": self.start_memory / 1024 / 1024,
            "end_memory_mb": end_memory / 1024 / 1024,
            "peak_memory_mb": self.peak_memory / 1024 / 1024,
            "memory_delta_mb": (end_memory - self.start_memory) / 1024 / 1024,
            "avg_cpu_percent": sum(self.cpu_samples) / len(self.cpu_samples) if self.cpu_samples else 0,
            "max_cpu_percent": max(self.cpu_samples) if self.cpu_samples else 0,
            "samples_count": len(self.cpu_samples)
        }


def run_performance_test(test_name: str, test_func, *args, **kwargs) -> Dict:
    """Run a performance test and return metrics."""
    print(f"\n🧪 Running performance test: {test_name}")
    
    monitor = PerformanceMonitor()
    monitor.start()
    
    try:
        # Run the test function
        result = test_func(*args, **kwargs)
        
        # Take final sample
        monitor.sample()
        metrics = monitor.stop()
        
        # Add result info
        metrics["success"] = result == 0
        metrics["exit_code"] = result
        
        print(f"✅ {test_name} completed in {metrics['execution_time']:.3f}s")
        print(f"   Memory: {metrics['start_memory_mb']:.1f}MB → {metrics['end_memory_mb']:.1f}MB (peak: {metrics['peak_memory_mb']:.1f}MB)")
        print(f"   CPU: avg {metrics['avg_cpu_percent']:.1f}%, max {metrics['max_cpu_percent']:.1f}%")
        
        return metrics
        
    except Exception as e:
        monitor.sample()
        metrics = monitor.stop()
        metrics["success"] = False
        metrics["error"] = str(e)
        print(f"❌ {test_name} failed: {e}")
        return metrics


def compare_approaches():
    """Compare subprocess vs import-based approaches."""
    print("🚀 Starting Performance Comparison")
    print("=" * 60)
    
    # Setup test environment
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_root = os.path.dirname(os.path.dirname(__file__))  # Go up to project root
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
            run_with_orchestration,
            repo_root, persona, case, model, reasoning, verbosity, output_dir
        )
        
        # Test 2: Orchestrated Import
        results["orchestrated_import"] = run_performance_test(
            "Orchestrated (Import)",
            run_with_orchestration_imports,
            repo_root, persona, case, model, reasoning, verbosity, output_dir
        )
        
        # Test 3: Single Agent Subprocess
        results["single_agent_subprocess"] = run_performance_test(
            "Single Agent (Subprocess)",
            run_without_orchestration,
            repo_root, persona, case, model, reasoning, verbosity, output_dir
        )
        
        # Test 4: Single Agent Import
        results["single_agent_import"] = run_performance_test(
            "Single Agent (Import)",
            run_without_orchestration_imports,
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
        
        memory_diff = import_metrics["peak_memory_mb"] - subprocess_metrics["peak_memory_mb"]
        memory_improvement = (memory_diff / subprocess_metrics["peak_memory_mb"]) * 100
        
        print(f"⏱️  Execution Time:")
        print(f"   Subprocess: {subprocess_metrics['execution_time']:.3f}s")
        print(f"   Import:     {import_metrics['execution_time']:.3f}s")
        print(f"   Difference: {time_diff:+.3f}s ({time_improvement:+.1f}%)")
        
        print(f"💾 Peak Memory:")
        print(f"   Subprocess: {subprocess_metrics['peak_memory_mb']:.1f}MB")
        print(f"   Import:     {import_metrics['peak_memory_mb']:.1f}MB")
        print(f"   Difference: {memory_diff:+.1f}MB ({memory_improvement:+.1f}%)")
        
        print(f"🖥️  CPU Usage:")
        print(f"   Subprocess: avg {subprocess_metrics['avg_cpu_percent']:.1f}%, max {subprocess_metrics['max_cpu_percent']:.1f}%")
        print(f"   Import:     avg {import_metrics['avg_cpu_percent']:.1f}%, max {import_metrics['max_cpu_percent']:.1f}%")
    
    # Single Agent comparison
    print("\n🤖 SINGLE AGENT PIPELINE COMPARISON:")
    print("-" * 40)
    
    subprocess_metrics = results["single_agent_subprocess"]
    import_metrics = results["single_agent_import"]
    
    if subprocess_metrics["success"] and import_metrics["success"]:
        time_diff = import_metrics["execution_time"] - subprocess_metrics["execution_time"]
        time_improvement = (time_diff / subprocess_metrics["execution_time"]) * 100
        
        memory_diff = import_metrics["peak_memory_mb"] - subprocess_metrics["peak_memory_mb"]
        memory_improvement = (memory_diff / subprocess_metrics["peak_memory_mb"]) * 100
        
        print(f"⏱️  Execution Time:")
        print(f"   Subprocess: {subprocess_metrics['execution_time']:.3f}s")
        print(f"   Import:     {import_metrics['execution_time']:.3f}s")
        print(f"   Difference: {time_diff:+.3f}s ({time_improvement:+.1f}%)")
        
        print(f"💾 Peak Memory:")
        print(f"   Subprocess: {subprocess_metrics['peak_memory_mb']:.1f}MB")
        print(f"   Import:     {import_metrics['peak_memory_mb']:.1f}MB")
        print(f"   Difference: {memory_diff:+.1f}MB ({memory_improvement:+.1f}%)")
        
        print(f"🖥️  CPU Usage:")
        print(f"   Subprocess: avg {subprocess_metrics['avg_cpu_percent']:.1f}%, max {subprocess_metrics['max_cpu_percent']:.1f}%")
        print(f"   Import:     avg {import_metrics['avg_cpu_percent']:.1f}%, max {import_metrics['max_cpu_percent']:.1f}%")
    
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
