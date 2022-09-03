## v1.1
### Game
The window is now scalable.

New hint mode: The hint will now appear in the following order:
1. If the puzzle has repeated numbers(red ones), the hint will point out all of them in red color.
2. If the puzzle has some wrong inputs that make it unsolvable, the hint will point out one of them in red color.
3. If the puzzle is correct so far, the hint will point out one of the trivial solutions in blue color.
4. If there is no wrong inputs nor trivial solutions, the hint will not appear.

Difficulty change: "Normal" and "Hard" mode now have more blanks.(40-44, 45-49 -> 40-45, 46-51)

### Code
New aligns: ```default```, ```abs```(originally ```center```), ```scale```(will be place at the scale of screen) and ```rel```(shift from some place of screen).

Replace class ```Interactable``` with ```Objects```, adding functions to show on screen and act on the input.
