# Game of Life (Pygame + Numba)

![Demo](demo.gif "Preview")

Conway’s Game of Life written in Python, using  
- **Pygame** for rendering & interaction  
- **Numba** for fast simulation  
- **OpenCV** for rendering bloom

## Features
- Click to draw cells (left = alive, right = erase)  
- Spacebar toggles simulation  
- Backspace clears the board  
- `E` steps one frame at a time  
- `P` toggles pretty rendering (rainbow + blur)  
- Scroll wheel changes brush size  

## How It Works
- Array is initialised once the program starts
- Mouse draws directly to the array 
- When simulating, one thread uses the current array state to calculate the new array state
- Another thread rasterises the current array state and masks it ontop of an RGB background + quarter res bloom pass (by default)
- At the end of the frame both threads are synced and array state is updated