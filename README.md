# 8puzzle-solver
A Python script that calculates the most efficient way to solve a 3x3 sliding puzzle, using two of the most common strategies.

I wrote this script during my time as student assistent at the Seminar for Economic Policy at LMU Munich. The goal was to compare the number of moves needed to solve a randomly chosen 3x3 sliding puzzle if individuals apply one of two strategies taught to them. I will refer to these approaches as "Worm"- and "Fix-One"-stratedies in the following.

## The Human-approach
Solving a slinging puzzle often takes frustratingly long. Sometimes you think you're getting close, only to realize that the final tiles won't fit - so you have to start all over again. 

Strategical approaches to solve the puzzle agree that fixing the first row is key to a quick success.

### The Worm Strategy
This strategy recommends to align the sequence {3, 2, 1} in the upper left corner. Starting with its "head", tile {3}, this "worm" is then moved into place.

### The Fix-One Strategy
This approach relies on fixing tile {1} in the upper left corner. After tile {1} falls into place, tiles {2} and {3} are moved to the top. Usually, the sequence ends with tile {2} sliding in between tile {1} and {3} from below.

## The Code
The 8puzzle-solver employs a modified A* search algorithm. 

## Getting Started
If you run the script, it first asks you to enter the puzzle layout as a list separated by tab. 

Entering (1 2 3 4 5 6 7 8 0) (bar the parenthesis) hence produces the layout of the solved puzzle.

If the layout entered by the user is solvable, the script proceeds to calculate the minimum amount of moves required to solve the puzzle with the "Worm"- and "Fix-One" strategy respecively. For both, the user can select whether she wants to see every move of the most efficient solution.

### Warning: For some starting layouts, the code still produces illogical solutions. Any suggestion is highly appreciated.
