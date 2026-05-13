🎮 Spot the Difference
HIT137 Group Assignment 3 — CDU

A desktop puzzle game built with Python, Tkinter, and OpenCV. Load any photo, hunt down 5 hidden differences, and race against the clock — no two rounds are ever the same.


Table of Contents

Demo & Screenshots
Features
How to Contribute
Tech Stack
Project Structure
Architecture Overview
OOP Concepts Demonstrated
Installation
Usage
Game Rules
Known Issues & Limitations
Roadmap / Future Ideas


Demo & Screenshots

Add a GIF or screenshot of the running app here. (e.g. docs/demo.gif)

📂 Load Image  →  Study both panels  →  Click differences on the right  →  Win!

Features
FeatureDetails🖼 Universal image supportJPG, PNG, BMP, TIFF, WEBP🎲 Randomised puzzles5 non-overlapping regions placed fresh each round🎨 11 visual effectsColour shift, blur, brightness, shape, border, invert, grayscale, pixelate, noise, dark patch, Canny edge🖱 Click-to-guessTolerance-based hit detection on the modified image📊 Live HUDScore, elapsed timer, mistake counter — all updated in real time❌ Mistake limit3 wrong clicks locks the round👁 Reveal buttonShows all remaining differences at any time✨ AnimationsPop (✓) and shake (✕) feedback on every click🔊 Audio cuesBeep tones on Windows via winsound (no extra install required)🌑 Dark UI themeStyled with #1e1e2f background and neon accent colours

How to Contribute
All contributions are welcome! This section covers everything you need to get started.
Quick-Start Contribution Flow
Fork → Clone → Branch → Code → Test → PR
1. Fork & Clone
bashgit clone https://github.com/<your-username>/HIT137-Assignment-3-CDU.git
cd HIT137-Assignment-3-CDU
2. Create a Feature Branch
Use a descriptive name so your intent is clear:
bashgit checkout -b feature/add-difficulty-levels
# or
git checkout -b fix/timer-reset-on-reload
# or
git checkout -b docs/improve-readme
Branch naming conventions:
PrefixUse forfeature/New functionalityfix/Bug fixesrefactor/Code cleanup with no behaviour changedocs/Documentation onlytest/Adding or fixing tests
3. Set Up Your Environment
bashpython -m venv venv
source venv/bin/activate          # macOS / Linux
venv\Scripts\activate             # Windows

pip install -r requirements.txt
4. Make Your Changes
The whole game lives in spot_difference_app.py — one file, six classes. See Architecture Overview to understand where things go.
Adding a new visual effect (the most beginner-friendly contribution):
python# 1. Create a class that inherits from DifferenceEffect
class SepiaEffect(DifferenceEffect):
    def apply(self, image, region):
        x, y, w, h = region
        roi = image[y:y+h, x:x+w].astype(np.float32)
        sepia_filter = np.array([[0.272, 0.534, 0.131],
                                  [0.349, 0.686, 0.168],
                                  [0.393, 0.769, 0.189]])
        sepia = np.clip(roi @ sepia_filter.T, 0, 255).astype(np.uint8)
        image[y:y+h, x:x+w] = sepia

# 2. Register it in ImageProcessor.__init__
self.effects = [
    ...,
    SepiaEffect(),   # ← add here
]
No other changes needed — the rest of the game picks it up automatically.
5. Test Your Changes
Run the app manually and verify your change works end-to-end:
bashpython spot_difference_app.py
Checklist before submitting:

 App starts without errors
 Loading an image works
 Clicking correct/incorrect regions updates score and HUD
 Reveal Differences shows all remaining regions
 Your new code has no syntax errors or obvious regressions
 Code is commented where non-obvious

6. Commit & Push
bashgit add .
git commit -m "feat: add sepia visual effect"
git push origin feature/add-sepia-effect
Commit message format:
<type>: <short description>

Types: feat | fix | refactor | docs | style | test | chore
7. Open a Pull Request
Go to the original repo on GitHub → Compare & pull request.
In your PR description, include:

What you changed and why
Steps to test it
Screenshots or a GIF if it's visual


Contribution Ideas
Not sure what to work on? Here are some ideas ranked by difficulty:
🟢 Beginner

Add a new visual effect (see template above)
Improve error messages or UI copy
Add comments / docstrings to undocumented methods
Fix code style inconsistencies (indentation, spacing in spot_difference_app.py)

🟡 Intermediate

