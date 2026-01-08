import os
import shutil
from interfaces import IFileSelector, IFileSystem, IUserInterface
from ui import ConsoleUI

""" File Manager Console Application 
    Generated with Claude 3.5 Haiku
    With 2 prompts : 
        Génère un programme console python qui permet d'explorer les fichiers, 
        en sélectionner pour copier, déplacer et supprimer les fichiers sélectionnés. 
        Une classe "métier" regroupe les fonctions de sélection, copie, déplacement 
        et suppression.

        Deux rectifications : il faudrait passer le code et l'interface en anglais 
        et sortir la sélection de la classe "métier"
"""


class RealFileSystem(IFileSystem) :
    def exists(self, path) :
        return os.path.exists(path)
	
    def is_file(self, path) :
        return os.path.isfile(path)

    def is_dir(self, path) :
        return os.path.isdir(path)

    def copy(self, src, dst) :
        shutil.copy2(src, dst)

    def move(self, src, dst) :
        shutil.move(src, dst)

    def remove_file(self, path) :
        os.remove(path)

    def remove_dir(self, path) :
        shutil.rmtree(path)




class FileSelector(IFileSelector) :
    def __init__(self):
        self.selected_files = []
        self.current_directory_contents = []

    def load_directory_contents(self, directory_path):
        """Load the contents of a directory"""
        try:
            self.current_directory_contents = os.listdir(directory_path)
            return self.current_directory_contents
        except Exception as e:
            print(f"Error loading directory contents: {e}")
            return []

    def select_files_by_indices(self, indices, directory_path):
        """Select files based on indices"""
        try:
            # Convert input string to list of indices
            selected_indices = [int(i.strip()) for i in indices.split(',')]
            
            # Reset previous selection
            self.selected_files.clear()
            
            # Select files
            for index in selected_indices:
                if 0 <= index < len(self.current_directory_contents):
                    full_path = os.path.join(directory_path, self.current_directory_contents[index])
                    self.selected_files.append(full_path)
            
            print("Selected files:")
            for file in self.selected_files:
                print(f" - {os.path.basename(file)}")
            
            return self.selected_files
        except ValueError:
            print("Invalid input. Please enter valid indices.")
            return []
        except Exception as e:
            print(f"Error selecting files: {e}")
            return []

    def get_selected_files(self):
        """Return the list of currently selected files"""
        return self.selected_files

    def clear_selection(self):
        """Clear the current file selection"""
        self.selected_files.clear()
        





#		sortir les fonctions d'exploration 
#		pour les mettre dans une classe FileExplorer
#		

class FileExplorer:
    def __init__(self, file_selector): 
        self.current_path = os.path.expanduser('~')
        self.file_selector = file_selector

    def display_directory_contents(self):
        """Display contents of the current directory"""
        try:
            contents = self.file_selector.load_directory_contents(self.current_path)
            print(f"\nCurrent Directory: {self.current_path}")
            print("-" * 50)
            for index, element in enumerate(contents):
                full_path = os.path.join(self.current_path, element)
                element_type = "📁 Folder" if os.path.isdir(full_path) else "📄 File"
                print(f"{index}. {element_type}: {element}")
        except PermissionError:
            print("Access denied to this directory.")
        except Exception as e:
            print(f"Error: {e}")

    def navigate(self, index):
        """Navigate to a subdirectory"""
        try:
            contents = os.listdir(self.current_path)
            selected_element = contents[index]
            full_path = os.path.join(self.current_path, selected_element)
            
            if os.path.isdir(full_path):
                self.current_path = full_path
                self.display_directory_contents()
            else:
                print(f"Cannot open file {selected_element}")
        except Exception as e:
            print(f"Navigation error: {e}")

    def go_to_parent_directory(self):
        """Move to the parent directory"""
        self.current_path = os.path.dirname(self.current_path)
        self.display_directory_contents()





#		classe FileManager "nettoyée" 
#		


class FileManager:
    def __init__(self , file_selector : IFileSelector , file_system : IFileSystem , ui : IUserInterface) :
        self.file_selector = file_selector
        self.file_system = file_system
        self.ui = ui

    def copy_files(self, destination):
        """Copy selected files"""
        try:
            selected_files = self.file_selector.get_selected_files()
            count = 0
            for file in selected_files:
                if self.file_system.exists(file):
                    self.file_system.copy(file, destination)
                    count += 1
            self.ui.display(f"{count} file(s) copied")
            self.file_selector.clear_selection()
        except Exception as e:
            self.ui.display(f"Copy error: {e}")

    def move_files(self, destination):
        """Move selected files"""
        try:
            selected_files = self.file_selector.get_selected_files()
            count = 0
            for file in selected_files:
                
                if self.file_system.exists(file):
                    self.file_system.move(file, destination)
                    count += 1
                    
            self.ui.display(f"{count} file(s) moved")
            self.file_selector.clear_selection()
        except Exception as e:
            self.ui.display(f"Move error: {e}")

    def delete_files(self):
        """Delete selected files"""
        try:
            selected_files = self.file_selector.get_selected_files()
            count = 0
            for file in selected_files:
                
                if self.file_system.is_file(file):
                    self.file_system.remove_file(file)
                    count += 1
                elif self.file_system.is_dir(file):
                    self.file_system.remove_dir(file)
                    count += 1
                    
            self.ui.display(f"{count} file(s)/folder(s) deleted")
            self.file_selector.clear_selection()
        except Exception as e:
            self.ui.display(f"Delete error: {e}")


def main_menu():
    file_system = RealFileSystem()
    console_ui = ConsoleUI()
    
    file_selector = FileSelector()
    file_explorer = FileExplorer(file_selector)
    file_manager = FileManager(file_selector , file_system , console_ui)
    
	
    
    while True:
        print("\n--- File Explorer ---")
        print("1. Display Directory")
        print("2. Navigate")
        print("3. Go to Parent Directory")
        print("4. Select Files")
        print("5. Copy")
        print("6. Move")
        print("7. Delete")
        print("8. Quit")
        
        choice = input("Your choice: ")
        
        try:
            if choice == '1':
                file_explorer.display_directory_contents()
            
            elif choice == '2':
                index = int(input("Enter navigation index: "))
                file_explorer.navigate(index)
            
            elif choice == '3':
                file_explorer.go_to_parent_directory()
            
            elif choice == '4':
                file_explorer.display_directory_contents()
                indices = input("Enter file indices to select (comma-separated): ")
                file_selector.select_files_by_indices(indices, file_explorer.current_path)
            
            elif choice == '5':
                dest = input("Enter destination path for copying: ")
                file_manager.copy_files(dest)
            
            elif choice == '6':
                dest = input("Enter destination path for moving: ")
                file_manager.move_files(dest)
            
            elif choice == '7':
                file_manager.delete_files()
            
            elif choice == '8':
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice")
        
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main_menu()