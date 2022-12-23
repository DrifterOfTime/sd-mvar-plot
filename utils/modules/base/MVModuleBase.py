import sys
print(sys.version)
print(sys.path)

from . _IMVModule import _IMVModule

@_IMVModule.register
class MVModuleBase(_IMVModule):
    """Performs basic functionality shared across all modules
    """
    
    label = "",
    rawPrompt = ""
    processedPrompt = [""]
    formattedPrompt = ""
    field = ""

    def setLabel(cls, label=""):
        cls.label = label

    def setField(cls, field=""):
        cls.field = field

    def _parse(cls): pass
    def _process(cls): pass
    def _confirm(cls): pass

    def apply(cls, i):
        setattr(cls.options.field, cls.processedPrompt[i])

    def format(cls, label = True): 
        if type(value) == float:
            value = round(value, 8)
        if label:
            return f"{cls.moduleOptions.label}: {value}"
        else:
            return value


    def __init__(cls, rawPrompt):
        cls.rawPrompt = rawPrompt

        cls.parse(cls)
        cls.process(cls)
        cls.confirm(cls)

        return cls.format(cls)