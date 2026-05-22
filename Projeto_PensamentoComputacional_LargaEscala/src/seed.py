from src.models import Usuario, Disciplina, Nota
from app import db, bcrypt


def seed_data():
    if Usuario.query.first():
        return

    admin = Usuario(
        nome="Coordenador Admin",
        email="admin@plataforma.edu",
        senha_hash=bcrypt.generate_password_hash("admin123").decode("utf-8"),
        papel="coordenador",
    )
    prof1 = Usuario(
        nome="Prof. Ana Souza",
        email="ana.souza@plataforma.edu",
        senha_hash=bcrypt.generate_password_hash("prof123").decode("utf-8"),
        papel="professor",
    )
    prof2 = Usuario(
        nome="Prof. Carlos Lima",
        email="carlos.lima@plataforma.edu",
        senha_hash=bcrypt.generate_password_hash("prof123").decode("utf-8"),
        papel="professor",
    )
    aluno1 = Usuario(
        nome="Maria Silva",
        email="maria.silva@aluno.edu",
        senha_hash=bcrypt.generate_password_hash("aluno123").decode("utf-8"),
        papel="aluno",
    )
    aluno2 = Usuario(
        nome="João Costa",
        email="joao.costa@aluno.edu",
        senha_hash=bcrypt.generate_password_hash("aluno123").decode("utf-8"),
        papel="aluno",
    )
    aluno3 = Usuario(
        nome="Lucia Fernandes",
        email="lucia.fernandes@aluno.edu",
        senha_hash=bcrypt.generate_password_hash("aluno123").decode("utf-8"),
        papel="aluno",
    )

    db.session.add_all([admin, prof1, prof2, aluno1, aluno2, aluno3])
    db.session.flush()

    d1 = Disciplina(nome="Algoritmos e Estruturas de Dados", codigo="AED001", carga_horaria=80, professor_id=prof1.id, descricao="Fundamentos de algoritmos e estruturas básicas.")
    d2 = Disciplina(nome="Banco de Dados", codigo="BD001", carga_horaria=60, professor_id=prof1.id, descricao="Modelagem e consultas SQL.")
    d3 = Disciplina(nome="Engenharia de Software", codigo="ES001", carga_horaria=60, professor_id=prof2.id, descricao="Metodologias ágeis e padrões de projeto.")
    d4 = Disciplina(nome="Inteligência Artificial", codigo="IA001", carga_horaria=80, professor_id=prof2.id, descricao="Machine learning e redes neurais.")
    d5 = Disciplina(nome="Redes de Computadores", codigo="RC001", carga_horaria=60, professor_id=prof1.id, descricao="Protocolos e arquitetura de redes.")

    db.session.add_all([d1, d2, d3, d4, d5])
    db.session.flush()

    aluno1.disciplinas = [d1, d2, d3, d4]
    aluno2.disciplinas = [d1, d2, d5]
    aluno3.disciplinas = [d3, d4, d5]

    notas = [
        Nota(aluno_id=aluno1.id, disciplina_id=d1.id, nota_p1=8.5, nota_p2=7.0, nota_p3=9.0, frequencia=90),
        Nota(aluno_id=aluno1.id, disciplina_id=d2.id, nota_p1=6.0, nota_p2=5.5, nota_p3=7.0, frequencia=85),
        Nota(aluno_id=aluno1.id, disciplina_id=d3.id, nota_p1=9.0, nota_p2=8.5, nota_p3=9.5, frequencia=95),
        Nota(aluno_id=aluno1.id, disciplina_id=d4.id, nota_p1=4.0, nota_p2=5.0, nota_p3=6.0, frequencia=80),
        Nota(aluno_id=aluno2.id, disciplina_id=d1.id, nota_p1=7.0, nota_p2=8.0, nota_p3=7.5, frequencia=88),
        Nota(aluno_id=aluno2.id, disciplina_id=d2.id, nota_p1=9.5, nota_p2=9.0, nota_p3=9.8, frequencia=100),
        Nota(aluno_id=aluno2.id, disciplina_id=d5.id, nota_p1=5.0, nota_p2=4.5, nota_p3=6.0, frequencia=70),
        Nota(aluno_id=aluno3.id, disciplina_id=d3.id, nota_p1=7.5, nota_p2=8.0, nota_p3=7.0, frequencia=92),
        Nota(aluno_id=aluno3.id, disciplina_id=d4.id, nota_p1=6.5, nota_p2=7.0, nota_p3=8.0, frequencia=87),
        Nota(aluno_id=aluno3.id, disciplina_id=d5.id, nota_p1=3.0, nota_p2=4.0, nota_p3=4.5, frequencia=65),
    ]

    for nota in notas:
        nota.calcular_media()

    db.session.add_all(notas)
    db.session.commit()
