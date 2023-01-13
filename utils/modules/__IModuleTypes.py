import csv
import re
from io import StringIO
from itertools import chain

import numpy as np

from utils.modules import IModule

def __parse_string(raw_values):
    return [x.strip() for x in chain.from_iterable(csv.reader(StringIO(raw_values)))]

def __parse_range(raw_values, re_range, re_count):
    valslist = __parse_string(raw_values)

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

class IModuleInt(IModule):
    def __init__(cls, raw_values):
        super().__init__(raw_values)

        cls._re_range = re.compile(r"\s*([+-]?\s*\d+)\s*-\s*([+-]?\s*\d+)(?:\s*\(([+-]\d+)\s*\))?\s*")
        cls._re_count = re.compile(r"\s*([+-]?\s*\d+)\s*-\s*([+-]?\s*\d+)(?:\s*\[(\d+)\s*\])?\s*")

    def _check(cls, index):
        is_valid = False
        value = cls.get_label(index)
        try: is_valid = value == int(value)
        except: pass
        return is_valid

    def __format(cls):
        for v in cls.__values:
            cls.__labels.append(f"{cls.name}: {v}")

    def _parse(cls, raw_values):
        cls.__values = __parse_range(raw_values, cls._re_range, cls._re_count)
        for i, v in enumerate(cls._values):
            cls._values[i] = round(v)

class IModuleFloat(IModule):
    def __init__(cls, raw_values):
        super().__init__(raw_values)

        cls._re_range = re.compile(r"\s*([+-]?\s*\d+(?:.\d*)?)\s*-\s*([+-]?\s*\d+(?:.\d*)?)(?:\s*\(([+-]\d+(?:.\d*)?)\s*\))?\s*")
        cls._re_count = re.compile(r"\s*([+-]?\s*\d+(?:.\d*)?)\s*-\s*([+-]?\s*\d+(?:.\d*)?)(?:\s*\[(\d+(?:.\d*)?)\s*\])?\s*")

    def __check(cls, index):
        value = cls._get_value(index)
        try:
            value = float(value)
            return True
        except: pass
        return False

    def __format(cls):
        for v in cls._values:
            v = round(v, 8)
            cls._labels.append(f"{cls.name}: {v}")

    def _parse(cls, raw_values):
        cls._values = __parse_range(raw_values, cls._re_range, cls._re_count)

class IModuleStr(IModule):
    def __init__(cls, raw_values):
        super().__init__(raw_values)

    def __format(cls):
        cls._labels = cls._values

    def _parse(cls, raw_values):
        cls._values = __parse_string(raw_values)

class IModuleOther(IModule):
    pass