# Festa IFC - Campus Blumenau

Este projeto é uma aplicação web desenvolvida com Streamlit para organizar a festa do IFC Campus Blumenau. O sistema permite cadastrar e gerenciar os principais itens da festa: alimentos, fornecedores de insumos, pessoas que irão atuar no evento e preços de venda dos alimentos.

## Objetivo

Os estudantes precisam decidir:

- quais alimentos serão vendidos;
- quem vai fornecer os insumos;
- quais pessoas vão trabalhar na festa (alunos, pais de alunos e servidores);
- qual será o preço de venda dos alimentos.

O sistema centraliza essas decisões em um painel simples e funcional, com persistência em banco de dados.

## Tecnologias utilizadas

- Streamlit
- SQLAlchemy
- SQLite para testes locais
- MySQL para produção
- uv como gerenciador de pacotes

## Estrutura do projeto

```text
friendly-robot/
├── .env.example
├── .gitignore
├── README.md
├── pyproject.toml
└── src/
    ├── __init__.py
    ├── app.py
    ├── crud.py
    ├── database.py
    └── models.py
```

## Requisitos

- Python 3.11+
- uv

## Instalação

No diretório do projeto, execute:

```bash
uv sync
```

## Configuração de ambiente

Crie um arquivo `.env` com base no exemplo abaixo:

```bash
cp .env.example .env
```

Conteúdo do `.env`:

```env
USE_MYSQL=false
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=festa_ifc
MYSQL_USER=root
MYSQL_PASSWORD=sua_senha
```

Se `USE_MYSQL=false`, a aplicação usa SQLite local para testes.
Se `USE_MYSQL=true`, a aplicação usa o banco MySQL configurado nas variáveis acima.

## Execução local

```bash
uv run python -m streamlit run src/app.py
```

Acesse a URL indicada no terminal, normalmente:

```text
http://localhost:8501
```

## Implantação no Streamlit Community Cloud

Para deploy no Streamlit Cloud, configure as variáveis de ambiente no painel do projeto:

- `USE_MYSQL`
- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`

Dessa forma, a aplicação usará MySQL em produção e SQLite em desenvolvimento local.

## Funcionalidades do sistema

- Cadastro de alimentos
- Cadastro de fornecedores
- Cadastro de pessoas envolvidas na festa
- Definição de preços de venda
- Associação entre alimentos e fornecedores
- CRUD completo para cada entidade
- Persistência com SQLite e MySQL
