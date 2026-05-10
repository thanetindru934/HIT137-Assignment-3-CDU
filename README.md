# 🎮 Spot the Difference — HIT137 Group Assignment 3

A desktop game built with Python, Tkinter, and OpenCV where players find hidden differences between two side-by-side images.

---

## Features

- Load any image (JPG, PNG, BMP, TIFF, WEBP) to generate a unique puzzle
- 5 randomly placed, non-overlapping differences applied per round
- 10 visual effect types: colour shift, blur, brightness, shape, border, invert, grayscale, pixelate, noise, dark patch
- Click-to-guess on the modified image with tolerance-based hit detection
- Live score (+10 correct, -5 wrong, minimum 0) and elapsed timer
- 3-mistake limit before the round locks
- Reveal all differences at any time
- Visual feedback animations (✓ / ✕) on clicks
- Audio feedback on Windows via `winsound` (no extra install needed)

---

## Requirements

- Python 3.8 or later
- See `requirements.txt` for dependencies

---

## Installation

```bash
# 1. Clone or download the project
git clone https://github.com/thanetindru934/HIT137-Assignment-3-CDU/
cd spot-the-difference

# 2. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate          # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

> **Note:** Tkinter is bundled with most Python distributions. If it's missing on Linux, run:
> ```bash
> sudo apt-get install python3-tk
> ```

---

## Usage

```bash
python spot_the_difference.py
```

1. Click **Load Image** and select any photo
2. Study both images side by side
3. Click on differences you spot in the **right (modified) image**
4. Find all 5 before making 3 mistakes
5. Use **Reveal Differences** if you get stuck

---

## Project Structure

```
spot-the-difference/
├── spot_the_difference.py   # Main application (single file)
├── requirements.txt
└── README.md
```

### Key Classes

| Class | Role |
|---|---|
| `DifferenceEffect` | Abstract base class for all effects (polymorphism) |
| `ColourShiftEffect`, `BlurEffect`, `BrightnessEffect`, `ShapeEffect`, `BorderEffect`, `InvertEffect`, `GrayEffect`, `PixelateEffect`, `NoiseEffect`, `DarkPatchEffect` | Concrete effect implementations |
| `DifferenceRegion` | Stores position and found-state of each hidden difference |
| `ImageProcessor` | Loads images, generates regions, applies effects, handles display conversion |
| `DifferenceGame` | Manages game state — score, mistakes, click validation, reveal |
| `SpotDifferenceApp` | Tkinter GUI — layout, events, timer, feedback animations |

---

## OOP Concepts Demonstrated

- **Inheritance** — all effect classes extend `DifferenceEffect`
- **Polymorphism** — `effect.apply()` called uniformly across all effect types
- **Encapsulation** — `DifferenceRegion` uses private attributes with getters
- **Abstraction** — `DifferenceGame` hides click-checking logic from the GUI layer

---


