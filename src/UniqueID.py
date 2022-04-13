import itertools


class HasUniqueID :
    """ a class with a unique ID 
    
        contains a property called unique_id
        unique_id returns an int which is unique over all instances
        unique_id cannot be set by the user
    """

    """ an iterator to make a unique number in every instance """
    _uid_iter = itertools.count()
    
    def __init__( self ) :
        """ set _unique_id in init """
        self._unique_id = next(self._uid_iter)
        
    
    @property
    def unique_id( self ) :
        """ a unique id of this object, read only """
        return self._unique_id