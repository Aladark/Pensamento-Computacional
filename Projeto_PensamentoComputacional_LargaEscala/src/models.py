from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


matricula_disciplina = db.Table(
    "matricula_disciplina",
    db.Column("usuario_id", db.Integer, db.ForeignKey("usuario.id")),
    db.Column("disciplina_id", db.Integer, db.ForeignKey("disciplina.id")),
)


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)
    papel = db.Column(db.String(20), nullable=False, default="aluno")
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    disciplinas = db.relationship("Disciplina", secondary=matricula_disciplina, backref="alunos")
    notas = db.relationship("Nota", backref="aluno", lazy=True)

    def __repr__(self):
        return f"<Usuario {self.email}>"


class Disciplina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    descricao = db.Column(db.Text)
    carga_horaria = db.Column(db.Integer, nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    professor = db.relationship("Usuario", foreign_keys=[professor_id])
    notas = db.relationship("Nota", backref="disciplina", lazy=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Disciplina {self.codigo}>"


class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    disciplina_id = db.Column(db.Integer, db.ForeignKey("disciplina.id"), nullable=False)
    nota_p1 = db.Column(db.Float)
    nota_p2 = db.Column(db.Float)
    nota_p3 = db.Column(db.Float)
    frequencia = db.Column(db.Float, default=100.0)
    media = db.Column(db.Float)
    situacao = db.Column(db.String(20))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def calcular_media(self):
        notas_validas = [n for n in [self.nota_p1, self.nota_p2, self.nota_p3] if n is not None]
        if not notas_validas:
            return None
        self.media = sum(notas_validas) / len(notas_validas)
        if self.frequencia < 75:
            self.situacao = "Reprovado por Falta"
        elif self.media >= 7.0:
            self.situacao = "Aprovado"
        elif self.media >= 5.0:
            self.situacao = "Recuperação"
        else:
            self.situacao = "Reprovado"
        return self.media

    def __repr__(self):
        return f"<Nota aluno={self.aluno_id} disciplina={self.disciplina_id}>"
