# Automated Reports
## Coverage Report
```text
Name                                      Stmts   Miss  Cover   Missing
-----------------------------------------------------------------------
cli/__init__.py                               1      0   100%
cli/board_renderer.py                        77      6    92%   131-135, 164, 172
cli/cli.py                                  208     29    86%   94, 169-172, 216-217, 243, 255-258, 268-269, 272-276, 285-288, 307-308, 320, 323-326, 338, 345-346, 350, 353-356, 368, 393, 397
cli/command_parser.py                        19      3    84%   41, 67, 75
cli/game_controller.py                       36      1    97%   111
cli/input_validator.py                       17      4    76%   51-54
cli/user_interface.py                        44      0   100%
core/__init__.py                              2      0   100%
core/backgammon.py                          441     51    88%   130, 265, 338, 372, 439, 482, 485, 509, 514, 518, 522, 529, 544, 549, 553, 566-579, 586-599, 606, 694, 704-706, 710-715, 722-728
core/board.py                               195      4    98%   155-156, 187, 212
core/checker.py                              73      3    96%   67, 94, 193
core/dice.py                                 15      1    93%   39
core/player.py                               43      0   100%
pygame_ui/__init__.py                         0      0   100%
pygame_ui/backgammon_board.py               154     25    84%   172, 254, 320, 332, 348, 362-380, 398-404, 413-418, 440-441, 479-480, 494-497, 501
pygame_ui/board_interaction.py              183     63    66%   183, 187, 195, 208, 221, 224, 242-262, 271-299, 316, 338, 355, 385, 389, 393, 421-452, 465, 474-476, 479, 518-519, 551-556
pygame_ui/button.py                          29     17    41%   55-71, 83-88
pygame_ui/pygame_ui.py                       91     79    13%   25-42, 47-53, 58-65, 70-72, 77-78, 83-90, 97-124, 129-161, 165
pygame_ui/renderers/__init__.py               4      0   100%
pygame_ui/renderers/board_renderer.py        82      4    95%   304-326
pygame_ui/renderers/checker_renderer.py      84      6    93%   197-198, 276-282
pygame_ui/renderers/dice_renderer.py         63      1    98%   157
test/__init__.py                              0      0   100%
test/base_pygame_test.py                     14      0   100%
test/test_backgammon.py                     651      3    99%   173, 924-925
test/test_bearing_off.py                    132      3    98%   133, 182, 280
test/test_board.py                          372      4    99%   323, 334, 480, 568
test/test_checker.py                        214      1    99%   315
test/test_cli.py                            146      1    99%   239
test/test_dice.py                           102      1    99%   179
test/test_player.py                         126      1    99%   184
test/test_pygame_ui_dice_and_turn.py         35      0   100%
test/test_pygame_ui_interaction.py          113      1    99%   273
test/test_pygame_ui_rendering.py             73      0   100%
-----------------------------------------------------------------------
TOTAL                                      3839    312    92%

```
## Pylint Report
```text

------------------------------------
Your code has been rated at 10.00/10


```
