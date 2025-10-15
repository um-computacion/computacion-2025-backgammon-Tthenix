# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### [Unreleased]

## Sprint 5

### [0.0.18] - 2025-10-15

#### Fix

- Crate base pygame test for refactor pygame test to fix pylint errors

## Sprint 4

### [0.0.17] - 2025-10-14

#### Added

- Player 1 and 2 logic to move checker
- Tuple design for dice
- add test for dice and turn, ui interaction, ui rendering

### [0.0.16] - 2025-10-12

#### Added

- Movement for checker on board
- test for pygame UI interaction functionality

#### Fix

- Fix Pylint errors

### [0.0.15] - 2025-10-6

#### Added

- Add checkers design on board pygame
- Added dice rolling functionality using core game logic (Space key to roll or press the button)

#### Fixed

- Fixed module import path in pygame_ui.py to allow running directly or from main.py

### [0.0.14] - 2025-10-2

#### Added

- Board design for pygame

### [0.0.13] - 2025-10-1

### Added

Player turn on cli

## Sprint 3

### [0.0.12] - 2025-09-24

#### Added

- Pieces to board
- commandas for cli: status, moves, move, enter, bearoff, end.
- game-over detection and announcement in CLI after moves and at turn end.
- test for CLI

### [0.0.11] - 2025-09-23

#### Added

- skleton of cli
- commandas for cli: help, roll, board, turn, quit

#### Fix

- Pylint 10/10 on core and test

### [0.0.11] - 2025-09-22

#### Fix

- Major pylint code quality improvements across all core modules
- Fixed module docstrings for all core classes (dice.py, player.py, checker.py, board.py, backgammon.py)

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
