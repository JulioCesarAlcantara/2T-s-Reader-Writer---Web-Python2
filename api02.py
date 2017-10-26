#!/usr/bin/env python
# import os
# from builtins import print
#!-*- conding: utf8 -*-

import sys

from pip.utils import encoding
#encoding: utf-8

#encoding: utf-8
from flask import jsonify, request, Flask, render_template, url_for, session, g
import json
# from ThingsSynchronization import ThingsSynchronization
# from ThingsManager.LocationModel import LocationModel
# from ThingsManager.Things import Things
# from ThingsManager.ThingsXLocation import ThingsXLocation
# import User
from werkzeug.utils import redirect
# from Classes.write_id import writerTag
import string
import random
import os

from Things import Things

from User import User
from write_id  import start

# import RPi.GPIO as GPIO
# import MFRC522
# import signal


reload(sys)
sys.setdefaultencoding('utf8')

def para_dict(obj):
    # Se for um objeto, transforma num dict
    if hasattr(obj, '__dict__'):
        obj = obj.__dict__

    # Se for um dict, le chaves e valores; converte valores
    if isinstance(obj, dict):
        return {k: para_dict(v) for k, v in obj.items()}

    elif isinstance(obj, list) or isinstance(obj, tuple):
        return [para_dict(e) for e in obj]
    else:
        return obj


app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    if 'user' in session:
        return render_template('/inicial.html', message=session['name'])
    return render_template('/login.html')


@app.route('/post_login', methods=['POST'])
def post_login():
    email = request.form['email']
    password = request.form['password']

    user = User()
    try:
        response = user.autenticate(email, password)
        if response == False:
            return render_template('/login.html', message="You have entered an invalid username or password")
        else:
            session.pop('user', None)
            session['token'] = response.token
            session['id'] = response.id
            session['name'] = response.name
            session['user']=request.form['email']
            session['permission']=response.permission
            return render_template('/inicial.html', message=session['name'])
    except Exception as e:
        print(e)
        return "Erro no servidor. Contate o Analista"


@app.route('/inicial')
def inicial():
    if g.user:
        return render_template('/inicial.html', message=session['name'])

    return redirect(url_for('index'))

@app.before_request
def beforerequest():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/getsession')
def getsession():
    if 'user' in session:
        return session['name']
    return 'Not logged in!'

@app.route('/dropsession')
def dropsession():
    session.pop('user', None)
    return 'Dropped!'

@app.route('/users', methods=['POST'])
def users():
    user = User()
    users = user.search_all_users()

    return render_template('/users.html', users=users)

@app.route('/things', methods=['POST'])
def locations():
    things = Things ()
    location = things.search_locations ()

    return render_template('/things.html', location=location)

@app.route('/conThings', methods=['POST'])
def thingsTable():
    things = Things ()
    location = things.search_locations ()

    loca_id = request.form['location']
    status = request.form['status']

    if loca_id == "0" and status == "1":
        thingsdata = things.search_all_things_actives()

        if thingsdata == False:
            msg = "Object not found."
            return render_template ('/things.html', location=location, message=msg)

    elif loca_id == "0" and status == "2":
        thingsdata = things.search_all_things_inactives()

        if thingsdata == False:
            msg = "Object not found."
            return render_template ('/things.html', location=location, message=msg)

    elif loca_id != "0" and status == "0":
        thingsdata = things.search_things_by_location(loca_id)

        if thingsdata == False:
            msg = "Object not found."
            return render_template ('/things.html', location=location, message=msg)

    elif loca_id != "0" and status == "1":
        thingsdata = things.search_things_actives_by_location(loca_id)

        if thingsdata == False:
            msg = "Object not found."
            return render_template ('/things.html', location=location, message=msg)

    elif loca_id != "0" and status == "2":
        thingsdata = things.search_things_inactives_by_location(loca_id)

        if thingsdata == False:
            msg = "Object not found."
            return render_template ('/things.html', location=location, message=msg)

    elif loca_id == "0" and status == "0":
        msg = "Please select a Location or Status for consultation. Or, if you prefer, select both."
        return render_template ('/things.html', location=location, message=msg)

    # thingsData = things.search_things_by_location (loca_id)

    return render_template('/things.html', thingsdata=thingsdata, location=location)


@app.route('/reader', methods=['POST'])
def listLocationReader():
    things = Things ()
    location = things.search_locations ()

    return render_template ('/reader.html', locations=location)

@app.route('/writer', methods=['POST'])
def listLocationWriter():
    things = Things ()
    location = things.search_locations ()

    return render_template ('/writer.html', locations=location)

