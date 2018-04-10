from asynchat import async_chat

import requests


def activeThings(Token, nThings):
    try:
        url = "https://dg-2ts-server.herokuapp.com/"
        response = requests.get (url + "active_thing_by_num/token="+ Token + "&num=" + nThings)
        data = response.json ()
        print data

        if response.ok:
            try:
                if data["response"] == None:
                    print("Aqui")
                    return 0
                else:
                    print(data['response'])
                    return True
            except Exception as e:
                print "Exception: ",e
                return 'Erro'

    except Exception as e:
        print "Erro no Servidor", e
        return False


activeThings('asdfasdfasdfz','29031')

# @app.route('/active_thing_by_num/token=<string:token>&num=<string:num>', methods=['GET'])
# def active_thing_by_num(token, num):
#     # valida token
#     user = User()
#     resp = user.verify_token(token)
#     if resp == False:
#         return jsonify({'response': 'Token Invalido'})
#     elif resp == 'ERRO':
#         return jsonify({'response': 'Erro ao verificar token'})
#
#     things = Things()
#     exits = things.search_things_by_num1(num)
#     if exits:
#         response = things.active_things_by_num1(num)
#         if response == False:
#             return jsonify({'response': 'Ocorreu um erro ao ativar a etiqueta'})
#         else:
#             return jsonify({'response': 'true'})
#     else:
#         return jsonify({'response': 'Objeto nao encontrado'})