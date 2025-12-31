Copilot guide for this repository

Purpose
-------
This short guide helps you (and GitHub Copilot) work effectively with the "Cat Attack" Python project in this repository. It includes quick run instructions, useful contextual notes, and example prompts you can use with Copilot (or with any AI coding assistant) to generate code, tests, or fixes.

Quick project summary
---------------------
- Language: Python 3.x
- UI: pygame
- Entry point: `Main.py`
- Assets: images in `animals/`, background in `images/`, sounds in `sound/`

Run locally
-----------
1. Create and activate a Python 3 virtual environment.

   powershell:
   python -m venv .venv; .\.venv\Scripts\Activate.ps1

2. Install dependencies (minimal):

   powershell:
   pip install -r requirements.txt

3. Start the game:

   powershell:
   python Main.py

Notes: If you get pygame import errors, install a compatible pygame wheel for your Python version.

Context for Copilot
-------------------
When asking Copilot (or any assistant) to change code in this repo, provide these contextual hints to get accurate results:
- The game's main loop and input handling are in `Main.py`.
- Game piece classes live in the root files `Cat.py`, `Dog.py`, `Monkey.py`, `Panda.py`, `Sheep.py`, `SheepZombie.py`, and `Blank.py`.
- Images are loaded from the `animals/` folder using names like `cat_blue_128.png` and their "active" variants `*_active.png`.
- Sounds live in `sound/` and are loaded with `pygame.mixer.music.load(...)`.
- Board positions are strings like `"a1"` and map to array indices via `getPositionInArray` and pixel positions via `getPositionInPixels`.

Common patterns and pitfalls (useful to mention in prompts)
---------------------------------------------------------
- Many methods compare strings like `piece.name == "cat"`. Keep string constants consistent.
- `gameboard` is a dict with keys `(x, y)` -> piece object.
- Piece objects expose attributes like `color`, `name`, `icon`, `position`, `isActive` and a method `availableMoves(fromArray, toArray)`.
- Some parts of the code use string booleans (for example `piece.isActive == "true"`) rather than Python booleans — be careful if you change these to bools globally.
- There are a couple of small inconsistencies in `Main.py` (for example, a `Dog` created for a blue cage uses `Dog("red", ...)` and an icon name missing an underscore). If you ask Copilot to search/repair, point out those expected fixes.

Suggested Copilot prompts
-------------------------
- "Add a unit test that verifies `getPositionInArray('b2')` returns `(1, 1)` and `getPositionInPixels('b2')` returns the expected pixel tuple. Use pytest."
- "Refactor `Main.py` to use Python booleans for `isActive` (True/False) instead of string values, update all code and tests accordingly." (ask for a small, incremental change)
- "Find and fix any places where a Dog for the blue cage is created with the wrong color or icon name — show a small patch." (point out the file and near the `freeAnimalFromCage` method)
- "Add defensive checks around loading assets with pygame.image.load(...) so the game fails gracefully if an image or sound file is missing."
- "Extract constants for magic numbers in `Main.py` (screen coordinates, tile size) and use them to compute positions so the board can be resized easily." 

Example short prompt you can paste to Copilot
--------------------------------------------
"In `Main.py`, `freeAnimalFromCage` creates a Dog for the blue cage using `Dog('red', ... 'dog_blue128', ...)`. Fix the color to `'blue'` and the icon name to `'dog_blue_128'`. Make a minimal change and update any dependent code if necessary. Provide only the file edits." 

Best practices when accepting Copilot suggestions
------------------------------------------------
- Review changes locally: run `python -m pyflakes Main.py` or a linter to catch syntax/name errors.
- Run the game after changes to confirm runtime behavior (audio and images load properly).
- For UI changes, keep the original coordinates/spacing in mind: many pixel values are hard-coded.

Small maintenance checklist to improve Copilot outcomes
-----------------------------------------------------
- Standardize `isActive` to a boolean across all Piece classes and `Main.py`.
- Replace string-based board coordinates (e.g., "a1") with a small Position helper or consistent mapping functions.
- Add a small test suite using pytest to guard movement rules (happy path + a couple edge cases).
- Add a simple script `scripts/verify_assets.py` that scans `animals/` and `sound/` for expected files and prints missing ones.

If you'd like, I can:
- Create the `COPILOT.md` (this file) — done.
- Open a PR that fixes the blue-dog creation bug in `Main.py` (small, low risk).
- Add a quick `scripts/verify_assets.py` that checks for missing assets.
- Add 2-3 pytest tests for `getPositionInArray` and piece movement.

Tell me which of the follow-ups you'd like and I will implement it next:
- Fix the blue-dog cage bug in `Main.py`.
- Add `scripts/verify_assets.py`.
- Add pytest tests for position mapping and one piece's movement.
- Convert `isActive` to booleans across the codebase.


Notes
-----
This file is intentionally lightweight and meant to be used as a Copilot prompt reference. Keep it in the repo root so Copilot and collaborators can easily see recommended prompts and the run steps.

