from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from src.models import Usuario

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and bcrypt.check_password_hash(usuario.senha_hash, senha):
            login_user(usuario, remember=request.form.get("lembrar") == "on")
            next_page = request.args.get("next")
            flash(f"Bem-vindo, {usuario.nome}!", "success")
            return redirect(next_page or url_for("main.dashboard"))
        flash("Email ou senha inválidos.", "danger")
    return render_template("auth/login.html")


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")
        confirmacao = request.form.get("confirmacao", "")
        papel = request.form.get("papel", "aluno")
        if not nome or not email or not senha:
            flash("Todos os campos são obrigatórios.", "danger")
            return render_template("auth/registro.html")
        if senha != confirmacao:
            flash("As senhas não coincidem.", "danger")
            return render_template("auth/registro.html")
        if Usuario.query.filter_by(email=email).first():
            flash("Email já cadastrado.", "danger")
            return render_template("auth/registro.html")
        senha_hash = bcrypt.generate_password_hash(senha).decode("utf-8")
        usuario = Usuario(nome=nome, email=email, senha_hash=senha_hash, papel=papel)
        db.session.add(usuario)
        db.session.commit()
        flash("Conta criada com sucesso! Faça login.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/registro.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da plataforma.", "info")
    return redirect(url_for("auth.login"))
