import numpy as np
import cv2
import time
import random


# creates grid randomly assigning tiles alive/unalive
def createGrid():
    new_grid = []
    for y in range(gridsize[1]):
        new_row = []
        for x in range(gridsize[0]):
            new_row.append(round(random.random()))
        new_grid.append(new_row)
    
    return new_grid

# updates the grid by one step
def updateGrid(grid):

    # creates the new grid
    new_grid = []
    for y in range(gridsize[1]):
        new_row = []
        for x in range(gridsize[0]):
            new_row.append(0)
        new_grid.append(new_row)

    # iterates over all tiles of the old grid
    for y in range(gridsize[1]):
        for x in range(gridsize[0]):
            neighbors = 0
            
            # check each neighboring tile
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dy == 0 and dx == 0:
                        continue

                    neighbor_y, neighbor_x = y+dy, x+dx
                    # if neighboring tile is inside the grid
                    if 0 <= neighbor_y < gridsize[1] and 0 <= neighbor_x < gridsize[0]:
                        neighbors += grid[neighbor_y][neighbor_x]
                        
            # tile is alive if the value is a 1, unalive if the value is a 0
            is_alive = grid[y][x] == 1
            if is_alive:
                # if tile is alive, having 2 or 3 neighbors keeps it alive
                if neighbors == 2 or neighbors == 3:
                    new_grid[y][x] = 1
                else:
                    new_grid[y][x] = 0
            else:
                # if a tile is unalive, having 3 neighbors makes it alive
                if neighbors == 3:
                    new_grid[y][x] = 1
                else:
                    new_grid[y][x] = 0
            
    return new_grid

def getDisplayGrid(grid, fps):
    display = np.array(grid, dtype=np.uint8).copy()
    display = 1 - display
    display *= 200
    display = cv2.resize(display, (600, 600), interpolation=cv2.INTER_NEAREST)
    cv2.putText(display, str(round(fps, 1)), (20,20), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=255, thickness=3)
    cv2.putText(display, str(round(fps, 1)), (20,20), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=0, thickness=2)
    return display



gridsize = 120, 120
grid = createGrid()


# rolling average of fps
fps_window = [0 for i in range(100)]
prev_time = time.time()
while True:
    # update the grid
    grid = updateGrid(grid)

    # track fps
    curr_time = time.time()
    fps = 1/(curr_time-prev_time)
    fps_window.append(fps)
    del fps_window[0]
    prev_time = curr_time

    # display the grid
    display = getDisplayGrid(grid, sum(fps_window) / len(fps_window))
    cv2.imshow("img", display)
    cv2.waitKey(1)
