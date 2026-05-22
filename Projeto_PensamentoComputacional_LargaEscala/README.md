# Pensamento-Computacional

# 🎓 Plataforma Acadêmica Inteligente

> Projeto desenvolvido como parte da disciplina **Pensamento Computacional** no curso de **Engenharia de Software**,
> sob orientação da **Profa. Kadidja Valéria**.

**Autor:** Francisco Alano
**Disciplina:** Pensamento Computacional
**Curso:** Engenharia de Software

---

## 📌 Sobre o Projeto

Este projeto foi desenvolvido com o objetivo de aplicar os conceitos de pensamento computacional e engenharia de software na concepção de um sistema de larga escala, explorando decomposição, abstração, reconhecimento de padrões e algoritmos na prática.

A **Plataforma Acadêmica Inteligente (PAI)** é uma aplicação web para gestão acadêmica que integra autenticação de usuários, gerenciamento de disciplinas e notas, um sistema de recomendações personalizadas baseado em IA e um painel de relatórios para coordenação.

---

## 🎯 Objetivos

- Relacionar engenharia de software e pensamento computacional.
- Reconhecer princípios e padrões relevantes para sistemas de larga escala.
- Identificar dificuldades reais no desenvolvimento de aplicações complexas.
- Aplicar metodologias ágeis no planejamento e execução do projeto.

---

## 🧠 Pensamento Computacional Aplicado

### Decomposição
O sistema foi dividido em módulos independentes e coesos:

- **Autenticação** — cadastro, login e controle de sessão com papéis (aluno, professor, coordenador)
- **Gestão de Disciplinas** — cadastro, matrícula e visualização de turmas
- **Gestão de Notas** — lançamento de P1/P2/P3, frequência e cálculo automático de média e situação
- **Recomendações Inteligentes** — análise de perfil acadêmico e geração de alertas personalizados
- **Relatórios** — painel estatístico com média de turma, desvio padrão e percentual de aprovação

### Reconhecimento de Padrões
- O módulo de autenticação segue padrões de sistemas bancários: hash de senha (bcrypt), controle de sessão e restrição de acesso por papel.
- A estrutura de notas foi inspirada em LMS consolidados como Blackboard e Moodle, com suporte a múltiplas avaliações, frequência e situação final.
- O painel de recomendações identifica padrões de risco acadêmico (média baixa, frequência crítica, disciplinas em recuperação) para gerar alertas direcionados.

### Abstração
O sistema abstrai a complexidade de cada módulo por trás de interfaces simples:

- Um modelo `Nota` encapsula todo o cálculo de média e situação final.
- O motor de recomendações abstrai a análise estatística (média, desvio, frequência) em alertas compreensíveis para o usuário.
- A camada de blueprints do Flask separa responsabilidades sem expor detalhes internos entre módulos.

### Algoritmos
- **Cálculo de média:** média aritmética das provas P1, P2 e P3 com regra de frequência mínima de 75%.
- **Classificação de situação:** Aprovado (≥ 7,0), Recuperação (5,0–6,9), Reprovado (< 5,0), Reprovado por Falta (frequência < 75%).
- **Recomendações personalizadas:** análise de perfil via `numpy` — calcula média geral, frequência média, disciplinas em risco e sugere novas matrículas para alunos com bom desempenho.

---

## 🛠️ Metodologia de Desenvolvimento

**Metodologia:** Scrum  
**Sprints:** ciclos de 2 semanas  
**Ferramentas:** GitHub Projects · Issues · Kanban

| Sprint | Entregável |
|--------|-----------|
| 1 | Modelagem do banco de dados, autenticação e estrutura base |
| 2 | Módulo de disciplinas e notas com cálculo automático |
| 3 | Motor de recomendações IA e painel de relatórios |
| 4 | Refinamento, testes e documentação |

---

## ⚠️ Desafios Identificados

| Desafio | Abordagem Adotada |
|--------|-------------------|
| Escalabilidade para múltiplos usuários simultâneos | Uso do padrão Application Factory do Flask, separação em blueprints e banco relacional via SQLAlchemy |
| Segurança de dados sensíveis | Hash de senhas com bcrypt, controle de acesso por papel, princípios de Saltzer & Schroeder |
| Integração com sistemas externos | Arquitetura modular preparada para integração via APIs REST |
| Consistência dos dados acadêmicos | Cálculo de média e situação centralizado no modelo `Nota`, evitando duplicação de lógica |

---

## 🗂️ Estrutura do Repositório

```
Projeto_PensamentoComputacional_LargaEscala/
│
├── app.py                          # Fábrica da aplicação Flask
├── requirements.txt                # Dependências do projeto
├── README.md                       # Documentação principal
│
└── src/
    ├── models.py                   # Modelos de dados (SQLAlchemy)
    ├── seed.py                     # Dados iniciais para demonstração
    │
    ├── auth/
    │   └── routes.py               # Autenticação: login, registro, logout
    ├── disciplinas/
    │   └── routes.py               # CRUD de disciplinas e matrículas
    ├── notas/
    │   └── routes.py               # Lançamento e edição de notas
    ├── recomendacoes/
    │   └── routes.py               # Motor de recomendações inteligentes
    ├── relatorios/
    │   └── routes.py               # Painel de relatórios e estatísticas
    ├── main/
    │   └── routes.py               # Dashboard principal
    │
    └── templates/                  # Templates HTML (Jinja2 + Bootstrap 5)
        ├── base.html
        ├── auth/
        ├── disciplinas/
        ├── notas/
        ├── recomendacoes/
        ├── relatorios/
        └── main/
```

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.10 ou superior

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/Projeto_PensamentoComputacional_LargaEscala.git
cd Projeto_PensamentoComputacional_LargaEscala

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python app.py
```

Acesse em: [http://localhost:]

> O banco de dados SQLite e os dados de demonstração são criados automaticamente na primeira execução.

---

## 🔐 Credenciais de Demonstração

| Perfil | E-mail | Senha |
|--------|--------|-------|
| Coordenador | admin@plataforma.edu | admin123 |
| Professor | ana.souza@plataforma.edu | prof123 |
| Aluno | maria.silva@aluno.edu | aluno123 |

---

## 🧰 Tecnologias Utilizadas

- **Python 3** — linguagem principal
- **Flask** — framework web
- **SQLAlchemy** — ORM para banco de dados relacional
- **Flask-Login** — gerenciamento de sessão e autenticação
- **Flask-Bcrypt** — hash seguro de senhas
- **NumPy** — cálculos estatísticos no motor de recomendações
- **Bootstrap 5** — interface responsiva
- **SQLite** — banco de dados (desenvolvimento)

---

## 📄 Licença

Projeto acadêmico desenvolvido para fins educacionais.
