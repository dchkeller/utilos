

from .Parameter import Parameter


def test_Parameter() :
    
    a = Parameter( value=3, name="a", comment="blabla", default=None )
    s = a.dumps()
    
    assert s == "a = 3    # blabla (default=null)"
    
    a_loaded = Parameter.loads( s )
    
    assert a_loaded.value == a.value
    assert a_loaded.name == a.name
    assert a_loaded.comment == a.comment
    assert a_loaded.default == a.default
    
    
    a.default = 0
    assert a.default == 0
    
    a.reset()
    assert a.value == a.default
    
    s2 = "test = true # Some test parameter (default=false)"
    t_loaded = Parameter.loads( s2 )
    
    assert t_loaded.value == True
    assert t_loaded.name == "test"
    assert t_loaded.comment == "Some test parameter"
    assert t_loaded.default == False
    
    
    a.value = "my new value"
    a.default = "my default value"
    s = a.dumps()
    assert s == 'a = "my new value"    # blabla (default="my default value")'
    
    a_loaded = Parameter.loads( s )
    assert a_loaded.value == a.value
    
    a.reset()
    assert a.value == a.default

