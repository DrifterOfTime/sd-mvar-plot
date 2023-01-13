import csv
from itertools import chain, permutations
from modules.shared import opts, state
from io import StringIO

class _IModule():
    """ Performs basic functionality shared across most modules

    Public Attributes:
        label: (`str`):
            Label used for module selection
        field: (`str`):
            Field to apply a parsed field value to in a `StableDiffusionProcessingTxt2Img` object
        value_type: (`type`):
            If field has a specified value type, this is it

    Public Methods:
        apply(p, loop_index):
            Applies the current field value to `cls.field` in p
        check(loop_index, options)
            Checks if the values are valid.
    """

    def _check(cls):
        return True

    def _format(cls):
        pass

    def _parse(cls):
        return []

    def _get_value(cls):
        return cls._values[cls._current_index]

    def apply(cls, p):
        """ Applies the current field value to `cls.field` in `p` if there is one
        """
        if cls._check():
            if cls._field:
                setattr(p, cls._field, cls._get_value)
                return True
            else: raise NotImplementedError("`apply()` requires a valid `_field` or custom implementation")
        return False

    def __init__(cls, raw_values):
        cls.name = ""
        cls._current_index = 0
        cls._field = ""
        cls._labels = []
        cls._values = cls._parse(raw_values)
        cls._format()