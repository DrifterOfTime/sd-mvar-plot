from utils.modules import _IModule
import re
from itertools import chain
import numpy as np
import csv
from io import StringIO

def _parse_string(raw_values):
    return [x.strip() for x in chain.from_iterable(csv.reader(StringIO(raw_values)))]

def _parse_range(raw_values, re_range, re_count):
    valslist = _parse_string(raw_values)

    valslist_ext = []

    for val in valslist:
        m = re_range.fullmatch(val)
        mc = re_count.fullmatch(val)
        if m is not None:
            start = float(m.group(1))
            end = float(m.group(2))
            step = float(m.group(3)) if m.group(3) is not None else 1

            valslist_ext += np.arange(start, end + step, step).tolist()
        elif mc is not None:
            start = float(mc.group(1))
            end   = float(mc.group(2))
            num   = int(mc.group(3)) if mc.group(3) is not None else 1
            
            valslist_ext += np.linspace(start=start, stop=end, num=num).tolist()
        else:
            valslist_ext.append(val)

    return valslist_ext

class _IModuleInt(_IModule):
    def __init__(cls, raw_values):
        super().__init__(raw_values)
        cls._type = int

        cls._re_range = re.compile(r"\s*([+-]?\s*\d+)\s*-\s*([+-]?\s*\d+)(?:\s*\(([+-]\d+)\s*\))?\s*")
        cls._re_count = re.compile(r"\s*([+-]?\s*\d+)\s*-\s*([+-]?\s*\d+)(?:\s*\[(\d+)\s*\])?\s*")

    def _check(cls):
        is_valid = False
        value = cls._get_value
        try: is_valid = value == int(value)
        except: pass
        return is_valid

    def _format(cls):
        for v in cls._values:
            cls._labels.append(f"{cls.name}: {v}")

    def _parse(cls, raw_values):
        cls._values = _parse_range(raw_values, cls._re_range, cls._re_count)

class _IModuleFloat(_IModule):
    def __init__(cls, raw_values):
        super().__init__(raw_values)
        cls._type = float

        cls._re_range = re.compile(r"\s*([+-]?\s*\d+(?:.\d*)?)\s*-\s*([+-]?\s*\d+(?:.\d*)?)(?:\s*\(([+-]\d+(?:.\d*)?)\s*\))?\s*")
        cls._re_count = re.compile(r"\s*([+-]?\s*\d+(?:.\d*)?)\s*-\s*([+-]?\s*\d+(?:.\d*)?)(?:\s*\[(\d+(?:.\d*)?)\s*\])?\s*")

    def _check(cls):
        value = cls._get_value()
        try:
            value = float(value)
            return True
        except: pass
        return False

    def _format(cls):
        for v in cls._values:
            v = round(v, 8)
            cls._labels.append(f"{cls.name}: {v}")

    def _parse(cls, raw_values):
        cls._values = _parse_range(raw_values, cls._re_range, cls._re_count)

class _IModuleStr(_IModule):
    def __init__(cls, raw_values):
        super().__init__(raw_values)
        cls._type = str

    def _format(cls):
        cls.labels = cls.values

    def _parse(cls, raw_values):
        cls.values = _parse_string(raw_values)

class _IModuleOther(_IModule):
    pass