# 🐞 Erros Identificados

## 1. Sintaxe
- Ausência de `fimalgoritmo` em alguns pseudocódigos iniciais.
- Estrutura de importação em Flask sem tratamento de exceções.

## 2. Lógica
- `db.create_all()` sendo chamado diretamente no `create_app`, sem migrações adequadas (ideal seria usar Flask-Migrate).
- `seed_data()` executado sempre que a aplicação inicia → risco de duplicação de dados.

## 3. Execução
- Variáveis de ambiente não configuradas corretamente podem quebrar a aplicação.
- Dependências não listadas em `requirements.txt`.
