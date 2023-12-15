from flask import Flask, jsonify
from flask_cors import CORS
import os
import json
import random

# instancia flask
app = Flask(__name__)
CORS(app)

# lista de usuarios
lst_users_data = []

# carpeta que contiene los archivos JSON
json_folder = "./data/data"

# iterar sobre cada archivo en la carpeta
for archivo in os.listdir(json_folder):
    if archivo.endswith(".json"):
        ruta_archivo = os.path.join(json_folder, archivo)

        # abrir y cargar el contenido del archivo JSON
        with open(ruta_archivo, 'r') as f:
            datos_json = json.load(f)

        # agregar a la lista
        lst_users_data.append(datos_json)


# endpoints

# obtener todos los usuarios y sus seguidores
@app.route('/users', methods=['GET'])
def get_users():
    if not lst_users_data:
        return jsonify({"error": "No users available"}), 404

    return jsonify(lst_users_data), 200


# obtener todos usuario con menor cantidad de seguidores
@app.route('/user/min_followers', methods=['GET'])
def get_user_with_min_followers():
    if not lst_users_data:
        return jsonify({"error": "No users available"}), 404

    # inicializa con el primer usuario
    min_followers_users = [lst_users_data[0]]

    # comienzo a iterar despues del primer item
    for user_data in lst_users_data[1:]:
        # comparo iteracion con primer item
        
        if len(user_data['users_following']) < len(min_followers_users[0]['users_following']):
            min_followers_users = [user_data]
        elif len(user_data['users_following']) == len(min_followers_users[0]['users_following']):
            min_followers_users.append(user_data)

    # selecciono un usuario random con el minimo de seguidores
    selected_user = random.choice(min_followers_users)

    # retorno el id del usuario y cantidad de seguidores
    return_data = {
        "user_id": selected_user["user_id"],
        "amount_of_followers": len(selected_user["users_following"])
    }
    return jsonify(return_data), 200


if __name__ == '__main__':
    h = "localhost"
    p= 3000
    app.run(host=h, port=p)

