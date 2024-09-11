from database import db

class Livro(db.Model):
    __tablename__= "livro"
    id_livro = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(100))
    autor = db.Column(db.String(100))
    ano_publicacao = db.Column(db.Integer)

    def __init__(self, titulo, autor, ano_publicacao):
        self.titulo = titulo
        self.autor = autor
        self.ano_publicacao = ano_publicacao

    def __repr__(self):
        return "<Livro {}>".format(self.titulo)