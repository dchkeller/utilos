
import logging
import re

from .Parameter import Parameter

_logger = logging.getLogger( "utilos.HasParameters" )

class HasParameters :
    """ a base class with parameters
    
        creates a proper init
        define class attributes as required in your derived class in the form
        class MyDerived( HasParameters ) :
            param1 = Parameter( comment="Explanation of Parameter 1", default=False )
            param2 = Parameter( comment="Explanation of Parameter 2", default=5 )
        
        The init function added will look like:
        def __init__( param1 = param1.default, param2 = param2.default )
        
        The docstring for this init function will contain the comments from param1 and param2.
        
        Additionaly, this class has a registry for all derived types.
        This allows for loading and constructing from str.
    """
    
    """ static dict containing all registered class names inheriting from here """
    _registered_types = {}
    
    def __init_subclass__( cls, **kwargs ) :
        """ define an __init__ and docstring based on the parameters defined """
        _logger.debug( "registering class %s" % cls )
        
        def __init__( self, **kwargs ) :
            for p in self._params.keys() :
                if p in kwargs :
                    setattr( self, p, kwargs.get(p) )
                    
        super().__init_subclass__(**kwargs)
        
        doc = "Initialize from parameters\n\nParameters:\n"
        for n, p in cls._params.items() :
            doc = doc + n + " :\t" + p.comment + "\n"
        
        __init__.__doc__ = doc
        cls.__init__ = __init__
        
        cls._name = cls.__name__.split(".")[-1]
        HasParameters._registered_types[cls._name] = cls

    
    def dumps( self ) :
        """ returns a string representation of this class as it is typically part of config or ini-files
            
            [<name>]
            param1 = value1 # comment (default=d1)
            param2 = value2 # comment (default=d2)
            
            
        """
        res = "[%s]\n" % self._name
        for n, p in self._params.items() :
            res += p.dumps() + "\n"
        return res
    
    @staticmethod
    def loads( config ):
        """ load from a string like the one returned by dumps """
        # split the input to lines
        lines = config.splitlines(False)
        # the first line is supposed to be of the form '[name]'
        r = re.compile( r"^\s*\[(?P<cls_name>\w+)\]\s*" )
        m = r.match( lines[0] )
        assert m is not None
        cls_name = m.groups()[0]
        # construct the class
        obj_type = HasParameters._registered_types[cls_name]
        obj = obj_type()
        # load the params
        for l in lines[1:] :
            p = Parameter.loads( l )
            obj._params[p.name] = p
        return obj