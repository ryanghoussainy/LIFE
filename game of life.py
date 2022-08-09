from tkinter import *
from copy import deepcopy
from random import choice

root = Tk()
root.title("Conway's Game of Life")
root.resizable(0, 0)

# Grid dimensions (display width is 150 pixels more)
WIDTH, HEIGHT = 1000, 700

# Cell colours
DEAD_COLOUR = "white"
ALIVE_COLOUR = "black"

# Number of cells in a row
side = 30

FONT = "Comic Sans MS"

canvas = Canvas(root, width=WIDTH + 150, height=HEIGHT)
canvas.pack()

options = [True, False] * 10

grid = [[False for x in range(side)] for i in range(round(side * 2 / 3))]

gens = 0  # Number of generations passed


def tick():
    global grid, gens
    if not pause:
        root.unbind("<Button 1>")
        root.unbind("<space>")
        new_grid = deepcopy(grid)
        canvas.delete("all")
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if y == 0 and x == 0:
                    neighbours = [grid[y][x + 1], grid[y + 1][x + 1], grid[y + 1][x]]
                elif y == 0 and x == len(grid[y]) - 1:
                    neighbours = [grid[y + 1][x], grid[y + 1][x - 1], grid[y][x - 1]]
                elif y == len(grid) - 1 and x == 0:
                    neighbours = [grid[y - 1][x], grid[y - 1][x + 1], grid[y][x + 1]]
                elif y == len(grid) - 1 and x == len(grid[y]) - 1:
                    neighbours = [grid[y - 1][x - 1], grid[y - 1][x], grid[y][x - 1]]
                elif y == 0:
                    neighbours = [grid[y][x + 1], grid[y + 1][x + 1], grid[y + 1][x], grid[y + 1][x - 1],
                                  grid[y][x - 1]]
                elif y == len(grid) - 1:
                    neighbours = [grid[y - 1][x - 1], grid[y - 1][x], grid[y - 1][x + 1], grid[y][x + 1],
                                  grid[y][x - 1]]
                elif x == 0:
                    neighbours = [grid[y - 1][x], grid[y - 1][x + 1], grid[y][x + 1], grid[y + 1][x + 1],
                                  grid[y + 1][x]]
                elif x == len(grid[y]) - 1:
                    neighbours = [grid[y - 1][x - 1], grid[y - 1][x], grid[y + 1][x], grid[y + 1][x - 1],
                                  grid[y][x - 1]]
                else:
                    neighbours = [grid[y - 1][x - 1], grid[y - 1][x], grid[y - 1][x + 1], grid[y][x + 1],
                                  grid[y + 1][x + 1],
                                  grid[y + 1][x], grid[y + 1][x - 1], grid[y][x - 1]]

                if not grid[y][x]:
                    if neighbours.count(True) == 3:
                        new_grid[y][x] = True
                elif neighbours.count(True) == 2 or neighbours.count(True) == 3:
                    new_grid[y][x] = True
                else:
                    new_grid[y][x] = False

                if new_grid[y][x]:
                    canvas.create_rectangle(WIDTH / side * x + 2, WIDTH / side * y + 2, WIDTH / side * x + WIDTH / side,
                                            WIDTH / side * y + WIDTH / side, fill=ALIVE_COLOUR)
                else:
                    canvas.create_rectangle(WIDTH / side * x + 2, WIDTH / side * y + 2, WIDTH / side * x + WIDTH / side,
                                            WIDTH / side * y + WIDTH / side, fill=DEAD_COLOUR)

        gens += 1
        generation_text.config(text=f"Generations {gens}")
        grid = deepcopy(new_grid)
        root.after(speed, tick)
    else:
        root.after(0, tick)


def start():
    """
    Start button pressed, simulation started
    """
    global grid, pause

    pause = False

    start_button.place_forget()
    exit_button.place_forget()
    randomise.place_forget()
    clear.place_forget()
    frequency_text.place_forget()
    frequency_up.place_forget()
    frequency_down.place_forget()

    pause_button.place(x=WIDTH + 37, y=55)

    grid = [[] for i in range(round(2 / 3 * side))]
    ind = -1
    for i in coord:
        if coord.index(i) % side == 0:
            ind += 1
        if i[4] == DEAD_COLOUR:
            grid[ind].append(False)
        else:
            grid[ind].append(True)
    tick()


def increase_speed():
    """
    Decrease the interval between ticks
    """
    global speed
    if speed != 50:
        speed -= 50
        speed_text.config(text=f"Speed: {speed}")
        if speed == 450:
            speed_down.place(x=WIDTH + 76, y=232)
        elif speed == 50:
            speed_up.place_forget()


def decrease_speed():
    """
    Increase the interval between ticks
    """
    global speed
    if speed != 500:
        speed += 50
        speed_text.config(text=f"Speed: {speed}")
        if speed == 100:
            speed_up.place(x=WIDTH + 39, y=232)
        elif speed == 500:
            speed_down.place_forget()


def select_colour(event):
    global cell_colour
    cx, cy = event.x, event.y
    for cell in coord:
        if cell[0] <= cx <= cell[2] and cell[1] <= cy <= cell[3]:
            if cell[4] == DEAD_COLOUR:
                cell_colour = ALIVE_COLOUR
            else:
                cell_colour = DEAD_COLOUR
            canvas.create_rectangle(cell[0], cell[1], cell[2], cell[3], fill=cell_colour)
            cell[4] = cell_colour


