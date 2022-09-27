## v2.0
Upcoming multiplayer mode!
### Game
#### Main
 - Add new music type, and music type is now selectable in options.
#### Other
#### Bug fix
 - Change snow type in ingame-options will now synchronously change the text in homepage-options.
 - After finish the puzzle, the bars text will change to locked type.

## v1.1
### Game
#### Main
 - The window is now scalable.

 - Add night mode.

 - Player can now save unfinished games, which can be played after returning to title screen or restarting the game.

 - Add end-game screen, showing game time, total moves, total hint times and percentage of correct moves.

#### Other
 - Now you can select on fixed blocks (designed to make arrow keys easier to use).

 - Add counter "moves" to count the total moves (including entering numbers and undos) and "used hints" to count the hint times (only count when hints pop up). "moves" counter can be seen in-game and at record screen, while "used hints" counter cannot.

 - New hint mode: The hint will now appear in the following order:
   1. If the puzzle has repeated numbers (red ones), the hint will point out all of them in red color.
   2. If the puzzle has some wrong inputs that make it unsolvable, the hint will point out one of them in red color.
   3. If the puzzle is correct so far, the hint will point out one of the trivial solutions in blue color.
   4. If there is no wrong inputs nor trivial solutions, the hint will not appear.

Difficulty change: "Normal" and "Hard" mode now have more blanks.(40-44, 45-49 -> 40-45, 46-51)

### Code
Lots of trash thrown into module ```objects```. Just thought that every other modules import it so it is easier to call those classes, but it becomes too messy@@

 - Add module ```ingame_options``` for ingame option page.

 - New aligns: ```default```, ```abs```(originally ```center```), ```scale```(will be placed at the scale of screen) and ```rel```(shift from some place of screen).

 - Replace class ```Interactable``` with ```Objects```, adding functions to show on screen and act on the input.

 - Add class ```Saves``` under ```HomePage```, saving temporary game saves.

 - Module ```objects``` now also handles ```Color``` (for night mode), ```Settings``` (moved from ```options```), ```Controls``` (added, for more readable code while keeping efficiency). ```Background``` is merged into ```Image```. Add class ```Snow```, controlling movement of snow.

 - Add module ```formats``` to store all the formatting functions (cuz they're so damn long).
