from pymongo import MongoClient

class DBSingleton():
    __dbInstance = None
    __instance = None

    @staticmethod
    def getInstance(connection=''):
        """ Static access method. """
        if DBSingleton.__dbInstance == None:
            DBSingleton(connection)
        return DBSingleton.__dbInstance

    def __init__(self, connection):
        super().__init__()
        if DBSingleton.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            DBSingleton.__instance = self
            DBSingleton.__dbInstance = MongoClient(connection)
