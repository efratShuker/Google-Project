"""
import useful libraries to project
"""
try:
    from app.insert_data import InsertData
    from app.user import User

except ImportError:
    print("Need to fix the installation")
    raise

if __name__ == '__main__':
    """
    define object of "InsertData" in order insert data to database it is only one in process
    """
    InsertData("C:/Users/user1/Documents/google project/data").insert_data_to_DB()
    """
    define object of "User" in order to begin get input from user and operate the system
    """
    User().run()
