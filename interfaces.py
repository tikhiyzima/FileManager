from abc import ABC, abstractmethod

class IFileSelector(ABC) :
    @abstractmethod
    def get_selected_files(self) :
        pass

    @abstractmethod
    def clear_selection(self) :
        pass

class IFileSystem(ABC) :
    @abstractmethod
    def exists(self, path) :
        pass

    @abstractmethod
    def is_file(self, path) :
        pass

    @abstractmethod
    def is_dir(self, path) :
        pass

    @abstractmethod
    def copy(self, src, dst) :
        pass

    @abstractmethod
    def move(self, src, dst) :
        pass

    @abstractmethod
    def remove_file(self, path) :
        pass

    @abstractmethod
    def remove_dir(self, path) :
        pass

class IUserInterface(ABC) :
    @abstractmethod
    def display(self, message) :
        pass