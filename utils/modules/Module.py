import sys
print(sys.version)
print(sys.path)

from utils.modules._IModule import _IModule

from utils.ui.Element import _Element

@_IModule.register
class Module(_IModule):
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
        format(loop_index, options)
            Formats the values for pretty printing on an annotated grid.
    """
    
    label = "",
    field = "",
    value_type = float
    
    _parsed_field_values = []

    # def _confirm(cls):
    #     is_valid = False
    #     for value in cls._parsed_field_values:
    #         match cls.value_type:
    #             case int:
    #                 cls.                    
    #         if cls.value.type == float:
    #             is_valid = type(value) == int or type(value) == float
    #         if type(value) != cls.value_type:
    #             raise RuntimeError("{cls.label}: Values must be of type {value_type}")

    def apply(cls, p, loop_index):
        """ Applies the current field value to `cls.field` in p if there is one
        """
        if cls.field:
            setattr(p, cls.field, cls._parsed_field_values[loop_index])
        
    def format(cls, loop_index, options = {"label": ""}): 
        """ Formats floats to not be too long and adds a label if there is one
        """
        field_value = cls._parsed_field_values[loop_index]
        if type(field_value) == float:
            field_value = round(field_value, 8)

        label = options["label"]
        if label:
            return f"{label}: {field_value}"
        else:
            return f"{field_value}"

    def __init__(cls, raw_field_values):
        cls._parsed_field_values = Parser(raw_field_values)
        # cls._confirm(cls)