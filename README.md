# MVar Plot
Stable Diffusion MVar Plot script for Automatic1111's WebUI. Currently only the legacy script works, which is basically a simple XYZ script.

## Goals
Merge several different scripts into one:
- [x] XYZ script (i.e. my legacy script)
- [ ] Expanded XY Grid 
- [ ] Some features from Unprompted
    - [ ] Wildcard files (Want to implement this with the option to keep a certain wildcard across all generations in a grid. Rather difficult to do with Unprompted)

- [ ] Rework to use OOP for easy creation of new modules, should the need/desire arise. (Current priority. Nothing will work in the new script until this is done.)

- [ ] Add some simple shortcodes to act as a replacement for Expanded XY Grid's multitool.

- [ ] Expanded XY Grid's multitool will be the only available "mode", and every module will be run through that.

### Further Roadmap
- [ ] Hints/guides for using the different modules within the UI itself