@app.route('/synchronize', methods=['POST'])
def synchronize():
    with open('sync.json') as json_data:
        data = json.load(json_data)
        list = []
        for thing in data['Things']:
            list.append(thing)

        for t in list:
            print(t['name'])

    return render_template ('/synchronize.html', things=list)

@app.route('/writeTag', methods=['POST'])
def writerInTag():

    start ('26')
    import subprocess

    # processo = subprocess.call (["sudo python /home/pi/Documentos/python2/2T-s-Reader-Writer---Web-Python2/write_id.py", "26"], shell=True)

    # print "Resultado" + str(processo)

    return render_template ('/writer.html', msg="sucesso")


def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()


@app.route('/readerLoc', methods=['POST'])
def thingsTableReader():
    things = Things ()
    location = things.search_locations ()

    loca_id = request.form['location1']

    if loca_id != "0":

        print ("Inserir funcao de leitura")
        txt = "Waiting for Reading ..."
    else:
        msg = "Please, Select a Location to Read."
        return render_template ('/reader.html', locations=location, message=msg)


    return render_template('/reader.html', locations=location, texto=txt)

@app.route('/writeCon', methods=['POST'])
def thingsTableWriter():
    things = Things ()
    location = things.search_locations ()

    code = request.form['code1']
    loca_id = request.form['location2']

    if loca_id != "0" and code == "":
        dados = things.search_things_inactives_by_location(loca_id)

        if dados == False:
            msg = "Objects not found."
            return render_template ('/writer.html', locations=location, message=msg)

    elif loca_id == "0" and code != "":
        dados = []
        dados.append(things.search_things_by_num1(code))

        if dados[0] == False:
            msg = "Objects not found."
            return render_template ('/writer.html', locations=location, message=msg)
    else:
        msg = "Please, Enter a Code or Location to Write."
        return render_template ('/writer.html', locations=location, message=msg)

    return render_template('/writer.html', locations=location, dado=dados)

@app.route('/adduser', methods=['POST'])
def adduser():
    nome = request.form['name']
    email = request.form['email']
    senha = request.form['password']
    permissao = request.form['permission']
    token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(9))

    user = User()

    try:
        response = user.insert_new_user(nome, email, senha, token, permissao)
        if response == True:
            return "sucesso"
        else:
            return "Erro ao cadastrar usuario."

    except Exception as e:
        return 'Erro no servidor. Contate o analista responsavel!'


@app.route('/findUser', methods=['POST'])
def findUser():
    id = request.form['id']
    user = User()
    users = user.search_all_users()
    try:
        response = user.search_user_by_id(id)
        if response == False:
            return "Erro ao buscar usuario"
        else:
            return render_template('/users.html', users=users, user1=response)

    except Exception as e:
        return 'Erro no servidor. Contate o analista responsavel!'


@app.route('/findThing', methods=['POST'])
def findThing():
    numThing = request.form['numeroPat']

    things = Things()
    try:
        response = things.search_things_by_num1(numThing)

        if response == False:
            return "Nenhuma coisa encontrada com o numero informado"
        else:
            return render_template('/things.html', thing=response)
    except Exception as e:
        return 'Erro no servidor. Contate o analista responsavel!'


@app.route('/editUser', methods=['POST'])
def editUser():
    id = request.form['id1']
    nome = request.form['name']
    email = request.form['email']
    senha = request.form['password']
    permissao = request.form['permission']

    user = User()
    try:
        response = user.edit_user(id, nome, email, senha, permissao)
        if response == False:
            return "Erro ao atualizar usuario"
        else:
            return "Usuario atualizado com sucesso"

    except Exception as e:
        return 'Erro no servidor. Contate o analista responsavel!'


@app.route('/editThing', methods=['POST'])
def editThing():
    id = request.form['id']
    descricao = request.form['descricao']
    num1 = request.form['num1']
    num2 = request.form['num2']
    preco = request.form['preco']
    situacao = request.form['situacao']
    estado = request.form['estado']
    observacao = request.form['observacao']

    thing = Things()

    try:
        response = thing.update_thing2(id, descricao, num1, num2, preco, situacao, estado, observacao)
        if response == True:
            return "Coisa atualizada com sucesso"
        else:
            return "Erro ao atualizar coisa"
    except Exception as e:
        return 'Erro no servidor. Contate o analista responsavel!'


@app.route('/voltar', methods=['POST'])
def voltar():
    return render_template('/inicial.html', message=session['name'])


@app.route('/things', methods=['POST'])
def things():
    return render_template('/things.html')

@app.route('/reader', methods=['POST'])
def reader():
    return render_template('/reader.html')


