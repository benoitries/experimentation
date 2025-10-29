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
Runs the full 8-stage orchestrated pipeline from `code-netlogo-to-lucim-agentic-workflow/`.

### Single Agent Mode  
Runs the single-agent pipeline from `code-netlogo-to-lucim-single-agent/`.

### Both Mode
Runs both pipelines for comparison.

## Input Synchronization

The experimentation runner automatically syncs required input files from the main code projects:
- `input-netlogo/` - NetLogo source files
- `input-persona/` - Agent persona sets (symlinks to the canonical `experimentation/input/input-persona/`)
- `input-valid-examples/` - Valid example diagrams and concepts

Note: Persona directories under `input-persona/` are symbolic links to `experimentation/input/input-persona/`. The default persona set is `persona-v1`; you can change it at runtime via the interactive selection menu in both pipelines.

Example layout:

```
experimentation/
  input/
    input-persona/
      persona-v1/
        PSN_1_NetLogoAbstractSyntaxExtractor.md
        PSN_2a_NetlogoInterfaceImageAnalyzer.md
        PSN_2b_NetlogoBehaviorExtractor.md
        PSN_3_LUCIMEnvironmentSynthesizer.md
        PSN_4_LUCIMScenarioSynthesizer.md
        PSN_5_PlantUMLWriter.md
        PSN_6_PlantUMLLUCIMAuditor.md
        PSN_7_PlantUMLLUCIMCorrector.md
        DSL_Target_LUCIM-full-definition-for-compliance.md
      persona-v2-after-ng-meeting/
        PSN_1_NetLogoAbstractSyntaxExtractor.md
        PSN_2a_NetlogoInterfaceImageAnalyzer.md
        PSN_2b_NetlogoBehaviorExtractor.md
        PSN_3_LUCIMEnvironmentSynthesizer.md
        PSN_4_LUCIMScenarioSynthesizer.md
        PSN_5_PlantUMLWriter.md
        PSN_6_PlantUMLLUCIMAuditor.md
        PSN_7_PlantUMLLUCIMCorrector.md
        DSL_Target_LUCIM-full-definition-for-compliance.md
```

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
