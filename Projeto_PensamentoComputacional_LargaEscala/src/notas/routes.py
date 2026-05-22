from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from src.models import Nota, Disciplina, Usuario

notas_bp = Blueprint("notas", __name__)


@notas_bp.route("/")
@login_required
def listar():
    if current_user.papel == "aluno":
        notas = Nota.query.filter_by(aluno_id=current_user.id).all()
    elif current_user.papel == "professor":
        disciplinas_ids = [d.id for d in Disciplina.query.filter_by(professor_id=current_user.id).all()]
        notas = Nota.query.filter(Nota.disciplina_id.in_(disciplinas_ids)).all()
    else:
        notas = Nota.query.all()
    return render_template("notas/listar.html", notas=notas)


@notas_bp.route("/lancar", methods=["GET", "POST"])
@login_required
def lancar():
    if current_user.papel not in ["coordenador", "professor"]:
        flash("Acesso negado.", "danger")
        return redirect(url_for("notas.listar"))
    if current_user.papel == "professor":
        disciplinas = Disciplina.query.filter_by(professor_id=current_user.id).all()
    else:
        disciplinas = Disciplina.query.all()
    alunos = Usuario.query.filter_by(papel="aluno").all()
    if request.method == "POST":
        aluno_id = request.form.get("aluno_id")
        disciplina_id = request.form.get("disciplina_id")
        nota_p1 = request.form.get("nota_p1") or None
        nota_p2 = request.form.get("nota_p2") or None
        nota_p3 = request.form.get("nota_p3") or None
        frequencia = request.form.get("frequencia", 100)
        nota = Nota.query.filter_by(aluno_id=aluno_id, disciplina_id=disciplina_id).first()
        if not nota:
            nota = Nota(aluno_id=int(aluno_id), disciplina_id=int(disciplina_id))
            db.session.add(nota)
        nota.nota_p1 = float(nota_p1) if nota_p1 else None
        nota.nota_p2 = float(nota_p2) if nota_p2 else None
        nota.nota_p3 = float(nota_p3) if nota_p3 else None
        nota.frequencia = float(frequencia)
        nota.calcular_media()
        db.session.commit()
        flash("Notas lançadas com sucesso!", "success")
        return redirect(url_for("notas.listar"))
    return render_template("notas/form.html", disciplinas=disciplinas, alunos=alunos)


@notas_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    if current_user.papel not in ["coordenador", "professor"]:
        flash("Acesso negado.", "danger")
        return redirect(url_for("notas.listar"))
    nota = Nota.query.get_or_404(id)
    if request.method == "POST":
        nota.nota_p1 = float(request.form.get("nota_p1")) if request.form.get("nota_p1") else None
        nota.nota_p2 = float(request.form.get("nota_p2")) if request.form.get("nota_p2") else None
        nota.nota_p3 = float(request.form.get("nota_p3")) if request.form.get("nota_p3") else None
        nota.frequencia = float(request.form.get("frequencia", 100))
        nota.calcular_media()
        db.session.commit()
        flash("Nota atualizada!", "success")
        return redirect(url_for("notas.listar"))
    return render_template("notas/form_editar.html", nota=nota)
