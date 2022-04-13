
from .Parameter import Parameter
from .HasParameters import HasParameters

class Dummy( HasParameters ) :
    
    param1 = Parameter( comment="Some parameter 1", default=1 )
    param2 = Parameter( comment="Some parameter 2", default=False )

def test_ParameterDescriptor() :
    
    d = Dummy()
    
    assert hasattr( d, "param1" )
    assert hasattr( d, "param2" )

    assert d._params["param1"].value == 1
    assert d._params["param2"].value == False
    assert d._params["param1"].default == 1
    assert d._params["param2"].default == False
    
    assert d.param1 == 1
    assert d.param2 == False
    
    assert d._params["param1"].default == 1
    
    
    d.param1_default = 3
    assert d.param1_default == 3
    d.param1_default = 1
    
    assert hasattr( d, "_params" )
    
    
    d.param1 = "my new value"
    assert d.param1 == "my new value"
    
    
    e = Dummy( param1 = 2, param2 = False )
    
    assert e.param1 == 2
    assert e.param2 == False
    
    assert e.__init__.__doc__ != ""
    
    s = e.dumps()
    
    f = HasParameters.loads( s )
    
    assert f.param1 == 2
    assert f.param2 == False
    
    s = s.replace( "default=1", "default=2" )
    s = s.replace( "default=False", "default='a'")
    g = HasParameters.loads( s )


    assert s == g.dumps()
    
    assert g.param1 == 2
    assert g._params["param1"].default == 2
    assert g.param2 == False