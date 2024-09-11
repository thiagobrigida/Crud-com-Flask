#pip install flask
#pip install Flask-SQLAlchemy
#pip install Flask-Migrate
#pip install Flask-Script
#pip install pymysql
#flask db init
#flask db migrate -m "Migração inicial"
#flask db upgrade
#flask run --debug "rodar o site"

from flask import Flask, render_template, request, flash, redirect
app = Flask(__name__)
from database import db
from flask_migrate import Migrate
from models import Livro
app.config['SECRET_KEY'] = '23ttnd4gnd55y-23md98'

#drive://usuario:senha@servidor/banco_de_dados
conexao = "mysql+pymysql://alunos:cefetmg@127.0.0.1/livros"
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('index.html')
5
@app.route('/biblioteca')
@app.route('/biblioteca/<titulo>')
@app.route('/biblioteca/<titulo>/<autor>')
@app.route('/biblioteca/<titulo>/<autor>/<int:ano_publicacao>')
def biblioteca(titulo = 'A morte de Ivan Ilitch', autor = 'Lev Tolstói', ano_publicacao = 1886):
    dados = {'titulo':titulo,'autor':autor, 'ano_publicacao':ano_publicacao}
    return render_template('biblioteca.html',dados_autor = dados)

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/dados', methods=['POST'])
def dados():
    flash('Dados ')
    dados = request.form
    return render_template('dados.html', dados=dados)

@app.route('/livro')
def livro():
    u = Livro.query.all()
    return render_template('livro_lista.html', dados = u)

@app.route('/livro/add')
def livro_add():
    return render_template('livro_add.html')

@app.route('/livro/save', methods=['POST'])
def livro_save():
    titulo = request.form.get('titulo')
    autor = request.form.get('autor')
    ano_publicacao = request.form.get('ano_publicacao')
    if titulo and autor and ano_publicacao:
        livro = Livro(titulo, autor, ano_publicacao)
        db.session.add(livro)
        db.session.commit()
        flash('Livro cadastrado com sucesso!!!')
        return redirect('/livro')
    else:
        flash('Preencha todos os campos')
        return redirect ('/livro/add')

@app.route('/livro/remove/<int:id_livro>')
def livro_remove(id_livro):
    livro = Livro.query.get(id_livro)
    if livro:
        db.session.delete(livro)
        db.session.commit()
        flash('Livro removido com sucesso!')
        return redirect('/livro')
    else:
        flash('Caminho Incorreto!')
        return redirect('/livro')

@app.route('/livro/edita/<int:id_livro>')
def livro_edita(id_livro):
    livro = Livro.query.get(id_livro)
    return render_template('livro_edita.html', dados = livro)    

@app.route('/livro/edita/save', methods=['POST'])
def livro_edita_save():
    titulo = request.form.get('titulo')
    autor = request.form.get('autor')
    ano_publicacao = request.form.get('ano_publicacao')
    id_livro = request.form.get('id_livro')
    if id_livro and titulo and autor and ano_publicacao:
        livro = Livro.query.get(id_livro)
        livro.titulo = titulo
        livro.autor = autor
        livro.ano_publicacao = ano_publicacao
        db.session.commit()
        flash('Dados atualizados com sucesso!!')
        return redirect('/livro')
    else:
        flash('Faltando dados!')
        return redirect('/livro')


if __name__ == '__main__':
    app.run()

