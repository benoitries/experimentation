# Experimentation Project

This project provides a unified interface for running both orchestrated and single-agent NetLogo to Messir/UCI conversion pipelines.

## Structure

- `main.py` - Main entry point for the experimentation runner
- `runner_orchestrated.py` - Orchestrated pipeline runner
- `runner_single_agent.py` - Single agent pipeline runner
- `results_writer.py` - Results writer (writes to output/ directory)
- `utils.py` - Common utilities
- `test_import_runner.py` - Test script for import runners
- `performance_test_final.py` - Performance comparison script
- `input/` - Synchronized input files
- `output/` - Experiment output files
- `templates/` - Report templates

## Usage

Run the main script to start an interactive experimentation session:

```bash
python main.py
```

The script will:
1. List available NetLogo cases
2. Allow selection of pipeline mode (orchestrated, single-agent, or both)
3. Sync required input files
4. Run the selected pipeline(s)
5. Generate results reports

## Pipeline Modes

### Orchestrated Mode
Runs the full 8-stage orchestrated pipeline from `code-netlogo-to-messir/`.

### Single Agent Mode  
Runs the single-agent pipeline from `code-nl2-messir-without-orchestration/`.

### Both Mode
Runs both pipelines for comparison.

## Input Synchronization

The experimentation runner automatically syncs required input files from the main code projects:
- `input-netlogo/` - NetLogo source files
- `input-persona/` - Agent personas
- `input-icrash/` - iCrash reference documents
- `input-images/` - Interface images

## Output Structure

Results are organized by execution ID (timestamp-persona-mode-label):
```
output/
  YYYY-MM-DD/
    HHMM-persona-mode-label/
      orchestrated_output/  # If orchestrated mode
        orchestrator_output.log  # Orchestrated pipeline execution log
      single_agent_output/  # If single agent mode
        single_agent_output.log  # Single agent pipeline execution log
```

## Results

Results are written to the `output/` directory with:
- `setup.json` - Experiment setup parameters
- `results.json` - Pipeline execution results
- `report.md` - Human-readable report
