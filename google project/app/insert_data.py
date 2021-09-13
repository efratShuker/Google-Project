"""
import useful libraries to project
"""
try:
    import os
    import re
    from app.data_base import DataBase

except ImportError:
    print("Need to fix the installation")
    raise

"""
class that read data from files and insert it to dictionary
"""
class InsertData:
    data_base = DataBase()

    def __init__(self, file_path):
        self.file_path = file_path

    """
    read all sentences from file and return it in array
    """
    def read_data(self, file):
        with open(file, encoding="utf8") as current_file:
            file_data = current_file.readlines()
            return file_data

    """
    pass all folders in root folder and read files and insert to database
    """
    def insert_data_to_DB(self):
        print("Loading the files and preparing the system...")
        for root, dirs, files in os.walk(self.file_path):
            for f in files:
                data_file = self.read_data(os.path.join(root, f))
                for line in data_file:
                    for word in line.split():
                        # replace all a special chars to "" and ignore than lower/bigger letters
                        new_name = re.sub('[!@#$%^&*().,;:/?><"\']', "", word.lower())
                        InsertData.data_base.insert(new_name, (line, line.find(word), os.path.join(root, f)))
        print("The system is ready. Enter your text:")
