# Conway's Game of Life (Pygame + NumPy)
An interactive, high-performance implementation of **Conway's Game of Life** built with Python, Pygame, and NumPy. 

Featuring vectorized grid computations with toroidal (wrap-around) boundaries, real-time interactive drawing, state history detection (auto-reset/auto-pause on infinite loops), and full runtime customization.

## Features

- **High Performance**: Vectorized cell update calculations using NumPy array operations.
- **Toroidal Grid**: Grid edges seamlessly wrap around top-to-bottom and left-to-right.
- **Loop Detection**: Detects repeating states/oscillators using packed binary hash sets.
  - **Auto-Reset Mode**: Automatically restarts the board with a new random seed when stagnation or a stable loop is detected.
  - **Auto-Pause Mode**: Pauses generation when a loop is detected.
- **Interactive Editing**: Click or drag with mouse buttons while paused:
  - **Left Click**: Draw alive cells.
  - **Right Click**: Erase cells.
- **Runtime Controls**: Adjust FPS, change grid dimensions, toggle window scaling, and export screenshots.

## Prerequisites

- **Python 3.10 or higher** (Uses Python 3.10+ `match-case` syntax)
- Required Python libraries:
  - `pygame`
  - `numpy`
  - `tkinter` (usually bundled with standard Python distributions)

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/pygame-game-of-life.git
cd pygame-game-of-life
```
Or download directly `pygame-game-of-life.py`.

### 2. Install dependencies
```bash
pip install pygame numpy
```

### 3. Run the application
```bash
python pygame_of_life.py
```

## Controls & Keybindings

| Key | Action |
| :--- | :--- |
| **`Space`** | Toggle Pause / Resume |
| **`Enter`** | Advance to the next generation (when paused) |
| **`Left Mouse Click`** | Draw alive cells (when paused) |
| **`Right Mouse Click`** | Erase cells (when paused) |
| **`A`** | Toggle **Auto-Reset** mode (resets upon cycle detection) |
| **`Q`** | Toggle **Auto-Pause** mode (pauses upon cycle detection) |
| **`R`** | Generate a new random grid |
| **`C`** | Clear grid |
| **`S`** | Change Grid Size (width and height) |
| **`F`** | Change Target FPS (`0` = uncapped) |
| **`W`** | Toggle Screen Scaling Mode (`SCALED` / standard) |
| **`P`** | Save Screenshot (`screenshot.png`) |
| **`I`** | Show simulation Info (FPS, Generation, Flags) |
| **`H`** | Open Help dialog |

## Technical Highlights

1. **Vectorized Grid Logic (`NumPy`)**:
   Instead of iterating over individual cells with nested loops, neighbor counting is performed via array slicing with `np.pad(..., mode='wrap')`. This allows standard Game of Life rules to be evaluated instantly across large grids.
2. **Loop & Stagnation Detection**:
   The grid state is packed into compact bytes via `np.packbits().tobytes()` and hashed. Storing hash history enables constant time $O(1)$ loop detection to automatically trigger resets or pauses.
3. **Optimal Initial Density**: ($p = \frac{\sqrt{5}-1}{4} \approx 30.9\%$): To maximize dynamic evolution in B3/S23 Conway's rules, the initial state uses half the Golden Ratio. This value solves $\frac{d}{dp} P(k \in \{2,3\}) = 0$, reduced to $4p^2 + 2p - 1 = 0$, optimizing local cell transition activity while preventing rapid extinction or overpopulation saturation.

## License

This project is open-source and available under the [MIT License](LICENSE).
