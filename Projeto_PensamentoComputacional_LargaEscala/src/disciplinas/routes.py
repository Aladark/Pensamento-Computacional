from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from src.models import Disciplina, Usuario, Nota

disciplinas_bp = Blueprint("disciplinas", __name__)


@disciplinas_bp.route("/")
@login_required
def listar():
    if current_user.papel in ["coordenador", "professor"]:
        disciplinas = Disciplina.query.all()
    else:
        disciplinas = current_user.disciplinas
    return render_template("disciplinas/listar.html", disciplinas=disciplinas)


@disciplinas_bp.route("/nova", methods=["GET", "POST"])
@login_required
def nova():
    if current_user.papel not in ["coordenador", "professor"]:
        flash("Acesso negado.", "danger")
        return redirect(url_for("disciplinas.listar"))
    professores = Usuario.query.filter_by(papel="professor").all()
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        codigo = request.form.get("codigo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        carga_horaria = request.form.get("carga_horaria", 60)
        professor_id = request.form.get("professor_id")
        if not nome or not codigo:
            flash("Nome e código são obrigatórios.", "danger")
            return render_template("disciplinas/form.html", professores=professores)
        if Disciplina.query.filter_by(codigo=codigo).first():
            flash("Código já existe.", "danger")
            return render_template("disciplinas/form.html", professores=professores)
        disciplina = Disciplina(
            nome=nome,
            codigo=codigo,
            descricao=descricao,
            carga_horaria=int(carga_horaria),
            professor_id=int(professor_id) if professor_id else None,
        )
        db.session.add(disciplina)
        db.session.commit()
        flash("Disciplina criada com sucesso!", "success")
        return redirect(url_for("disciplinas.listar"))
    return render_template("disciplinas/form.html", professores=professores)


@disciplinas_bp.route("/<int:id>")
@login_required
def detalhe(id):
    disciplina = Disciplina.query.get_or_404(id)
    notas = Nota.query.filter_by(disciplina_id=id).all()
    return render_template("disciplinas/detalhe.html", disciplina=disciplina, notas=notas)


@disciplinas_bp.route("/matricular/<int:id>", methods=["POST"])
@login_required
def matricular(id):
    if current_user.papel != "aluno":
        flash("Apenas alunos podem se matricular.", "danger")
        return redirect(url_for("disciplinas.listar"))
    disciplina = Disciplina.query.get_or_404(id)
    if disciplina in current_user.disciplinas:
        flash("Você já está matriculado nesta disciplina.", "warning")
    else:
        current_user.disciplinas.append(disciplina)
        db.session.commit()
        flash(f"Matriculado em {disciplina.nome}!", "success")
    return redirect(url_for("disciplinas.listar"))