@app.route('/addthing', methods=['POST'])
def addthing():
    descricao = request.form['descricao']
    num1 = request.form['num1']
    num2 = request.form['num2']
    preco = request.form['preco']
    situacao = request.form['situacao']
    estado = request.form['estado']
    observacao = request.form['observacao']

    thing = Things()
    try:
        response = thing.insert_new_thing(num1, num2, descricao, preco, situacao, estado, observacao)
        if response == True:
            return "Coisa cadastrada com sucesso."
        else:
            return "Erro ao cadastrar coisa."

    except Exception as e:
        return 'Erro no servidor. Contate o analista responsavel !!'


@app.route('/quit', methods=['POST'])
def quit():
    session.pop('user', None)
    return render_template('/login.html')


@app.route('/user_autenticate/email=<string:email>&password=<string:password>', methods=['GET'])
def logar(email, password):
    user = User()
    response = user.autenticate(email, password)
    if response == False:
        return jsonify({'response': 'Nenhum usuario encontrado'})
    elif response == 'ERRO':
        return jsonify({'response': 'Ocorreu um erro no servidor'})
    else:
        return json.dumps(para_dict(response))


@app.route('/search_things_by_num/token=<string:token>&num=<string:num>', methods=['GET'])
def search_things_by_num(token, num):
    # valida token
    user = User()
    resp = user.verify_token(token)
    if resp == False:
        return jsonify({'response': 'Token Invalido'})
    elif resp == 'ERRO':
        return jsonify({'response': 'Erro ao verificar token'})

    things = Things()
    response = things.search_things_by_num1(num)
    if response == False:
        return jsonify({'response': 'Nenhum objeto encontrado'})
    elif response == 'ERRO':
        return jsonify({'response': 'Ocorreu um erro no servidor'})
    else:
        return json.dumps(para_dict(response))


@app.route('/search_things_actived_by_location/token=<string:token>&locaid=<string:loca_id>', methods=['GET'])
def search_things_act_by_location(token, loca_id):
    # valida token
    user = User()
    resp = user.verify_token(token)
    if resp == False:
        return jsonify({'response': 'Token Invalido'})
    elif resp == 'ERRO':
        return jsonify({'response': 'Erro ao verificar token'})

    things = Things()
    response = things.search_things_actives_by_location(loca_id)
    if response == False:
        return jsonify({'response': 'Nenhum objeto encontrado'})
    elif response == 'ERRO':
        return jsonify({'response': 'Ocorreu um erro no servidor'})
    else:
        return json.dumps(para_dict(response))


@app.route('/search_things_inactived_by_location/token=<string:token>&locaid=<string:loca_id>', methods=['GET'])
def search_things_inact_by_location(token, loca_id):
    # valida token
    user = User()
    resp = user.verify_token(token)
    if resp == False:
        return jsonify({'response': 'Token Invalido'})
    elif resp == 'ERRO':
        return jsonify({'response': 'Erro ao verificar token'})

    things = Things()
    response = things.search_things_inactives_by_location(loca_id)
    if response == False:
        return jsonify({'response': 'Nenhum objeto encontrado'})
    elif response == 'ERRO':
        return jsonify({'response': 'Ocorreu um erro no servidor'})
    else:
        return json.dumps(para_dict(response))


@app.route('/search_all_things_inactived/token=<string:token>', methods=['GET'])
def search_all_things_inactives(token):
    # valida token
    user = User()
    resp = user.verify_token(token)
    if resp == False:
        return jsonify({'response': 'Token Invalido'})
    elif resp == 'ERRO':
        return jsonify({'response': 'Erro ao verificar token'})

    things = Things()
    response = things.search_all_things_inactives()
    if response == False:
        return jsonify({'response': 'Nenhum objeto encontrado'})
    elif response == 'ERRO':
        return jsonify({'response': 'Ocorreu um erro no servidor'})
    else:
        return json.dumps(para_dict(response))


@app.route('/search_things_by_location/token=<string:token>&locaid=<string:loca_id>', methods=['GET'])
def search_things_by_location(token, loca_id):
    # valida token
    user = User()
    resp = user.verify_token(token)
    if resp == False:
        return jsonify({'response': 'Token Invalido'})
    elif resp == 'ERRO':
        return jsonify({'response': 'Erro ao verificar token'})

    things = Things()
    response = things.search_things_by_location(loca_id)
    if response == False:
        return jsonify({'response': 'Nenhum objeto encontrado'})
    elif response == 'ERRO':
        return jsonify({'response': 'Ocorreu um erro no servidor'})
    else:
        return json.dumps(para_dict(response))


