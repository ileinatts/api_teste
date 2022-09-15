from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = "123456789"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"

db = SQLAlchemy(app)
db:SQLAlchemy

class Postagem(db.Model):
    __tablename__ = 'Postagem'
    id_postagem = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String)
    id_autor = db.Column(db.Integer, db.ForeignKey('Autor.id_autor'))


class Autor(db.Model):
    __tablename__ = 'Autor'
    id_autor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    email = db.Column(db.String)
    senha = db.Column(db.String)
    admin = db.Column(db.Boolean)
    postagens = db.relationship('Postagem')

def inicializar_banco():    
    db.drop_all()
    db.create_all()

    autor1 = Autor(nome='Iago', email='iagols@gmail.com', senha='12345', admin=True)
    
    
    db.session.add(autor1)
    db.session.commit()
    
    
if __name__ == '__main__':
    inicializar_banco()
