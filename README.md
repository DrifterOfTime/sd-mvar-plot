# MVar Plot
Stable Diffusion MVar Plot script for Automatic1111's WebUI. Currently only the legacy script works, which is basically a simple XYZ script.

## Legacy Script Installation/Usage
Download `scripts/mvar_plot_legacy.py` and put it in `webui/scripts`.
Usage is the same as X/Y plot, except in addition to columns and rows, you can automatically produce multiple pages, too. Similar to the XYZ Script that already exists, but I did edit some extra things, such as making interrupting the script more efficient (especially noticable when using the Checkpoint Name module).

## Goals
Merge several different scripts into one:
- [x] XYZ script (i.e. my legacy script)
- [ ] Prompt Matrix
- [ ] Some features from Unprompted
    - [ ] Wildcard files (Want to implement this with the option to keep a certain wildcard across all generations in a grid. Rather difficult to do with Unprompted)

- [ ] Rework to use OOP for easy creation of new modules, should the need/desire arise. (Current priority. Nothing will work in the new script until this is done.)

- [ ] Add a configurable number of axes which can then be sorted into columns, rows, and pages (perhaps maybe folders, too)

- ~Add some simple shortcodes to act as a replacement for Expanded XY Grid's multitool.~

- ~Expanded XY Grid's multitool will be the only available "mode", and every module will be run through that.~

I no longer plan to implement the multitool. Trying to make a script with similar functionality but an easier to use interface.

### Further Roadmap
- [ ] Hints/guides for using the different modules within the UI itself

