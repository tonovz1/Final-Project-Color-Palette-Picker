# Color Palette Picker for Digital Art

## Repository
https://github.com/tonovz1/Final-Project-Color-Palette-Picker.git

## Description
A Python-based color palette picker that lets users generate, explore, and export color palettes for use in digital art and media projects. 
It helps solve the common challenge of choosing visually pleasing color schemes by offering palette-generation tools for digital artists.

## Features
- Generate color palettes from a base color
	- Uses color theory rules (complementary, analogous, triadic, etc.) to compute harmonious palettes from a user-selected hex or RGB color.
- Display palettes visually in a GUI window
	- Uses `tkinter` or `pygame` to render colored swatches so users can preview the full palette at a glance.
- Copy individual color values to clipboard
	- Lets users click a swatch and copy its hex/RGB value, making it easy to bring colors into other tools.
- Save and export palettes to a file
	- Writes the palette's color values to a `.txt` or `.json` file so users can reference them in other projects.
- Random palette generator
	- Generates a completely random aesthetically pleasing palette using HSL/HSV color space constraints to avoid muddy or clashing colors.

## Challenges
- Learning how to work with color theory math (HSL, HSV, complementary angles) in Python.
- Building a functional GUI with `tkinter` or `pygame` for palette display and interaction.
- Figuring out how to access the system clipboard programmatically in Python.
- Understanding color space conversions between RGB, HEX, HSL, and HSV formats.

## Outcomes
Ideal Outcome:
- A fully interactive GUI app where users can input a base color, select a harmony rule, visually preview the generated palette with labeled swatches, copy individual values, and export the palette to a file.

Minimal Viable Outcome:
- A command-line program that takes a hex color as input, generates a basic complementary or analogous palette using color theory, and prints the resulting color values to the console or saves them to a file.

## Milestones

- Week 1
  1. Research color theory rules and implement hex/RGB/HSL conversion functions.
  2. Build logic to generate complementary, analogous, and triadic palettes from a base color.

- Week 2
  1. Create a basic GUI window that displays palette swatches using `tkinter`.
  2. Add click-to-copy functionality for individual color values.

- Week 3 (Final)
  1. Add random palette generation and file export feature.
  2. Polish the UI, test edge cases, and finalize the project for submission.
