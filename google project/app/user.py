"""
import useful libraries to project
"""
try:
    from app.auto_complete_data import AutoCompleteData

except ImportError:
    print("Need to fix the installation")
    raise

"""
class that contact to user. get input from user and send it to 'AutoCompleteData' class
"""
class User:

    def __init__(self):
        self.string_search = ""

    """
    get input from user and if user enter '#' the system back to start
    """
    def run(self):
        while True:
            self.string_search += " " + input(self.string_search + " ")
            if "#" not in self.string_search:
                AutoCompleteData((self.string_search.lower()).split()).find_string()
            else:
                print("The system is ready. Enter your text:")
                self.string_search = ""
