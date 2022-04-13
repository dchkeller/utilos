


import logging
import re
import json

_logger = logging.getLogger( "utilos.Parameter" )

class Parameter :
    """ a parameter class
    
        Has the following properties
        * a value
        * a name
        * a comment
        * a default value
        
        A parameter can be written to string an read from a string.
        This function uses json internally to encode and decode value and default.
        See json-Documentation for further details.
    """
    
    def __init__( self, name=None, value=None, comment="", default=None ) :
        self.name = name
        self.value = value
        self.comment = comment
        self.default = default
        
        if self.value is None :
            self.value = self.default
    
    def reset( self ) :
        """ reset the value to default  """
        self.value = self.default
    
    def __repr__( self ) :
        """ returns a simple representation as a string """
        return "Parameter( value=%s, name=%s )" % (self.value, self.name)
    
    def _dump_value( self, value ) :
        """ This function is called from dumps to translate value to a string representation
        
            You can overload this function if desired to define the way the parameter
            translates value to a string
            
            Returns:
            str : a translation of value to a string
        """
        return json.dumps( value )
    
    def dumps( self ) :
        """ returns a string representation as it is typically used in config-files
        
            Returns:
            str : '<name> = <self._dump_value( self.value )> # <comment> (default=<self._dump_value( self.default )>)'
        """
        return "%s = %s    # %s (default=%s)" % (self.name, self._dump_value( self.value ), self.comment, self._dump_value( self.default ) )
    
    @staticmethod
    def _load_value( s ) :
        """ This function is called from loads to translate a string to a value/default
        
            You can overload this function if desired to define the way the parameter
            translates string to value.
            
            Returns:
            any : a translation of string to a value
        """
        return json.loads( s )
    
    
    @staticmethod
    def loads( s ) :
        """ load a parameters from a string like the one returned by dumps 
        
            Intentioned use-case is loading ini or config-files with parameters.
            
            
            Parameters:
            s : string-like object containing a dump of a parameter of the form 
                "<name> = <value> # comment (default=<default>)"
            
            Returns:
            a Parameter object
        """
        r = re.compile( r"^(?P<name>\w*)\s*=\s*(?P<value>.*)\s*\#\s*(?P<comment>.*)\s+\(default\s*=\s*(?P<default>.*)\s*\)\s*$" )
        m = r.match( s )
        if m :
            d = m.groupdict()
            return Parameter( name=d["name"], 
                             value=Parameter._load_value(d["value"]), 
                             comment=d["comment"], 
                             default=Parameter._load_value(d["default"]) )
         
    def __set_name__( self, owner, name ) :
        """ descriptor access to set name of a param """
        _logger.debug( "%s.__set_name__" % self )
        self.name = name
        if not hasattr( owner, "_params" ) :
            owner._params = dict()
        owner._params[name] = self
    
    def __get__( self, obj, objtype=None ) :
        """ descriptor access to value of a param """
        _logger.debug( "accessing %s.value" % self )
        return self.value
    
    def __set__( self, obj, value ) :
        """ descriptor access to set value of a param """
        _logger.debug( "setting %s.value=%s" % (self, value))
        self.value = value