def motion(event):
    cx, cy = event.x, event.y
    for cell in coord:
        if cell[0] <= cx <= cell[2] and cell[1] <= cy <= cell[3]:
            canvas.create_rectangle(cell[0], cell[1], cell[2], cell[3], fill=cell_colour)
            cell[4] = cell_colour


def exit():
    """
    Stops the program
    """
    root.destroy()


def display(board):
    """
    Displays grid
    """
    global coord
    coord = []
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] is False:
                canvas.create_rectangle(WIDTH / side * x + 2, WIDTH / side * y + 2, WIDTH / side * x + WIDTH / side,
                                        WIDTH / side * y + WIDTH / side, fill=DEAD_COLOUR)
                coord.append([WIDTH / side * x + 2, WIDTH / side * y + 2, WIDTH / side * x + WIDTH / side,
                              WIDTH / side * y + WIDTH / side, DEAD_COLOUR])
            else:
                canvas.create_rectangle(WIDTH / side * x + 2, WIDTH / side * y + 2, WIDTH / side * x + WIDTH / side,
                                        WIDTH / side * y + WIDTH / side, fill=ALIVE_COLOUR)
                coord.append([WIDTH / side * x + 2, WIDTH / side * y + 2, WIDTH / side * x + WIDTH / side,
                              WIDTH / side * y + WIDTH / side, ALIVE_COLOUR])


def randomise_board():
    global grid
    grid = [[choice(options) for i in range(side)] for x in range(round(2 / 3 * side))]
    display(grid)


def increase_frequency():
    """
    Increases black/white frequency for randomising grid
    """
    global frequency
    if round(frequency, 2) != 1:
        frequency += 0.05
        if round(frequency, 2) > 0.5:
            options.remove(options[options.index(False)])
        else:
            options.append(True)
    frequency_text.config(text=f"Frequency: {round(frequency, 2)}")


def decrease_frequency():
    """
    Decreases black/white frequency for randomising grid
    """
    global frequency
    if round(frequency, 2) != 0.05:
        frequency -= 0.05
        if round(frequency, 2) >= 0.5:
            options.append(False)
        else:
            options.remove(options[options.index(True)])
    frequency_text.config(text=f"Frequency: {round(frequency, 2)}")


def clear_grid():
    global grid
    grid = [[False for x in range(side)] for i in range(round(side * 2 / 3))]
    display(grid)


def pause():
    global pause
    pause = True
    pause_button.place_forget()
    resume_button.place(x=WIDTH + 37, y=55)


def resume():
    global pause
    pause = False
    resume_button.place_forget()
    pause_button.place(x=WIDTH + 37, y=55)


# Simulation banner
sim_label = Label(root, text="Simulation", font=(FONT, 12), bg="gray", width=15)
sim_label.place(x=WIDTH + 1, y=3)

# Start button
start_button = Button(root, text="Go!", font=(FONT, 12), bg="green", command=start, width=4, height=1)
start_button.place(x=WIDTH + 25, y=43)

# Exit button
exit_button = Button(root, text="Exit", font=(FONT, 12), bg="red", command=exit, width=4, height=1)
exit_button.place(x=WIDTH + 74, y=43)

# Pause button
pause_button = Button(root, text="Pause", font=(FONT, 12), bg="red", command=pause, width=7, height=3)

# Resume button
resume_button = Button(root, text="Resume", font=(FONT, 12), bg="green", command=resume, width=7, height=3)

# Grid randomising button
randomise = Button(root, text="Randomise!", font=(FONT, 12), bg="gold", command=randomise_board, width=9, height=1)
randomise.place(x=WIDTH + 24, y=90)

# Clear button
clear = Button(root, text="Clear", font=(FONT, 12), bg="lightblue", command=clear_grid, width=9, height=1)
clear.place(x=WIDTH + 24, y=136)

# Speed banner
speed_label = Label(root, text="Speed", font=(FONT, 12), bg="gray", width=15)
speed_label.place(x=WIDTH + 1, y=192)

# Initial speed
speed = 200

# Increase speed button
speed_up = Button(root, text="+", bg="cyan", command=increase_speed, width=4, height=1)
speed_up.place(x=WIDTH + 39, y=232)

# Decrease speed button
speed_down = Button(root, text="-", bg="cyan", command=decrease_speed, width=4, height=1)
speed_down.place(x=WIDTH + 76, y=232)

# Display speed
speed_text = Label(root, text=f"Speed: {speed}", font=(FONT, 10))
speed_text.place(x=WIDTH + 40, y=260)

# Frequency banner
frequency_label = Label(root, text="Frequency", font=(FONT, 12), bg="gray", width=15)
frequency_label.place(x=WIDTH + 1, y=292)

# Initial frequency
frequency = 0.5

# Display frequency
frequency_text = Label(root, text=f"Frequency: {frequency}", font=(FONT, 10))
frequency_text.place(x=WIDTH + 30, y=360)

# Increase frequency button
frequency_up = Button(root, text="+", bg="cyan", command=increase_frequency, width=4, height=1)
frequency_up.place(x=WIDTH + 39, y=332)

# Decrease frequency button
frequency_down = Button(root, text="-", bg="cyan", command=decrease_frequency, width=4, height=1)
frequency_down.place(x=WIDTH + 76, y=332)

# Display number of generations
generation_text = Label(root, text=f"Generations: {gens}", font=(FONT, 12))
generation_text.place(x=WIDTH + 10, y=HEIGHT - 60)

display(grid)

canvas.bind("<B1-Motion>", motion)
canvas.bind("<Button-1>", select_colour)

root.mainloop()
