from pymodm import connect

mongo_uri = "mongodb+srv://application:dbapplication@ticktrackcluster-p1bgs." \
            "mongodb.net/ticktrack?retryWrites=true&w=majority"
connect(mongo_uri, alias="mongodb_app")
