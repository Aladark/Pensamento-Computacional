from flask import Blueprint, render_template, make_response
from flask_login import login_required, current_user
from src.models import Nota, Disciplina, Usuario
import numpy as np

relatorios_bp = Blueprint("relatorios", __name__)


def estatisticas_disciplina(disciplina_id):
    notas = Nota.query.filter_by(disciplina_id=disciplina_id).all()
    if not notas:
        return None
    medias = [n.media for n in notas if n.media is not None]
    if not medias:
        return None
    aprovados = len([n for n in notas if n.situacao == "Aprovado"])
    reprovados = len([n for n in notas if n.situacao in ["Reprovado", "Reprovado por Falta"]])
    recuperacao = len([n for n in notas if n.situacao == "Recuperação"])
    return {
        "total": len(notas),
        "media_turma": round(np.mean(medias), 2),
        "maior_nota": round(max(medias), 2),
        "menor_nota": round(min(medias), 2),
        "desvio_padrao": round(float(np.std(medias)), 2),
        "aprovados": aprovados,
        "reprovados": reprovados,
        "recuperacao": recuperacao,
        "percentual_aprovacao": round(aprovados / len(notas) * 100, 1) if notas else 0,
    }


@relatorios_bp.route("/")
@login_required
def index():
    if current_user.papel not in ["coordenador", "professor"]:
        from flask import flash, redirect, url_for
        flash("Acesso restrito.", "danger")
        return redirect(url_for("main.dashboard"))
    disciplinas = Disciplina.query.all()
    relatorios = []
    for d in disciplinas:
        stats = estatisticas_disciplina(d.id)
        if stats:
            relatorios.append({"disciplina": d, "stats": stats})
    total_alunos = Usuario.query.filter_by(papel="aluno").count()
    total_disciplinas = Disciplina.query.count()
    todas_notas = Nota.query.all()
    medias_geral = [n.media for n in todas_notas if n.media is not None]
    media_plataforma = round(np.mean(medias_geral), 2) if medias_geral else 0
    aprovados_total = len([n for n in todas_notas if n.situacao == "Aprovado"])
    return render_template(
        "relatorios/index.html",
        relatorios=relatorios,
        total_alunos=total_alunos,
        total_disciplinas=total_disciplinas,
        media_plataforma=media_plataforma,
        aprovados_total=aprovados_total,
        total_notas=len(todas_notas),
    )


@relatorios_bp.route("/aluno/<int:aluno_id>")
@login_required
def aluno(aluno_id):
    if current_user.papel == "aluno" and current_user.id != aluno_id:
        from flask import flash, redirect, url_for
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.dashboard"))
    aluno = Usuario.query.get_or_404(aluno_id)
    notas = Nota.query.filter_by(aluno_id=aluno_id).all()
    medias = [n.media for n in notas if n.media is not None]
    media_geral = round(np.mean(medias), 2) if medias else 0
    return render_template("relatorios/aluno.html", aluno=aluno, notas=notas, media_geral=media_geral)
