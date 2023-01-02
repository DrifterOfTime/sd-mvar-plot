import sys

from collections import namedtuple
from copy import copy
from itertools import permutations, chain
import random
import csv
from io import StringIO
from PIL import Image, ImageFont, ImageDraw
from fonts.ttf import Roboto
import numpy as np

import modules.scripts as scripts
import gradio as gr

from modules import images, sd_samplers
from modules.hypernetworks import hypernetwork
from modules.processing import process_images, Processed, StableDiffusionProcessingTxt2Img
from modules.shared import opts, cmd_opts, state
import modules.shared as shared
import modules.sd_samplers
import modules.sd_models
import re

import modules.scripts as scripts

base_dir = scripts.basedir()
sys.path.append(base_dir)

try:
    from utils.modules.modules import *
except:
    print("MVar Plot not working", stream=sys.stderr)

def process_pages(p: StableDiffusionProcessingTxt2Img, col_modules: list(Module), row_modules: list(Module), page_modules: list(Module), cell, draw_legend: bool, include_lone_images: bool) -> Processed:
    """ Draw image grids on multiple images based on options chosen by the user

    Args:
        p (`StableDiffusionProcessingTxt2Img`)
        col_modules, row_modules, page_modules (`list(Module)`)
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
    image_cache = []

    processed_result = None
    cell_mode = "P"
    cell_size = (1,1)

    page_module_value_count = 0
    row_module_value_count = 0
    col_module_value_count = 0

    page_labels = []
    row_labels = []
    col_labels = []

    for page in page_modules:
        page_module_value_count += len(page.parsed_field_values)
        page_labels.append(page.value_labels)
    for row in row_modules:
        row_module_value_count += len(row.parsed_field_values)
        row_labels.append(row.value_labels)
    for col in page_modules:
        col_module_value_count += len(col.parsed_field_values)
        col_labels.append(col.value_labels)

    total_job_count = page_module_value_count * row_module_value_count * col_module_value_count
    state.job_count = total_job_count * p.n_iter

    current_job_count = 0

    for ipg, pg in enumerate(page_modules):
        for ipgv, pgv in enumerate(pg.parsed_field_values):
            for ir, r in enumerate(row_modules):
                for irv, rv in enumerate(r.parsed_field_values):
                    for ic, c in enumerate(col_modules):
                        for icv, cv in enumerate(c.parsed_field_values):
                            current_job_count += 1
                            state.job = f"{current_job_count} out of {total_job_count}"

                            processed:Processed = cell(cv, rv, pgv)

                            try:
                                # this dereference will throw an exception if the image was not processed
                                # (this happens in cases such as if the user stops the process from the UI)
                                processed_image = processed.images[0]
                                
                                if processed_result is None:
                                    # Use our first valid processed result as a template container to hold our full results
                                    processed_result = copy(processed)
                                    cell_mode = processed_image.mode
                                    cell_size = processed_image.size
                                    # Clear out that first image in case include_lone_images == False
                                    processed_result.images.clear()
                                    processed_result.all_prompts.clear()
                                    processed_result.all_seeds.clear()
                                    processed_result.infotexts.clear()

                                image_cache.append(processed_image)

                                if include_lone_images:
                                    processed_result.images.append(processed_image)
                                    processed_result.all_prompts.append(processed.prompt)
                                    processed_result.all_seeds.append(processed.seed)
                                    processed_result.infotexts.append(processed.infotexts[0])
                            except:
                                image_cache.append(Image.new(cell_mode, cell_size))

                            # Get out quick if interrupted
                            if state.interrupted: return processed_result

            grid = images.image_grid(image_cache, rows=len(row_module_value_count))
            image_cache.clear()

            if draw_legend:
                # Draw row and column labels
                grid = images.draw_grid_annotations(grid, cell_size[0], cell_size[1], col_labels, row_labels)

                # Draw page labels
                w, h = grid.size
                empty_string = [[images.GridAnnotation()]]
                grid = images.draw_grid_annotations(grid, w, h, [images.GridAnnotation(page_labels[ipg])], empty_string)

            processed_result.images.insert(ipg * page_module_value_count + ipgv, grid)

    if not processed_result:
        print("Unexpected error: `process_pages` failed to return even a single processed image")
        return Processed()

    return processed_result