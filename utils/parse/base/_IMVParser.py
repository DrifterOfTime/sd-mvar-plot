import abc

class _IMVParser(metaclass = abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'parse') and 
                callable(subclass.parse) or
                NotImplemented)

    @abc.abstractmethod
    def parse(cls):
        """Parse text to a usable format"""
        raise NotImplementedError