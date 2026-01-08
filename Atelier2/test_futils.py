import unittest
from unittest.mock import MagicMock, create_autospec

from futils import FileSelection, UserInterface, FileSystem, FileManager


class TestFManager(unittest.TestCase):

    def new_file_manager(self, selected_files=None, fs_delete_side_effect=None) -> FileManager:
        sel = create_autospec(FileSelection, spec_set=True)
        fs = create_autospec(FileSystem, spec_set=True)
        ui = create_autospec(UserInterface, spec_set=True)
        
        fs.delete = MagicMock(side_effect=fs_delete_side_effect) if fs_delete_side_effect else MagicMock(return_value=None)

        sel.get_and_reset = MagicMock(return_value=selected_files or [])
        return FileManager(sel, fs, ui)


    def test_delete_empty_list(self):
        test = self.new_file_manager(selected_files=[])
        self.assertEqual(0, test.delete_files())
        self.assertEqual(0, test.fs.delete.call_count)


    def test_delete_singlefile_list(self):
        test = self.new_file_manager(["file1"])

        actual = test.delete_files()
        
        self.assertEqual(1, actual)
        test.fs.delete.assert_called_once_with("file1")


    def test_delete_multiplefile_list(self):
        test = self.new_file_manager(["file1", "file2", "file3"])

        actual = test.delete_files()
        
        self.assertEqual(3, actual)    
        test.fs.delete.assert_has_calls([
            unittest.mock.call("file1"), 
            unittest.mock.call("file2"), 
            unittest.mock.call("file3")
        ])
        
    
    def test_delete_with_exception(self):
        test = self.new_file_manager(
            selected_files=["file1"],
            fs_delete_side_effect=Exception("Delete failed"),
        )
        actual = test.delete_files()
        
        self.assertEqual(0, actual)
        test.ui.error.assert_called_once()
        test.fs.delete.assert_called_once_with("file1")
