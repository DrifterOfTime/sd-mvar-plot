import csv
from itertools import chain, permutations
from modules.shared import opts, state
from io import StringIO

class IModule():
    """ Performs basic functionality shared across most modules

    Public Attributes:
        name: (`str`):
            Name used for module selection

    Public Methods:
        __len__(raw_values)
        __getitem__(index)
        get_label(index)

    """
    def __init__(cls, raw_values):
        cls.name = ""
        cls.__field = ""
        cls.__values = cls.__parse(raw_values)
        cls.__labels = cls.__format()

    def __len__(cls):
        return len(cls.__labels)

    def __getitem__(cls, index) -> function:
        """ Returns a function that applies value at `index` to `p`
            Call as `object[index](p)`
        """
        if index < len(cls):
            return lambda p: cls.__apply(p, index)
        else:
            raise IndexError("Index out of range")

    def get_label(cls, index):
        """ Returns the label for the value at `index`
        """
        if index < len(cls):
            return cls.__labels[index]
        else:
            raise IndexError("Index out of range")

    def __get_value(cls, index):
        """ Returns the value at `index`
        """
        if index < len(cls):
            return cls.__values[index]
        else:
            raise IndexError("Index out of range")

    def __check(cls, index) -> bool:
        """ Check if value at `index` is valid
            Returns True if successful
            Placeholder
        """
        return True

    def __format(cls) -> list(str):
        """ Turns the values into text suitable for printing on grids
            Placeholder
        """
        raise NotImplementedError("__format() not implemented")

    def __parse(cls):
        raise NotImplementedError("__parse() not implemented")

    def __apply(cls, p, index) -> bool:
        """ Default action: Applies the module's value at `index` to `__field` attribute in `p`
            Returns True if successful
        """
        is_processed = False
        if cls.__check():
            if cls.__field:
                setattr(p, cls.__field, cls[index])
                is_processed = True
            else: raise NotImplementedError("`apply()` requires a valid `__field` or custom implementation")
        return is_processed