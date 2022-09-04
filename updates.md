## v1.1
### Game
The window is now scalable.

Player can now save unfinished games, which can be played after returning to title screen or restarting the game.

New hint mode: The hint will now appear in the following order:
1. If the puzzle has repeated numbers(red ones), the hint will point out all of them in red color.
2. If the puzzle has some wrong inputs that make it unsolvable, the hint will point out one of them in red color.
3. If the puzzle is correct so far, the hint will point out one of the trivial solutions in blue color.
4. If there is no wrong inputs nor trivial solutions, the hint will not appear.

Difficulty change: "Normal" and "Hard" mode now have more blanks.(40-44, 45-49 -> 40-45, 46-51)

Add counter "moves" to count the total moves (including entering numbers, deleting numbers, undos and clears) and counter "used hints" to count the hints used (only count when hints pop up). "moves" counter can be seen in-game and at record screen, while "used hints" counter cannot.

### Code
New aligns: ```default```, ```abs```(originally ```center```), ```scale```(will be place at the scale of screen) and ```rel```(shift from some place of screen).

Replace class ```Interactable``` with ```Objects```, adding functions to show on screen and act on the input.

Add class ```Saves``` under ```HomePage```, saving temporary game saves.
