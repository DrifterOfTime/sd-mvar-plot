import abc

class _IMVModule(metaclass = abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, '_parse') and 
                callable(subclass._parse) and 
                hasattr(subclass, '_confirm') and 
                callable(subclass._confirm) and
                hasattr(subclass, '_format') and 
                callable(subclass._format) and
                hasattr(subclass, 'apply') and 
                callable(subclass.apply) or 
                NotImplemented)

    @abc.abstractmethod
    def _parse(cls):
        """Parse the raw prompt text passed to the module"""
        raise NotImplementedError

    @abc.abstractmethod
    def _confirm(cls):
        """Confirm that the data is the proper type to pass to the generator"""
        raise NotImplementedError

    @abc.abstractmethod
    def _format(cls):
        """Format the data into printable format (for grid annotations)"""
        raise NotImplementedError

    @abc.abstractmethod
    def apply(cls, i):
        """Apply the `i`th prompt/parameters to the generator"""
        raise NotImplementedError