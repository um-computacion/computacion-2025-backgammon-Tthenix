# Automated Reports
## Coverage Report
```text
Name                                   Stmts   Miss  Cover   Missing
--------------------------------------------------------------------
cli/__init__.py                            1      0   100%
cli/cli.py                               244     27    89%   83, 166-167, 216-217, 237, 244-245, 251-252, 254-256, 262-263, 276-277, 284, 293, 297-298, 301, 303-304, 313, 344, 348
core/__init__.py                           2      0   100%
core/backgammon.py                       436     51    88%   130, 265, 318, 362, 373, 394, 424, 463, 466, 490, 495, 499, 503, 510, 525, 530, 534, 547-557, 564-577, 584, 660, 670-672, 676-681, 688-694
core/board.py                            188      6    97%   109-110, 147-148, 179, 196
core/checker.py                           73      3    96%   67, 94, 189
core/dice.py                              13      0   100%
core/player.py                            43      0   100%
pygame_ui/__init__.py                      0      0   100%
pygame_ui/pygame_ui.py                   443     83    81%   58-74, 86-91, 408-432, 598-599, 735-736, 741, 751-753, 946, 995, 1042, 1049, 1064, 1072, 1126, 1170-1175, 1208-1224, 1303-1356, 1360
test/__init__.py                           0      0   100%
test/base_pygame_test.py                  12      0   100%
test/test_backgammon.py                  651      3    99%   173, 909-910
test/test_board.py                       344      4    99%   316, 327, 473, 509
test/test_checker.py                     214      1    99%   311
test/test_cli.py                         146      1    99%   235
test/test_dice.py                        102      1    99%   178
test/test_player.py                      126      1    99%   181
test/test_pygame_ui_dice_and_turn.py      35      0   100%
test/test_pygame_ui_interaction.py       113      1    99%   237
test/test_pygame_ui_rendering.py          69      0   100%
--------------------------------------------------------------------
TOTAL                                   3255    182    94%

```
## Pylint Report
```text
************* Module computacion-2025-backgammon-Tthenix.test.test_pygame_ui_rendering
test/test_pygame_ui_rendering.py:11:0: E0401: Unable to import 'test.base_pygame_test' (import-error)
test/test_pygame_ui_rendering.py:11:0: E0611: No name 'base_pygame_test' in module 'test' (no-name-in-module)
test/test_pygame_ui_rendering.py:46:4: C0116: Missing function or method docstring (missing-function-docstring)
test/test_pygame_ui_rendering.py:46:4: C0103: Method name "setUp" doesn't conform to snake_case naming style (invalid-name)
test/test_pygame_ui_rendering.py:66:4: C0116: Missing function or method docstring (missing-function-docstring)
test/test_pygame_ui_rendering.py:66:4: C0103: Method name "tearDown" doesn't conform to snake_case naming style (invalid-name)
************* Module computacion-2025-backgammon-Tthenix.test.test_pygame_ui_interaction
test/test_pygame_ui_interaction.py:10:0: E0401: Unable to import 'test.base_pygame_test' (import-error)
test/test_pygame_ui_interaction.py:10:0: E0611: No name 'base_pygame_test' in module 'test' (no-name-in-module)
test/test_pygame_ui_interaction.py:18:4: C0103: Method name "setUp" doesn't conform to snake_case naming style (invalid-name)
************* Module computacion-2025-backgammon-Tthenix.test.test_pygame_ui_dice_and_turn
test/test_pygame_ui_dice_and_turn.py:9:0: E0401: Unable to import 'test.base_pygame_test' (import-error)
test/test_pygame_ui_dice_and_turn.py:9:0: E0611: No name 'base_pygame_test' in module 'test' (no-name-in-module)
test/test_pygame_ui_dice_and_turn.py:15:4: C0116: Missing function or method docstring (missing-function-docstring)
test/test_pygame_ui_dice_and_turn.py:15:4: C0103: Method name "setUp" doesn't conform to snake_case naming style (invalid-name)
test/test_pygame_ui_dice_and_turn.py:29:4: C0116: Missing function or method docstring (missing-function-docstring)
test/test_pygame_ui_dice_and_turn.py:29:4: C0103: Method name "tearDown" doesn't conform to snake_case naming style (invalid-name)

-----------------------------------
Your code has been rated at 9.85/10


```
