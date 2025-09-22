# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### [Unreleased]

## Sprint 3

### [0.0.11] - 2025-09-22

#### Fix

- Major pylint code quality improvements across all core modules
- Fixed module docstrings for all core classes (dice.py, player.py, checker.py, board.py, backgammon.py)
- Renamed board.bar to board.checker_bar to resolve pylint naming conflicts
- Added comprehensive type hints and docstrings following PEP 257
- Fixed trailing whitespace and formatting issues
- Created main.py entry point as required by coding standards
- Updated all test files to use new property names consistently
- Removed duplicate test methods to fix pylint issues
- Fixed inconsistent bar/checker_bar references in test files
- Maintained 98% test coverage throughout refactoring

### [0.0.10] - 2025-09-21

#### Fix
- Upgrade board and backgammon test for coverage 98%
- Fix pylint on test_backgammon
### [0.0.8] - 2025-09-19

#### Added

- Add checker logic
- Add board logic
- Add backgammon logic

#### Fix

- Checker test(test_move_checker_when_on_bar_raises_exception)
- Add random import to board.py

## Sprint 2

### [0.0.8] - 2025-09-15

#### Fix

- Add mock to test dice
- Add mock to test backgammon
- Add mock to test board

### [0.0.8] - 2025-09-11

#### Added

- Player class logic

### [0.0.7] - 2025-09-10

#### Added

-Dice class logic

#### Documentation

-Add uml graph

#### fix

-fix coverage reports

### [0.0.6] - 2025-09-08

#### Added

-Create the skeleton backgammon test.py
-Create the skeleton checker test.py

### [0.0.5] - 2025-09-04

#### Added

-Create github actions

## Sprint 1

### [0.0.4] - 2025-08 -28

#### Added

-Create the skeleton backgammon test.py
-Create the skeleton checker test.py

### [0.0.3] - 2025-08 -27

#### Added

-Create the skeleton player test.py

### [0.0.2] - 2025-08 -26

#### Added

-Create the skeleton board test.py

### [0.0.1] - 2025-08-25

#### Added

-Create the skeleton dice test.py

### [0.0.0] - 2025-08-23

#### Added

- Initial commit with full folder structure.
- Requeriments started with coverage==7.10.5 and pygame==2.6.1
- GitHub repository initialized for Backgammon project.
