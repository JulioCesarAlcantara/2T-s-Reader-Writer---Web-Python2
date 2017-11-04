import requests
# from flask import app, jsonify, json

from LocationModel import LocationModel
from Things import Things
from ThingsModel import ThingsModel
from ThingsXLocationModel import ThingsXLocationModel
from User import User

# @app.route('/get_locations_db/token=<string:token>', methods=['GET'])
# def get_locations_db(token):
#     if token != token_padrao_get_db:
#         return jsonify({'response': 'Token Invalido'})
#
#     location = Locations()
#     return json.dumps(para_dict(location.get_all_locations_db()))

def getLocations(token):

    try:
        url = "https://dg-2ts-server.herokuapp.com/"
        response = requests.get (url + "get_locations_db/token=" + token)
        data = response.json ()

        if response.ok:
            try:
                if data["response"] == None:
                    print ("Aqui")
                else:
                    print (data["response"])
            except Exception as e:
                locations = []
                for dados in data:
                    locations.append(LocationModel(**dados))

                return locations
    except Exception as e:
        print ("Erro no Servidor")

#
# @app.route('/get_things_db/token=<string:token>', methods=['GET'])
# def get_things_db(token):
#     if token != token_padrao_get_db:
#         return jsonify({'response': 'Token Invalido'})
#
#     things = Things()
#
#     return json.dumps(para_dict(things.get_all_things_db()))
#
def getThings(token):

    try:
        url = "https://dg-2ts-server.herokuapp.com/"
        response = requests.get (url + "get_things_db/token=" + token)
        data = response.json ()

        if response.ok:
            try:
                if data["response"] == None:
                    print ("Aqui")
                else:
                    print (data["response"])
            except Exception as e:
                Things = []
                for dados in data:
                    Things.append (ThingsModel (**dados))

                return Things
    except Exception as e:
        print ("Erro no Servidor")

# a = getThings('123')
#
# for b in a:
#     print b

#
# @app.route('/get_things_location_db/token=<string:token>', methods=['GET'])
# def get_things_location_db(token):
#     if token != token_padrao_get_db:
#         return jsonify({'response': 'Token Invalido'})
#
#     things_location = ThingsXLocation()
#
#     return json.dumps(para_dict(things_location.get_things_x_location_db()))
#

def getThingsLocations(token):

    try:
        url = "https://dg-2ts-server.herokuapp.com/"
        response = requests.get (url + "get_things_location_db/token=" + token)
        data = response.json ()

        if response.ok:
            try:
                if data["response"] == None:
                    print ("Aqui")
                else:
                    print (data["response"])
            except Exception as e:
                ThingsLoc = []
                for dados in data:
                    ThingsLoc.append (ThingsXLocationModel (**dados))

                return ThingsLoc
    except Exception as e:
        print ("Erro no Servidor")

#
# @app.route('/get_users_db/token=<string:token>', methods=['GET'])
# def get_users_db(token):
#     if token != token_padrao_get_db:
#         return jsonify({'response': 'Token Invalido'})
#
#     user = User()
#
#     return json.dumps(para_dict(user.get_users_db()))

def getUsers(token):

    try:
        url = "https://dg-2ts-server.herokuapp.com/"
        response = requests.get (url + "get_users_db/token=" + token)
        print url + "get_users_db/token=" + token
        data = response.json ()

        if response.ok:
            try:
                if data["response"] == None:
                    print ("Aqui")
                else:
                    print (data["response"])
            except Exception as e:
                Users = []
                for dados in data:
                    Users.append (User (**dados))

                return Users
    except Exception as e:
        print ("Erro no Servidor")

def synchronizeBdLocal():
    token_bd = '123'
    things = Things ()
    user = User()
    locationsServer = getLocations(token_bd)
    thingServer = getThings(token_bd)
    thingsLocationServer = getThingsLocations(token_bd)
    userServer = []
    userServer =getUsers(token_bd)

    arrayIdServer = []
    for a in userServer:
        a.id = "0"
        arrayIdServer.append(a)

        print a.id


    userLocal = []
    locationsLocal = things.search_locations ()
    thingLocal = things.search_all_things()
    userLocal=user.search_all_users()

    arrayIdLocal = []
    for a in userLocal:
        a.id = "0"
        arrayIdLocal.append (a)

        print a.id

    arrayUser = []
    for i in range(len(userServer)):
            if arrayIdServer[i] not in arrayIdLocal:
                for users in arrayIdServer:
                    user.insert_new_user(users.name, users.email, users.password, users.token, users.permission)


synchronizeBdLocal()