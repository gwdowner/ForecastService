import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, jsonify
from Data import DBSingleton 

# We must first import the connection
DBSingleton(os.getenv('DB_CONNECTION'))
from Server.forecast import forecastApi

PORT = os.getenv('PORT')

app = Flask(__name__)
app.register_blueprint(forecastApi)
## Load in model ##
## Register routes
@app.route('/')
def hello():
    return 'hello world'


## run application
##app.run(port=PORT)
if __name__ == '__main__':
    app.run(port=PORT)
