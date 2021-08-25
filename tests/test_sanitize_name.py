from csvUpload.util.tasks import sanitize_name

class TestFilenameSanitization:
    def test_1(self):
        new_name = sanitize_name('Test-File-1')
        assert new_name == 'TestFile1'

    def test2(self):
        new_name = sanitize_name('TestFile')
        assert new_name == 'TestFile'

    def test3(self):
        new_name = sanitize_name(';-_')
        assert len(new_name) == 6
        assert ';' not in new_name
        assert '-' not in new_name
        assert '_' not in new_name