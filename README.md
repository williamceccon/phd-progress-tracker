# 🎓 PHD Progress Tracker

> CLI profissional para rastreamento de tarefas, prazos e marcos do doutorado.

![Coverage](https://codecov.io/gh/williamceccon/phd-progress-tracker/badge.svg)
[![CI](https://github.com/williamceccon/phd-progress-tracker/actions/workflows/ci.yml/badge.svg)](https://github.com/williamceccon/phd-progress-tracker/actions)
[![codecov](https://codecov.io/github/williamceccon/phd-progress-tracker/graph/badge.svg?token=4O3ZS4D9BA)](https://codecov.io/github/williamceccon/phd-progress-tracker)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://python.org)

## 📋 Sobre

Aplicação de linha de comando (CLI) para gerenciar o progresso da dissertação de doutorado e Revisão Sistemática de Literatura (RSL). Permite adicionar tarefas com prazos, acompanhar status, definir prioridades e visualizar um dashboard completo de progresso.

**Tecnologias:** Python 3.12 · Typer · Rich · Poetry · pytest

## ⚙️ Instalação

**Pré-requisitos:** Python 3.12+, [Poetry](https://python-poetry.org)

```bash
git clone https://github.com/williamceccon/phd-progress-tracker
cd phd-progress-tracker
poetry install

🚀 **Comandos**

Tarefas

# Adicionar tarefa
poetry run phd add "Revisar literatura" --deadline 2026-03-01 --category "RSL"
poetry run phd add "Análise de dados" --deadline +14d --priority HIGH

# Listar tarefas (com filtros opcionais)
poetry run phd list
poetry run phd list --status TODO
poetry run phd list --category "RSL"

# Editar tarefa pelo ID
poetry run phd edit <id> --title "Novo título"
poetry run phd edit <id> --deadline 2026-06-30
poetry run phd edit <id> -t "Revisar Cap. 3" -d "+7d"

# Concluir tarefa
poetry run phd complete <id>

Marcos (Milestones)

# Adicionar marco importante
poetry run phd milestone-add "Defesa de Qualificação" --date 2026-06-01

# Visualizar dashboard completo
poetry run phd dashboard

Prioridades disponíveis

Nível	Descrição
LOW	Baixa prioridade
MEDIUM	Média prioridade (padrão)
HIGH	Alta prioridade
CRITICAL	Crítica — prazo iminente
Status disponíveis

Status	Emoji	Descrição
TODO	⏳	Pendente
IN_PROGRESS	🔄	Em progresso
COMPLETED	✅	Concluída
BLOCKED	🚫	Bloqueada

🧪 **Testes**

# Rodar testes com cobertura
poetry run pytest tests/ -v --cov=phd_progress_tracker

# Verificar formatação e qualidade
poetry run black --check .
poetry run flake8 phd_progress_tracker/

🏗️ **Estrutura do Projeto**

phd-progress-tracker/
├── phd_progress_tracker/
│   ├── cli/
│   │   └── commands.py      # Comandos CLI (add, list, edit, complete, dashboard)
│   ├── models/
│   │   ├── task.py          # Modelo de tarefa
│   │   └── milestone.py     # Modelo de marco
│   └── utils/
│       ├── database.py      # Persistência JSON
│       └── date_helper.py   # Helpers de data
├── tests/
├── pyproject.toml
└── README.md

🔄 **Fluxo de Desenvolvimento**

git pull origin main                    # Sincroniza
git checkout -b feature/nova-feature    # Cria branch
# ... desenvolve ...
poetry run black . && poetry run pytest # Valida
git push origin feature/nova-feature   # Push
# Abre PR → CI verde → Merge

📄 **Licença**
MIT © 2026 William Ceccon
