from _IMVParser import _IMVParser

@_IMVParser.register
class MVParserBase(_IMVParser):
    def parse(cls):
        pass