Add difficulty levels (Easy = 3 diffs / fewer effects, Hard = 7 diffs / more subtle effects)
Add a high-score leaderboard stored in a local JSON file
Cross-platform audio support (replace winsound with playsound or pygame.mixer)
Add a hint system (briefly flash the region location)
Allow the number of differences and mistake limit to be configurable via a settings dialog

🔴 Advanced

Add a multiplayer mode (two windows, first to find all differences wins)
Generate a report/summary PDF after each round
Add unit tests using pytest for DifferenceGame and DifferenceRegion
Implement an auto-image fetch mode (pull random public-domain images from an API)


Tech Stack
LibraryVersionPurposePython3.8+Core languageTkinterstdlibDesktop GUIOpenCV (cv2)≥ 4.5Image processing & effectsNumPy≥ 1.21Array operations for pixel manipulationPillow≥ 9.0Bridge between OpenCV and Tkinter image formatswinsoundstdlib (Windows)Audio feedback beeps

Project Structure
HIT137-Assignment-3-CDU/
├── spot_difference_app.py   # Entire application — all classes in one file
├── requirements.txt         # pip dependencies
├── README.md
└── .gitignore

Architecture Overview
SpotDifferenceApp  (GUI layer — Tkinter)
    │
    ├── ImageProcessor         (image loading, effect application, display conversion)
    │       └── DifferenceEffect  (abstract base)
    │               ├── ColourShiftEffect
    │               ├── BlurEffect
    │               ├── BrightnessEffect
    │               ├── ShapeEffect
    │               ├── BorderEffect
    │               ├── InvertEffect
    │               ├── GrayEffect
    │               ├── PixelateEffect
    │               ├── NoiseEffect
    │               ├── DarkPatchEffect
    │               └── CannyEdgeEffect
    │
    ├── DifferenceGame         (game state — score, mistakes, click validation)
    │
    └── DifferenceRegion       (position + found-state of each hidden difference)
Class Responsibilities
ClassResponsibilityDifferenceEffectAbstract base; defines apply(image, region) interface*Effect subclassesEach implements one visual transformationDifferenceRegionStores bounding box & found status; checks if a click lands inside itImageProcessorLoads images, generates non-overlapping regions, applies effects, resizes for displayDifferenceGameTracks score, mistake count, locked state; validates clicksSpotDifferenceAppBuilds the Tkinter GUI, runs the timer loop, wires events to game logic

OOP Concepts Demonstrated

Inheritance — every effect class extends DifferenceEffect
Polymorphism — effect.apply() is called uniformly regardless of which effect is chosen
Encapsulation — DifferenceRegion uses private attributes (__x, __y, etc.) with public getters
Abstraction — DifferenceGame.check_click() hides click-validation logic from the GUI; ImageProcessor hides all OpenCV details


Installation
bash# 1. Clone the repo
git clone https://github.com/thanetindru934/HIT137-Assignment-3-CDU.git
cd HIT137-Assignment-3-CDU

# 2. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate       # macOS / Linux
venv\Scripts\activate          # Windows

# 3. Install dependencies
pip install -r requirements.txt

Linux only: If Tkinter is not bundled with your Python installation:
bashsudo apt-get install python3-tk


Usage
bashpython spot_difference_app.py

Click Load Image and select any photo from your computer
Study the Original Image (left) and Modified Image (right) side by side
Click on spots you think differ in the right panel
Find all 5 differences before making 3 mistakes
Use Reveal Differences if you get stuck


Game Rules
RuleValueDifferences per round5Points for correct guess+10Points deducted for wrong guess−5 (floor: 0)Maximum mistakes before lockout3Click tolerance radius20 px (scaled)

Known Issues & Limitations

Audio feedback (winsound) works on Windows only. On macOS/Linux the game is silent.
Very small images (< ~150 × 150 px) may fail to generate 5 non-overlapping regions.
No persistent high-score storage between sessions.
The app is not resizable in a fully responsive way — images are capped at 600 × 450 px.


Roadmap / Future Ideas

 Cross-platform sound support
 Difficulty selector (Easy / Medium / Hard)
 Hint system
 High-score leaderboard (local JSON)
 Unit tests for game logic
 Configurable number of differences and mistake limit
 Packaging as a standalone .exe / .app


License
This project was created for academic purposes as part of HIT137 — Software Now at Charles Darwin University. No licence has been applied; please check with the authors before reuse.

Authors
HIT137 Group — Charles Darwin University, 2026
