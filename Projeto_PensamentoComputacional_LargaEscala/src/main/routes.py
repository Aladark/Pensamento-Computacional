from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from src.models import Nota, Disciplina, Usuario

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("auth.login"))


@main_bp.route("/dashboard")
@login_required
def dashboard():
    contexto = {"usuario": current_user}
    if current_user.papel == "aluno":
        notas = Nota.query.filter_by(aluno_id=current_user.id).all()
        disciplinas = current_user.disciplinas
        medias = [n.media for n in notas if n.media is not None]
        media_geral = round(sum(medias) / len(medias), 2) if medias else 0
        aprovadas = len([n for n in notas if n.situacao == "Aprovado"])
        contexto.update({
            "notas": notas,
            "disciplinas": disciplinas,
            "media_geral": media_geral,
            "aprovadas": aprovadas,
            "total": len(notas),
        })
    elif current_user.papel == "professor":
        disciplinas = Disciplina.query.filter_by(professor_id=current_user.id).all()
        total_alunos = sum(len(d.alunos) for d in disciplinas)
        contexto.update({
            "disciplinas": disciplinas,
            "total_alunos": total_alunos,
        })
    else:
        total_alunos = Usuario.query.filter_by(papel="aluno").count()
        total_disciplinas = Disciplina.query.count()
        total_notas = Nota.query.count()
        contexto.update({
            "total_alunos": total_alunos,
            "total_disciplinas": total_disciplinas,
            "total_notas": total_notas,
        })
    return render_template("main/dashboard.html", **contexto)
