import abc

class _IModule(metaclass = abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, '_confirm') and 
                callable(subclass._confirm) and
                hasattr(subclass, '_format') and 
                callable(subclass.format) and
                hasattr(subclass, 'apply') and 
                callable(subclass.apply) or 
                NotImplemented)

    @abc.abstractmethod
    def _confirm(cls):
        """Confirm that the data is the proper type to pass to the generator"""
        raise NotImplementedError

    @abc.abstractmethod
    def format(cls):
        """Format the data into printable format (for grid annotations)"""
        raise NotImplementedError

    @abc.abstractmethod
    def apply(cls, i):
        """Apply the `i`th prompt/parameters to the generator"""
        raise NotImplementedError