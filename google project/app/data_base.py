"""
this class is api of database with basic action
this is singleton - you can define only one object of this class.
this database is dictionary that key is word and value is array of sentences that word in key in sentence
"""

class DataBase:

    """
    this is for singleton
    """
    __instance = None
    _data_base = {}

    """
    run over the 'new' function for define this class of singleton
    """
    def __new__(cls, *args):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    """
    insert to database if keys already exist in database so append the value to array in this key
    if key not in database add key to database and value in array
    """
    def insert(self, key, value):
        if key in DataBase._data_base.keys():
            DataBase._data_base[key].append(value)
        else:
            DataBase._data_base[key] = [value]

    """
    return value of given key
    """
    def get(self, key):
            return DataBase._data_base[key]

    """
    run over 'str' function for print the dictionary
    """
    def __str__(self):
        return f"{DataBase._data_base}"
