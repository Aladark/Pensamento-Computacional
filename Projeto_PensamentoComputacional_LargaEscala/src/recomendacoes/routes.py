from flask import Blueprint, render_template
from flask_login import login_required, current_user
from src.models import Nota, Disciplina, Usuario
import numpy as np

recomendacoes_bp = Blueprint("recomendacoes", __name__)


def calcular_perfil_aluno(aluno_id):
    notas = Nota.query.filter_by(aluno_id=aluno_id).all()
    if not notas:
        return None, []
    medias = [n.media for n in notas if n.media is not None]
    frequencias = [n.frequencia for n in notas if n.frequencia is not None]
    media_geral = np.mean(medias) if medias else 0
    media_freq = np.mean(frequencias) if frequencias else 0
    reprovadas = [n for n in notas if n.situacao in ["Reprovado", "Reprovado por Falta"]]
    recuperacao = [n for n in notas if n.situacao == "Recuperação"]
    return {
        "media_geral": round(media_geral, 2),
        "media_frequencia": round(media_freq, 2),
        "total_disciplinas": len(notas),
        "reprovadas": len(reprovadas),
        "recuperacao": len(recuperacao),
        "aprovadas": len([n for n in notas if n.situacao == "Aprovado"]),
    }, notas


def gerar_recomendacoes(perfil, notas):
    recomendacoes = []
    if not perfil:
        return [{"tipo": "info", "titulo": "Sem dados", "mensagem": "Nenhuma nota registrada ainda."}]

    if perfil["media_geral"] < 5.0:
        recomendacoes.append({
            "tipo": "danger",
            "titulo": "Atenção ao Desempenho",
            "mensagem": f"Sua média geral está em {perfil['media_geral']:.1f}. Procure apoio com monitores e professores com urgência.",
        })
    elif perfil["media_geral"] < 7.0:
        recomendacoes.append({
            "tipo": "warning",
            "titulo": "Melhore seu Desempenho",
            "mensagem": f"Média geral {perfil['media_geral']:.1f}. Revise os conteúdos das disciplinas com nota abaixo de 7.",
        })
    else:
        recomendacoes.append({
            "tipo": "success",
            "titulo": "Excelente Desempenho!",
            "mensagem": f"Parabéns! Média geral {perfil['media_geral']:.1f}. Continue assim e considere a monitoria.",
        })

    if perfil["media_frequencia"] < 75:
        recomendacoes.append({
            "tipo": "danger",
            "titulo": "Frequência Crítica",
            "mensagem": f"Frequência média de {perfil['media_frequencia']:.1f}%. Abaixo de 75% leva a reprovação automática.",
        })
    elif perfil["media_frequencia"] < 85:
        recomendacoes.append({
            "tipo": "warning",
            "titulo": "Atenção à Frequência",
            "mensagem": f"Frequência média {perfil['media_frequencia']:.1f}%. Mantenha presença acima de 85% para segurança.",
        })

    for nota in notas:
        if nota.situacao == "Recuperação":
            recomendacoes.append({
                "tipo": "warning",
                "titulo": f"Recuperação: {nota.disciplina.nome}",
                "mensagem": f"Média atual {nota.media:.1f}. Você precisa de pelo menos 7.0 na recuperação para ser aprovado.",
            })
        elif nota.situacao == "Reprovado por Falta":
            recomendacoes.append({
                "tipo": "danger",
                "titulo": f"Reprovado por Falta: {nota.disciplina.nome}",
                "mensagem": f"Frequência {nota.frequencia:.1f}% está abaixo do mínimo. Consulte a coordenação.",
            })

    disciplinas_matriculadas_ids = set()
    for nota in notas:
        disciplinas_matriculadas_ids.add(nota.disciplina_id)

    todas = Disciplina.query.all()
    disponiveis = [d for d in todas if d.id not in disciplinas_matriculadas_ids]
    if disponiveis and perfil["media_geral"] >= 7.0:
        nomes = ", ".join([d.nome for d in disponiveis[:3]])
        recomendacoes.append({
            "tipo": "info",
            "titulo": "Disciplinas Sugeridas",
            "mensagem": f"Com seu bom desempenho, considere se matricular em: {nomes}.",
        })

    return recomendacoes


@recomendacoes_bp.route("/")
@login_required
def index():
    if current_user.papel == "aluno":
        perfil, notas = calcular_perfil_aluno(current_user.id)
        recomendacoes = gerar_recomendacoes(perfil, notas)
        return render_template("recomendacoes/index.html", perfil=perfil, recomendacoes=recomendacoes)

    if current_user.papel in ["coordenador", "professor"]:
        alunos = Usuario.query.filter_by(papel="aluno").all()
        dados_alunos = []
        for aluno in alunos:
            perfil, notas = calcular_perfil_aluno(aluno.id)
            if perfil:
                dados_alunos.append({"aluno": aluno, "perfil": perfil})
        return render_template("recomendacoes/coordenador.html", dados_alunos=dados_alunos)

    return render_template("recomendacoes/index.html", perfil=None, recomendacoes=[])
