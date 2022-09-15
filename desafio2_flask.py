from flask import Flask, jsonify, request, make_response
from desafio_sql import Autor, Postagem, app, db
from datetime import datetime, timedelta
from functools import wraps
import json
import jwt

def token_obrigatorio(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        toke = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'Mensagem':'Token nao foi incluido'}, 401)
        try:
            resultado = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            autor = Autor.query.filter_by(id_autor=resultado['id_autor']).first()
        except:
            return jsonify({'Mensagem':'Token invalido'}, 401)
        return f(autor, *args, **kwargs)
    return decorator
@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Login invalido', 401, {'WWW-Authenticate':'Basic realm="Login obrigatório"'})
    usuario = Autor.query.filter_by(nome=auth.username).first()
    if not usuario:
        return make_response('Login invalido', 401, {'WWW-Authenticate':'Basic realm="Login obrigatório"'})
    if auth.password == usuario.senha:
        token = jwt.encode({'id_autor':usuario.id_autor, 'exp':datetime.utcnow() + timedelta(minutes=30)}, app.config["SECRET_KEY"])
        return jsonify({'token':token})
    return make_response('Login invalido', 401, {'WWW-Authenticate':'Basic realm="Login obrigatório"'})
    
    
#rota padrao
@app.route('/')
@token_obrigatorio
def obter_postagens(autor):
    postagens = Postagem.query.all()
    lista_postagem = []
    for postagem in postagens:
        postagem_atual = {}
        postagem_atual['titulo'] = postagem.titulo
        postagem_atual['id_autor'] = postagem.id_autor
        lista_postagem.append(postagem_atual)
    return jsonify({'postagens':lista_postagem})


@app.route('/postagens/<int:indice>', methods=['GET'])
@token_obrigatorio
def obter_postagens_id(autor, id_postagem):
    postagens = Postagem.query.filter_by(id_postagem=id_postagem).first()
    postagem_atual = {}
    try:
        postagem_atual['titulo'] = postagens.titulo
    except:
        pass
    postagem_atual['id_autor'] = postagens.id_autor
    return jsonify({'Voce buscou pela postagem':postagem_atual})


@app.route('/postagens', methods=['POST'])
@token_obrigatorio
def nova_postagens(autor):
    nova_postagem = request.get_json()
    postagem = Postagem(titulo=nova_postagem['titulo'], id_autor=nova_postagem['id_autor'])
    db.session.add(postagem)
    db.session.commit()
    return jsonify({'Mensagem':'Postagem adicionado com sucesso'}, 200)


@app.route('/postagens/<int:indice>', methods=['PUT'])
@token_obrigatorio
def modificar_postagens(autor, id_postagem):
    modificar_postagem = request.get_json()
    postagem = Postagem.query.filter_by(id_postagem=id_postagem).first()
    if not postagem:
        return jsonify({'Mensagem':'Postagem não encontrado'})
    try:
        postagem.titulo = modificar_postagem['titulo']
    except:
        pass
    try:
        postagem.id_autor = modificar_postagem['id_autor']
    except:
        pass
    db.session.commit()
    return jsonify({'Mensagem':'Postagem modificada com sucesso'}, 200)


@app.route('/postagens/<int:indice>', methods=['DELETE'])
@token_obrigatorio
def deletar_postagens(autor, id_postagem):
    postagem = Postagem.query.filter_by(id_postagem=id_postagem).first()
    if not postagem:
        return jsonify({'Mensagem':'Postagem não encontrada'})
    db.session.delete(postagem)
    db.session.commit()


@app.route('/autores')
@token_obrigatorio
def obter_autores(autor):
    autores = Autor.query.all()
    lista_autores = []
    for autor in autores:
        autor_atual = {}
        autor_atual['id_autor'] = autor.id_autor
        autor_atual['nome'] = autor.nome
        autor_atual['email'] = autor.email
        lista_autores.append(autor_atual)
    return jsonify({'Autores':lista_autores})


@app.route('/autores/<int:id_autor>', methods=['GET'])
@token_obrigatorio
def obter_autores_id(autor, id_autor):
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor:
        return jsonify({'Mensagem':'Autor não encontrado'})
    autor_atual = {}
    autor_atual['id_autor'] = autor.id_autor
    autor_atual['nome'] = autor.nome
    autor_atual['email'] = autor.email
    return jsonify({'Voce buscou pelo Autor':autor_atual})


@app.route('/autores', methods=['POST'])
@token_obrigatorio
def novos_autores(autor):
    novo_autor = request.get_json()
    autor = Autor(nome=novo_autor['nome'], senha=novo_autor['senha'], email=novo_autor['email'], )
    db.session.add(autor)
    db.session.commit()
    return jsonify({'Mensagem':'Autor adicionado com sucesso'}, 200)


@app.route('/autores/<int:id_autor>', methods=['PUT'])
@token_obrigatorio
def modificar_autores(autor, id_autor):
    modificar_autor = request.get_json()
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor:
        return jsonify({'Mensagem':'Autor não encontrado'})
    try:
        if modificar_autor ['nome']:
            autor.nome = modificar_autor ['nome']
    except:
        pass
    try:
        if modificar_autor ['email']:
            autor.nome = modificar_autor ['email']
    except:
        pass
    try:
        if modificar_autor ['senha']:
            autor.nome = modificar_autor ['senha']
    except:
        pass
    db.session.commit()
    return jsonify({'Mensagem':'Autor modificado com sucesso'}, 200)

@app.route('/autores/<int:id_autor>', methods=['DELETE'])
@token_obrigatorio
def deletar_autores(autor, id_autor):
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor:
        return jsonify({'Mensagem':'Autor não encontrado'})
    db.session.delete(autor)
    db.session.commit()
    
    return jsonify({'Mensagem':'Autor deletado com sucesso'}, 200)


app.run(port=5002, host='localhost', debug=True)