@app.route('/active_thing_by_num/token=<string:token>&num=<string:num>', methods=['GET'])
def active_thing_by_num(token, num):
    # valida token
    user = User()
    resp = user.verify_token(token)
    if resp == False:
        return jsonify({'response': 'Token Invalido'})
    elif resp == 'ERRO':
        return jsonify({'response': 'Erro ao verificar token'})

    things = Things()
    exits = things.search_things_by_num1(num)
    if exits:
        response = things.active_things_by_num1(num)
        if response == False:
            return jsonify({'response': 'Ocorreu um erro ao ativar a etiqueta'})
        else:
            return jsonify({'response': 'true'})
    else:
        return jsonify({'response': 'Objeto nao encontrado'})


@app.route('/search_locations/token=<string:token>', methods=['GET'])
def search_locations(token):
    # valida token
    user = User()
    resp = user.verify_token(token)
    if resp == False:
        return jsonify({'response': 'Token Invalido'})
    elif resp == 'ERRO':
        return jsonify({'response': 'Erro ao verificar token'})

    things = Things()
    response = things.search_locations()
    if response == False:
        return jsonify({'response': 'Nenhuma localizacao encontrada'})
    elif response == 'ERRO':
        return jsonify({'response': 'Ocorreu um erro no servidor'})
    else:
        return json.dumps(para_dict(response))


@app.route('/search_things_missing_by_location/token=<string:token>&locaid=<string:loca_id>', methods=['GET'])
def search_things_missing_by_location(token, loca_id):
    # valida token
    user = User()
    resp = user.verify_token(token)
    if resp == False:
        return jsonify({'response': 'Token Invalido'})
    elif resp == 'ERRO':
        return jsonify({'response': 'Erro ao verificar token'})

    thingsXLocation = ThingsXLocation()
    response = thingsXLocation.search_things_missing_by_location(loca_id)
    if response == False:
        return jsonify({'response': 'Nenhum objeto encontrado'})
    elif response == 'ERRO':
        return jsonify({'response': 'Ocorreu um erro no servidor'})
    else:
        return json.dumps(para_dict(response))


@app.route('/search_things_over_by_location/token=<string:token>&locaid=<string:loca_id>', methods=['GET'])
def search_things_over_by_location(token, loca_id):
    # valida token
    user = User()
    resp = user.verify_token(token)
    if resp == False:
        return jsonify({'response': 'Token Invalido'})
    elif resp == 'ERRO':
        return jsonify({'response': 'Erro ao verificar token'})

    thingsXLocation = ThingsXLocation()
    response = thingsXLocation.search_things_over_by_location(loca_id)
    if response == False:
        return jsonify({'response': 'Nenhum objeto encontrado'})
    elif response == 'ERRO':
        return jsonify({'response': 'Ocorreu um erro no servidor'})
    else:
        return json.dumps(para_dict(response))


@app.route('/synchronize_location/token=<string:token>&locaid=<string:location>&num=<string:num_patr>', methods=['GET'])
def synchronize_location(token, location, num_patr):
    # verifica validade do token
    user = User()
    resp = user.verify_token(token)
    if resp == False:
        return jsonify({'response': 'Token Invalido'})
    elif resp == 'ERRO':
        return jsonify({'response': 'Erro ao verificar token'})
    else:
        user_id = resp.id

    thingsSynchronization = ThingsSynchronization()
    response = thingsSynchronization.synchronize_location(num_patr, location, user_id)
    if response == True:
        return jsonify({'response': 'true'})
    else:
        return jsonify({'response': response})


@app.route(
    '/edit_thing/token=<string:token>&num=<string:num_patr>&locaid=<string:location>&situation=<string:situation>&state=<string:state>&note=<string:note>',
    methods=['GET'])
def edit_things(token, num_patr, location, situation, state, note):
    # verifica validade do token
    user = User()
    resp = user.verify_token(token)
    if resp == False:
        return jsonify({'response': 'Token Invalido'})
    elif resp == 'ERRO':
        return jsonify({'response': 'Erro ao verificar token'})
    else:
        user_id = resp.id

    thingsSynchronization = ThingsSynchronization()
    response = thingsSynchronization.synchronize_things(num_patr, situation, state, note, user_id, location)
    if response == True:
        return jsonify({"response": "OK"})
    else:
        return jsonify({"response": response})


@app.route('/search_all_things_actived/token=<string:token>', methods=['GET'])
def search_all_things_actives(token):
    # valida token
    user = User()
    resp = user.verify_token(token)
    if resp == False:
        return jsonify({'response': 'Token Invalido'})
    elif resp == 'ERRO':
        return jsonify({'response': 'Erro ao verificar token'})

    things = Things()
    response = things.search_all_things_actives()
    if response == False:
        return jsonify({'response': 'Nenhum objeto encontrado'})
    elif response == 'ERRO':
        return jsonify({'response': 'Ocorreu um erro no servidor'})
    else:
        return json.dumps(para_dict(response))


# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port)
if __name__ == '__main__':
    app.run(debug=True)
