class TestClass: 
    def test_one(self):
        x = "this"
        assert "h" in x
    
    def test_two(self): 
        x = "hello"
        help(str)
        assert hasattr(x, "__add__")