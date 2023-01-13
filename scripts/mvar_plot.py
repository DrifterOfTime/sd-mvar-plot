import csv
import json
import random
import re
import sys
from collections import namedtuple
from copy import copy
from io import StringIO
from itertools import chain, permutations, product

import gradio as gr
import modules.scripts as scripts
import modules.sd_models
import modules.sd_samplers
import modules.shared as shared
import numpy as np
from fonts.ttf import Roboto
from modules import images, sd_samplers
from modules.hypernetworks import hypernetwork
from modules.processing import (Processed, StableDiffusionProcessingTxt2Img,
                                process_images)
from modules.shared import cmd_opts, opts, state
from PIL import Image, ImageDraw, ImageFont

base_dir = scripts.basedir()
sys.path.append(base_dir)

import utils.modules as mods

def parse(raw_prompt):
    return []

class Script(scripts.Script):
    def title(cls):
        return "MVar Plot"

    def ui(cls, is_img2img):

        col_modules = col_values = row_modules = row_values = page_modules = page_values = []

        for i in range(num_col_modules):
            with gr.Row():
                col_modules.append(gr.Dropdown(label=f"Col Module {i}", choices=[c.label for c in current_axis_options], value=current_axis_options[1].label, type="index", elem_id=f"c_type_{i}"))
                col_values.append(gr.Textbox(label=f"Col Values {i}", lines=1))

        for j in range(num_row_modules):
            with gr.Row():
                row_modules.append(gr.Dropdown(label=f"Row Module {j}", choices=[r.label for r in current_axis_options], value=current_axis_options[0].label, type="index", elem_id=f"r_type_{j}"))
                row_values.append(gr.Textbox(label=f"Row Values {j}", lines=1))

        for k in range(num_page_modules):
            with gr.Row():
                page_modules.append(gr.Dropdown(label=f"Page Module {k}", choices=[pg.label for pg in current_axis_options], value=current_axis_options[0].label, type="index", elem_id=f"pg_type_{k}"))
                page_values.append(gr.Textbox(label=f"Page Values {k}", lines=1))
        
        draw_legend = gr.Checkbox(label='Draw legend', value=True)
        include_lone_images = gr.Checkbox(label='Include Separate Images', value=False)
        no_fixed_seeds = gr.Checkbox(label='Keep -1 for seeds', value=False)

        return [col_modules, col_values, row_modules, row_values, page_modules, page_values, draw_legend, include_lone_images, no_fixed_seeds]

    def run(cls, p:StableDiffusionProcessingTxt2Img, axes_raw_prompts, draw_legend, include_lone_images, no_fixed_seeds):

        processed_result = None
        cell_mode = "P"
        cell_size = (1,1)

        axes = []
        total_job_count = 1

        for i, axis_raw_prompt in enumerate(axes_raw_prompts):
            axes[i] = parse(axis_raw_prompt)
            total_job_count *= len(axes[i])

        state.job_count = total_job_count * p.n_iter

        def process_and_draw():

            def process_cell(pc:StableDiffusionProcessingTxt2Img, current_axes:list(mods._IModule), current_axis_value_indeces):
                """ Process designated cell image.

                Args:
                    pc (`StableDiffusionProcessingTxt2Img`):
                        This function is passed a copy of `p`
                    col, row, page (`mods.Module`):
                        The current module to be processed
                    icolv, irowv, ipagev (`int`)
                        The index of the current value of the module to be processed
                """
                for axis_index, axis in enumerate(current_axes):
                    axis.apply(pc, current_axis_value_indeces[axis_index])

                processed = process_images(pc)

                try:
                    # this dereference will throw an exception if the image was not processed
                    # (this happens in cases such as if the user stops the process from the UI)
                    cell_mode = processed.images[0].mode
                    cell_size = processed.images[0].size

                    if include_lone_images:
                        image_cache.add(proc = processed)
                except:
                    image_cache.add(image = Image.new(cell_mode, cell_size))

            def draw_page() -> Processed:
                """ Draw image grids on multiple images based on options chosen by the user

                Args:
                    p (`StableDiffusionProcessingTxt2Img`)
                    col_modules, row_modules, page_modules (`list(mods.Module)`)
                    draw_legend (`bool`):
                        Whether to draw labels on grid
                    include_lone_images (`bool`)
                        Whether to save individual images

                Returns: (processed_result)
                    result (`Processed`):
                        Processed images
                """

                # Temporary list of all the images that are generated to be populated into each grid.
                # Will be filled with empty images for any individual step that fails to process properly.
                # Cleared after each grid generation.
                
                if not processed_result:
                    print("Unexpected error: `process_pages` failed to return even a single processed image")
                    return Processed()

                return processed_result

            current_modules = []
            current_indeces = []

            def loop():

                for axis_modules_index, axis in enumerate(axes):
                    for module_index, module in enumerate(axis):
                        current_modules.append(module)
                        current_indeces.append(0)
                        for axis_value_index, axis_value in enumerate(module.parsed_values):
                            if not module.check(axis_value_index):
                                print(f"Module `{module.label}` with value `{axis_value}` failed check")
                            else:
                                # Process current cell
                                if len(current_modules) == len(axes):
                                    pc = copy(p)
                                    process_cell(pc, current_modules, current_indeces)
                                    if current_indeces[len(current_indeces)] == len(module.parsed_values):
                                        return

                                # Draw pages after processing columns and rows
                                elif len(current_modules) == len(axes)-2:
                                    draw_page()

                            current_indeces[module_index] += 1
                            loop()





                    match mode:
                        case "col":
                            for icol, col in enumerate(col_modules):
                                if not col.check(icol):
                                    print(f"Failed check for column {icol}")
                                else:
                                    pc = copy(p)
                                    for icolv, colv in enumerate(col.parsed_field_values):
                                        process_cell(pc=pc, current_axes = [col, row, page], icolv=icolv, irowv=irowr, ipagev=ipager)
                                        if state.interrupted: break
                                if state.interrupted: break
                        case "row":
                            for irow, row in enumerate(row_modules):
                                for irowv, rowv in enumerate(row.parsed_field_values):
                                    if not row.check(irow):
                                        print(f"Failed check for row {irow}")
                                    else:
                                        loop_inner("col", irowv, ipager)
                                        if state.interrupted: break
                                if state.interrupted: break
                        case "page":
                            for ipage, page in enumerate(page_modules):
                                for ipagev, pagev in enumerate(page.parsed_field_values):
                                    if not page.check(ipagev):
                                        print(f"Failed check for page {ipage}")
                                    else:
                                        loop_inner("row", 0, ipagev)
                                        if state.interrupted: break
                                grid = images.image_grid(image_cache, rows=len(row_module_value_count))
                                image_cache.clear()

                                if draw_legend:
                                    # Draw row and column labels
                                    grid = images.draw_grid_annotations(grid, cell_size[0], cell_size[1], col_labels, row_labels)

                                    # Draw page label
                                    w, h = grid.size
                                    empty_string = [[images.GridAnnotation()]]
                                    grid = images.draw_grid_annotations(grid, w, h, [images.GridAnnotation(page_labels[ipage])], empty_string)

                                processed_result.images.insert(ipage * page_module_value_count + ipagev, grid)
                                processed_result.all_prompts.insert(ipage * page_module_value_count + ipagev, "")
                                processed_result.all_seeds.insert(ipage * page_module_value_count + ipagev, -1)
                                processed_result.infotexts.insert(ipage * page_module_value_count + ipagev, "")

                                if state.interrupted: break

                loop_inner()
