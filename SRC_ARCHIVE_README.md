# Experimentation Source Code

This directory contains the source code for the experimentation framework.

## Structure

- `io/` - Input/output utilities
  - `input_sync.py` - Synchronizes input files from the main codebase
- `runner/` - Pipeline execution modules
  - `orchestrated.py` - Orchestrated pipeline runner
  - `single_agent.py` - Single agent pipeline runner
- `results/` - Results management utilities
  - `writer.py` - Results writer for experiment reports
- `utils.py` - Common utilities used across modules

## Usage

The modules are designed to be imported dynamically by `main.py`. Each module provides specific functionality:

- **IO Module**: Handles synchronization of input files from the main codebase
- **Runner Modules**: Execute different pipeline modes (orchestrated vs single agent)
- **Results Module**: Manages experiment results and report generation
- **Utils Module**: Provides common functionality like file copying and dummy file generation

## Dependencies

All modules use relative imports within the `src/` package structure. The main entry point is `main.py` in the parent directory.
