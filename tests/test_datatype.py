from csvUpload.util.csvutil import datatype

class TestDatatype:
    def test1(self):
        assert datatype('test') == 'VARCHAR'

    def test2(self):
        assert datatype('123') == 'INT'

    def test3(self):
        assert datatype('1.223') == 'REAL'

    def test4(self):
        assert datatype('.23') == 'REAL'

    def test5(self):
        assert datatype('9') == 'INT'

    def test6(self):
        assert datatype('Epsilon-Alpha') == 'VARCHAR'