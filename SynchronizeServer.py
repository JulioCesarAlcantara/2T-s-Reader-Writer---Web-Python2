import requests
from Connection import Connection

# @app.route('/get_locations_db/token=<string:token>', methods=['GET'])
# def get_locations_db(token):
#     if token != token_padrao_get_db:
#         return jsonify({'response': 'Token Invalido'})
#
#     location = Locations()
#     return json.dumps(para_dict(location.get_all_locations_db()))

def getLocations():

    try:
        url = "https://dg-2ts-server.herokuapp.com/"
        response = requests.get (url + "get_locations_db/token=123")

        if response.ok:
            return response.text
        else:
            return False

    except Exception as e:
        print ("Erro no Servidor")
        return 0

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
def getThings():

    try:
        url = "https://dg-2ts-server.herokuapp.com/"
        response = requests.get (url + "get_things_db/token=123")

        if response.ok:
            return response.text
        else:
            return False

    except Exception as e:
        print ("Erro no Servidor")
        return 0
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

def getThingsLocations():

    try:
        url = "https://dg-2ts-server.herokuapp.com/"
        response = requests.get (url + "get_things_location_db/token=123")

        if response.ok:
            return response.text
        else:
            return False
    except Exception as e:
        print ("Erro no Servidor")
        return 0
#
# @app.route('/get_users_db/token=<string:token>', methods=['GET'])
# def get_users_db(token):
#     if token != token_padrao_get_db:
#         return jsonify({'response': 'Token Invalido'})
#
#     user = User()
#
#     return json.dumps(para_dict(user.get_users_db()))

def getUsers():

    try:
        url = "https://dg-2ts-server.herokuapp.com/"
        response = requests.get (url + "get_users_db/token=123")

        if response.ok:
            return response.text
        else:
            return False
    except Exception as e:
        print ("Erro no Servidor")
        return 0

def updateBdThingsLocation():
    location = getLocations()
    users = getUsers()
    things = getThings()
    thingsLocation = getThingsLocations()

    if thingsLocation == False:
        print "Erro ao buscar dados de coisas na localizacao. Contate o analista"
    elif thingsLocation == 0:
        print "Erro no servidor"
    else:
        try:
            print "Deletando tabela de bens x localizacao ..."
            sql = "DELETE FROM `patr_bens_x_localizacao`"
            conn = Connection()
            conn.execute_sql(sql)
            conn.commit()
            print "bens x localizacao excluida com sucesso !!"

            print "Deletando tabela de usuarios ... "
            sql = "DELETE FROM `usuarios`"
            conn = Connection ()
            conn.execute_sql (sql)
            conn.commit ()
            print "tabela de usuarios excluida com sucesso !!"

            print "Deletando tabela de bens ..."
            sql = "DELETE FROM `patr_bens`"
            conn = Connection ()
            conn.execute_sql (sql)
            conn.commit ()
            print "Tabela de bens excluida com sucesso !!"

            print "Deletando tabela de localizacoes ..."
            sql = "DELETE FROM `localizacao`"
            conn = Connection ()
            conn.execute_sql (sql)
            conn.commit ()
            print "Tabela de localizacoes excluida com sucesso !!"

            print "Inserindo usuarios ..."
            sql = str(users)
            conn = Connection()
            conn.execute_sql(sql)
            conn.commit ()
            print "Usuarios inseridos com sucesso !! "

            print "Inserindo localizacoes ..."
            sql = str(location)
            conn = Connection()
            conn.execute_sql(sql)
            conn.commit()
            print "Localizacoes inseridas com sucesso !!"

            print "Inserindo Coisas ..."
            sql = str (things)
            conn = Connection ()
            conn.execute_sql (sql)
            conn.commit ()
            print "Coisas inseridas com sucesso !!"

            print "Inserindo coisas nas localizacoes ..."
            sql = str (thingsLocation)
            conn = Connection ()
            conn.execute_sql (sql)
            conn.commit ()
            print "Coisas inseridas nas localizacoes com sucesso !!"

            print "Banco de Dados Local Sincronizado com Sucesso !!"
            return True
        except Exception as e:
            conn.rollback()
            print(e)
            print "Erro ao sincronizar. Verique sua conexao !!"
            return False
        finally:
            conn.close_connection()

# def updateBdUsers():
#     location = getLocations()
#     users = getUsers()
#     things = getThings()
#
#     if users == False:
#         print "Erro ao buscar dados de usuarios no servidor. Contate o analista"
#     elif users == 0:
#         print "Erro no servidor"
#     else:
#         try:
#             sql = "DELETE FROM `usuarios`"
#             conn = Connection()
#             conn.execute_sql(sql)
#             conn.commit()
#
#             sql = str(users)
#             conn = Connection ()
#             conn.execute_sql (sql)
#             conn.commit ()
#
#             print "Deu Certo !!!"
#         except Exception as e:
#             conn.rollback()
#             print(e)
#             print "Deu errado !!!"
#         finally:
#             conn.close_connection()
#
# def updateBdUsers():
#     location = getLocations()
#     users = getUsers()
#     things = getThings()
#
#     if users == False:
#         print "Erro ao buscar dados de usuarios no servidor. Contate o analista"
#     elif users == 0:
#         print "Erro no servidor"
#     else:
#         try:
#             sql = "DELETE FROM `usuarios`"
#             conn = Connection()
#             conn.execute_sql(sql)
#             conn.commit()
#
#             sql = str(users)
#             conn = Connection ()
#             conn.execute_sql (sql)
#             conn.commit ()
#
#             print "Deu Certo !!!"
#         except Exception as e:
#             conn.rollback()
#             print(e)
#             print "Deu errado !!!"
#         finally:
#             conn.close_connection()
