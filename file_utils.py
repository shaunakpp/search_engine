import os
import shutil
class FileUtils:
    def __init__(self):
        self.path = ""
        self.files = []

    def get_files_from_path(self, file_path):
        self.path = file_path
        for (dirpath, dirnames, filenames) in os.walk(self.path):
            self.files.extend(filenames)
            break
        if '.DS_Store' in self.files:
            self.files.remove('.DS_Store')
        return self.files

    def clean_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            shutil.rmtree(path)
            os.makedirs(path)
