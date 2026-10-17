import pygame
import numpy as np
import tkinter as tk
from tkinter import messagebox, simpledialog

root = tk.Tk()
root.withdraw()

# --- Parameters ---
COLOR_BG = np.array([16, 16, 16], dtype=np.uint8)
COLOR_ALIVE = np.array([128, 128, 128], dtype=np.uint8)
PAUSE_FPS = 24
DENSITY = 3 / 8

def show_help() -> None:
    messagebox.showinfo(
        "Help",
        "H = Help\n" \
        "I = Info\n" \
        "A = AutoReset\n" \
        "Q = AutoPause\n" \
        "C = Clear\n" \
        "R = Generate\n" \
        "F = Change FPS\n" \
        "S = Change Size\n" \
        "P = Screenshot\n" \
        "W = Switch screen mode\n" \
        "Space = Pause\n" \
        "Enter = Next generation\n" \
    )

def update_grid(g : np.ndarray) -> np.ndarray:
    # If the type is standardised to uint8, other functions that require bool will fail.
    padded = np.pad(g.astype(np.uint8), pad_width=1, mode='wrap')
    neighbors = (
        padded[:-2, :-2] + padded[:-2, 1:-1] + padded[:-2, 2:] +
        padded[1:-1, :-2]                     + padded[1:-1, 2:] +
        padded[2:, :-2]  + padded[2:, 1:-1]  + padded[2:, 2:]
    )
    return (neighbors == 3) | (g & (neighbors == 2))

def random_grid(width : int, height : int) -> np.ndarray:
    return np.random.random((width, height)) < DENSITY

def main() -> None:
    show_help()

    width, height = 64, 64

    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE | pygame.SCALED)
    is_scaled = True
    pygame.display.set_caption(f"Conway's Game of Life {width}x{height}")
    clock = pygame.time.Clock()

    grid = random_grid(width, height)
    history = set()

    running = True
    paused = True
    auto_reset = True
    auto_pause = not auto_reset

    fps = 12
    generation = 0

    # Previously
    grid_surface = pygame.Surface((width, height))

    while running:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_SPACE: # Pause
                        paused = not paused
                    case pygame.K_RETURN:
                        if paused:
                            grid = update_grid(grid)
                            generation += 1
                    case pygame.K_a: # Auto reset
                        auto_reset = not auto_reset
                        auto_pause = False
                        history.clear()
                    case pygame.K_q: # Auto pose
                        auto_pause = not auto_pause
                        auto_reset = False
                    case pygame.K_c: # Clear
                        grid = np.zeros((width, height), dtype=bool)
                        history.clear()
                        generation = 0
                    case pygame.K_r: # Generate a new random grid
                        grid = random_grid(width, height)
                        history.clear()
                        generation = 0
                    case pygame.K_i: # Show info
                        messagebox.showinfo(
                            "info",
                            f"FPS: {fps}\n"\
                            f"Generation: {generation}\n"\
                            f"AutoReset: {auto_reset}\n"\
                            f"AutoPause: {auto_pause}"
                        )
                    case pygame.K_f: # Change FPS
                        new_fps = simpledialog.askinteger("Enter a value", "FPS (0 = No limitation)", minvalue=0)
                        fps = new_fps if new_fps is not None else fps
                    case pygame.K_p: # Screenshot
                        pygame.image.save(screen, "screenshot.png")
                        messagebox.showinfo("Screenshot", "You have taken a screenshot")
                    case pygame.K_s: # Change the grid's size
                        new_width = simpledialog.askinteger("Enter a value", "Width", minvalue=2)
                        new_height = simpledialog.askinteger("Enter a value", "Height", minvalue=2)
                        
                        if new_width and new_height:
                            width = new_width
                            height = new_height

                            pygame.display.set_caption(f"Conway's Game of Life {width}x{height}")
                            grid_surface = pygame.Surface((width, height))
                            grid = random_grid(width, height)
                            history.clear()
                            generation = 0
                            paused = True
                            if is_scaled:
                                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE | pygame.SCALED)
                            else:
                                screen = pygame.display.set_mode((width, height))
                    case pygame.K_w:
                        is_scaled = not is_scaled
                        if is_scaled:
                            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE | pygame.SCALED)
                        else:
                            screen = pygame.display.set_mode((width, height))
                    case pygame.K_h:
                        show_help()

        # Calculate the next generation
        if not paused:
            generation += 1
            if auto_reset or auto_pause:
                current_hash = hash(np.packbits(grid).tobytes())
                if current_hash in history:
                    if auto_reset:
                        grid = random_grid(width, height)
                        history.clear()
                        generation = 0
                    elif auto_pause:
                        paused = True
                else:
                    history.add(current_hash)
            grid = update_grid(grid)
            clock.tick(fps)
        else:
            # Draw and erase cells with mouse
            mouse_pressed = pygame.mouse.get_pressed()
            if mouse_pressed[0] or mouse_pressed[2]:
                x, y = pygame.mouse.get_pos()
                if 0 <= x < width and 0 <= y < height:
                    grid[x, y] = True if mouse_pressed[0] else False
                    history.clear()
                clock.tick(360)
            else:
                clock.tick(PAUSE_FPS)

        # Image rendering
        pixels = pygame.surfarray.pixels3d(grid_surface)
        pixels[:] = COLOR_BG
        pixels[grid] = COLOR_ALIVE
        del pixels
        screen.blit(grid_surface, (0, 0))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
