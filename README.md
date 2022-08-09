# Conway's Game of Life

A zero-player deterministic game, invented by John Conway in 1970, in which the initial state of the grid decides everything.

Cells can be either dead or alive. The eight cells that surround a cell are called its "neighbours".

The rules are as follows:
  - If a live cell has fewer than 2 live neighbours, it dies of underpopulation.
  - If a live cell has more than 3 live neighbours, it dies of overpopulation.
  - Thus, any live cell with 2 or 3 live neighbours remains alive.
  - Finally, a dead cell with exactly 3 live neighbours becomes alive.
