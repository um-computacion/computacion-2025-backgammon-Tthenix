# Automated Reports
## Coverage Report
```text
Name                      Stmts   Miss  Cover   Missing
-------------------------------------------------------
core/__init__.py              0      0   100%
core/backgammon.py          427     53    88%   123, 202, 247, 300, 344, 355, 377, 407, 446, 449, 473, 478, 482, 486, 493, 508, 513, 517-530, 540-550, 559, 635, 645-647, 651-656, 663-669
core/board.py               178      9    95%   109-110, 149-150, 178, 195, 229, 246, 260
core/checker.py              73      3    96%   67, 94, 189
core/dice.py                 14      0   100%
core/player.py               43      0   100%
test/test_backgammon.py     651      3    99%   150, 800-801
test/test_board.py          344      4    99%   316, 327, 473, 509
test/test_checker.py        214      1    99%   311
test/test_dice.py           102      1    99%   178
test/test_player.py         126      1    99%   181
-------------------------------------------------------
TOTAL                      2172     75    97%

```
## Pylint Report
```text
************* Module core.dice
core/dice.py:18:8: W0107: Unnecessary pass statement (unnecessary-pass)
************* Module core.backgammon
core/backgammon.py:13:0: R0902: Too many instance attributes (10/7) (too-many-instance-attributes)
core/backgammon.py:56:12: W0612: Unused variable 'i' (unused-variable)
core/backgammon.py:191:4: R0911: Too many return statements (9/6) (too-many-return-statements)
core/backgammon.py:191:4: R0912: Too many branches (13/12) (too-many-branches)
core/backgammon.py:272:12: C0200: Consider using enumerate instead of iterating with range and len (consider-using-enumerate)
core/backgammon.py:327:12: C0200: Consider using enumerate instead of iterating with range and len (consider-using-enumerate)
core/backgammon.py:358:8: C0200: Consider using enumerate instead of iterating with range and len (consider-using-enumerate)
core/backgammon.py:393:8: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
core/backgammon.py:413:8: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
core/backgammon.py:495:15: R1716: Simplify chained comparison between the operands (chained-comparison)
core/backgammon.py:523:19: R1716: Simplify chained comparison between the operands (chained-comparison)
core/backgammon.py:524:20: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
core/backgammon.py:501:4: R0911: Too many return statements (8/6) (too-many-return-statements)
core/backgammon.py:501:4: R0912: Too many branches (22/12) (too-many-branches)
core/backgammon.py:539:8: R1702: Too many nested blocks (6/5) (too-many-nested-blocks)
core/backgammon.py:643:12: C0200: Consider using enumerate instead of iterating with range and len (consider-using-enumerate)
************* Module core.board
core/board.py:130:4: R0911: Too many return statements (7/6) (too-many-return-statements)
core/board.py:218:4: R0912: Too many branches (20/12) (too-many-branches)
************* Module test.test_backgammon
test/test_backgammon.py:331:48: W0613: Unused argument 'mock_roll' (unused-argument)

-----------------------------------
Your code has been rated at 9.91/10


```
