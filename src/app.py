# Importing the libraries that are needed for the program to run.
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, jsonify, request, Response, current_app
from flask_pymongo import PyMongo
from datetime import datetime
from bson import json_util
import logging
from bson.objectid import ObjectId

# Creating a Flask application instance.
app = Flask(__name__)

# Setting the secret key for the Flask app and the MongoDB URI.
app.secret_key = generate_password_hash("APIMongoPythonFlaskMonitoreo")
app.config["MONGO_URI"] = "mongodb://localhost:27017/invernadero"

# Creating a connection to the MongoDB database.
mongo = PyMongo(app)

time = str(datetime.today().strftime('%B %d %Y'))
salida = str(f'../logs/salida_({str(time)}).log')
logging.basicConfig(filename=salida, level=logging.DEBUG)

"""
    It takes a JSON object, inserts it into a MongoDB collection, and returns the ID of the inserted
    object.
    :return: The response is a JSON object with the _id of the inserted document.
"""


@app.route('/api/v1/addDatos', methods=['POST'])
def post_addDatos():
    app.logger.info(f'Funcionalidad post_addDatos... {datetime.now()}')
    datos = request.json
    if datos:
        id = mongo.db.datoCollection.insert_many(
            datos
        )
        # print("estos son los datos --> ",str(id.inserted_ids))
        response = jsonify({
            '_id': str(id.inserted_ids),
        })
        response.status_code = 201
        app.logger.info(f'Cantidad de datos -> {str(id.inserted_ids)} <--> {datetime.now()}')
        return response
    else:
        app.logger.error(f' addDatos incorrectos <--> {datetime.now()}')
        return {'message': 'addDatos incorrectos'}


"""
    It takes a request, queries the database, and returns a response
    :return: A list of dictionaries.
"""


@app.route('/api/v1/datos', methods=['GET'])
def get_datos():
    app.logger.info(f'Funcionalidad get_datos...{datetime.now()}')
    datos = mongo.db.datoCollection.find()
    response = json_util.dumps(datos)
    app.logger.info(f'Cantidad de datos -> {response.count("_id")} <--> {datetime.now()}')
    return Response(response, mimetype="application/json")


"""
    It takes a JSON object with two fields, fecha_ini and fecha_fin, and returns a JSON object with all
    the documents in the collection that have a date between the two dates
    :return: A JSON object with the following structure:
    [
        "_id": {
            "": "5c9b8f8f8b0be816b8b8b8b8"
        },
        "FECHA": "2019-03-27",
        "HORA": "12:00:00",
        ...,
        ...
    ]
"""


@app.route('/api/v1/filterDatos', methods=['POST'])
def post_filterDatos():
    app.logger.info(f'Funcionalidad post_filterDatos...{datetime.now()}')
    fecha_ini = request.json["fecha_ini"]
    fecha_fin = request.json["fecha_fin"]
    diccionario = {"FECHA": {"$gte": str(datetime.strptime(fecha_ini, "%Y-%m-%d")),
                             "$lte": str(datetime.strptime(fecha_fin, "%Y-%m-%d"))}}
    app.logger.info(f'Consulta {diccionario} <--> {datetime.now()}')
    registros = mongo.db.datoCollection.find(diccionario)
    response = json_util.dumps(registros)
    # return jsonify(registros)
    return Response(response, mimetype="application/json")


"""
    It filters the data from the database by date.
    
    :param fecha_ini: 2020-01-01
    :param fecha_fin: 2020-01-01
    :return: The response is a JSON object with the data that is in the database.
"""


@app.route('/api/v1/filterDatos/<fecha_ini>&<fecha_fin>', methods=['GET'])
def get_filterDatos(fecha_ini, fecha_fin):
    app.logger.info(f'Funcionalidad get_filterDatos...{datetime.now()}')
    diccionario = {"FECHA": {"$gte": str(datetime.strptime(fecha_ini, "%Y-%m-%d")),
                             "$lte": str(datetime.strptime(fecha_fin, "%Y-%m-%d"))}}
    app.logger.info(f'Consulta {diccionario} <--> {datetime.now()}')
    registros = mongo.db.datoCollection.find(diccionario)
    response = json_util.dumps(registros)
    return Response(response, mimetype="application/json")


"""
    It returns a JSON object with a message key and a value of "API YA ESTA ARRIBA INVERNADERO"
    :return: A dictionary with a key and value.
"""


@app.route('/', methods=['GET'])
def main():
    app.logger.info(f'Estado de API...{datetime.now()}')
    return {'message': 'API YA ESTA ARRIBA INVERNADERO'}


# Running the Flask app.
if __name__ == ('__main__'):
    app.logger.info(f'Se Inicia el Script de la API...{datetime.now()}')
    main()
    app.run(host="192.168.2.112", port=5000, debug=True)
