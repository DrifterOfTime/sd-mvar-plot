from csv import reader
from io import StringIO
from numpy import split
import shortcodes

from _IParser import _IParser

def parse(cls, raw_prompt, type):
    split_prompt = reader(split('\n'),)
    pass

@_IParser.register
class Parser(_IParser):
    def process_raw_prompt(cls):
        pass