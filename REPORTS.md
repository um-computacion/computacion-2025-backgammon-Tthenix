# Automated Reports
## Coverage Report
```text
Name                                      Stmts   Miss  Cover   Missing
-----------------------------------------------------------------------
cli/__init__.py                               1      0   100%
cli/board_renderer.py                        77      6    92%   150-154, 190, 201
cli/cli.py                                  208     29    86%   113, 213-216, 277-278, 304, 316-319, 334-335, 338-342, 351-354, 378-379, 391, 394-397, 409, 421-422, 426, 429-432, 444, 477, 481
cli/command_parser.py                        19      3    84%   41, 67, 75
cli/game_controller.py                       36      1    97%   111
cli/input_validator.py                       17      4    76%   51-54
cli/user_interface.py                        44      0   100%
core/__init__.py                              2      0   100%
core/backgammon.py                          441     51    88%   164, 380, 460, 508, 591, 649, 652, 687, 692, 696, 700, 707, 726, 731, 735, 755-768, 782-795, 806, 928, 938-940, 944-949, 963-969
core/board.py                               195      4    98%   199-200, 239, 274
core/checker.py                              73      3    96%   67, 94, 193
core/dice.py                                 15      1    93%   43
core/player.py                               43      0   100%
pygame_ui/__init__.py                         0      0   100%
pygame_ui/backgammon_board.py               154     25    84%   192, 282, 356, 368, 387, 401-419, 440-446, 458-463, 489-490, 531-532, 553-556, 567
pygame_ui/board_interaction.py              183     63    66%   231, 235, 247, 264, 284, 287, 305-325, 334-362, 379, 401, 418, 455, 459, 463, 491-522, 535, 544-546, 549, 595-596, 628-633
pygame_ui/button.py                          29     17    41%   61-77, 89-94
pygame_ui/pygame_ui.py                       91     79    13%   25-42, 56-62, 75-82, 95-97, 110-111, 124-131, 145-172, 181-213, 217
pygame_ui/renderers/__init__.py               4      0   100%
pygame_ui/renderers/board_renderer.py        82      4    95%   304-326
pygame_ui/renderers/checker_renderer.py      84      6    93%   197-198, 276-282
pygame_ui/renderers/dice_renderer.py         63      1    98%   157
test/__init__.py                              0      0   100%
test/base_pygame_test.py                     14      0   100%
test/test_backgammon.py                      36      0   100%
test/test_backgammon_bar.py                  89      1    99%   33
test/test_backgammon_basic.py               174      0   100%
test/test_backgammon_bearing_off.py         103      0   100%
test/test_backgammon_checkers.py            103      0   100%
test/test_backgammon_moves.py               181      2    99%   404-405
test/test_bearing_off.py                    132      4    97%   163, 206-207, 348
test/test_board.py                          372      4    99%   348, 359, 505, 593
test/test_checker.py                        214      1    99%   346
test/test_cli.py                            146      1    99%   268
test/test_dice.py                           102      1    99%   211
test/test_player.py                         126      1    99%   209
test/test_pygame_ui_dice_and_turn.py         35      0   100%
test/test_pygame_ui_interaction.py          113      1    99%   289
test/test_pygame_ui_rendering.py             73      0   100%
-----------------------------------------------------------------------
TOTAL                                      3874    313    92%

```
## Pylint Report
```text

------------------------------------
Your code has been rated at 10.00/10


```
