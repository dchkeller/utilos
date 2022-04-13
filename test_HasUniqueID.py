
from .HasUniqueID import HasUniqueID

import pytest


class Dummy1( HasUniqueID ) :
    pass

class Dummy2( HasUniqueID ) :
    pass

class Dummy3( Dummy1 ) :
    pass

def test_unique_id() :
    
    a = Dummy1()
    b = Dummy2()
    c = Dummy3()

    assert a.unique_id != b.unique_id
    assert b.unique_id != c.unique_id
    assert c.unique_id != a.unique_id
    
    with pytest.raises( AttributeError ) :
        c.unique_id = 4
    

    

