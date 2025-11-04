# Dactyl Manuform - Personal Fork

This is my personal fork of the Dactyl Manuform keyboard generator, modified to my own tastes.

Based on [Wylderbuilds' fork](https://github.com/WyldeLLC/dactyl-keyboard), which itself is based on [joshreve's Python 3 adaptation](https://github.com/joshreve/dactyl-keyboard) of the original Clojure-based generator.

## Usage

To generate STL/STEP files:

```bash
python src/dactyl_manuform.py
```

Run this from the repository root. Generated files will be placed in the `things/` directory.

## Configuration

Edit `src/run_config.json` to configure the keyboard design. This is where you'll set parameters like:
- Number of rows/columns
- Thumb cluster style
- Plate style (standard, hotswap, etc.)
- Curvature and tenting
- Engine type (`"solid"` for OpenSCAD - recommended, `"cadquery"` for STEP/STL - bloated)
- `"export_outline": true` - Export 2D bottom outline as DXF for custom bottom plate designs (off by default because it's slow and you probably don't need it every iteration)

## Installation

Set up a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install numpy scipy solidpython dataclasses-json
```

## Support the Original Creator

If you find this generator useful, consider supporting joshreve (the original Python port creator):

[![Donate using Liberapay](https://liberapay.com/assets/widgets/donate.svg)](https://liberapay.com/joshreve/donate)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/K3K25ZIHR)

You can also purchase keyboards from [ergohaven](https://www.ergohaven.xyz/), which supports joshreve's work.

## License

General Code Copyright © 2015-2021 Matthew Adereth, Tom Short, and Joshua Shreve

The source code is distributed under the [GNU AFFERO GENERAL PUBLIC LICENSE Version 3](LICENSE). The generated models are distributed under the [Creative Commons Attribution-NonCommercial-ShareAlike License Version 3.0](LICENSE-models).
