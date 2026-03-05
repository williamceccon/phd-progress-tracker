# 🎓 PHD Progress Tracker

> CLI profissional para rastreamento de tarefas, prazos e marcos do doutorado.

[![CI](https://github.com/williamceccon/phd-progress-tracker/actions/workflows/ci.yml/badge.svg)](https://github.com/williamceccon/phd-progress-tracker)
[![codecov](https://codecov.io/github/williamceccon/phd-progress-tracker/graph/badge.svg)](https://codecov.io/github/williamceccon/phd-progress-tracker)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://python.org)
[![Version 2.0](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/williamceccon/phd-progress-tracker)

## 📋 Sobre

Aplicação de linha de comando (CLI) e interface web para gerenciar o progresso da dissertação de doutorado e Revisão Sistemática de Literatura (RSL). Permite adicionar tarefas com prazos, acompanhar status, definir prioridades e visualizar um dashboard completo de progresso.

**Tecnologias:**
- **Backend**: Python 3.12 · FastAPI · Uvicorn
- **Frontend**: Next.js 14 · React 18 · Tailwind CSS
- **CLI**: Python 3.12 · Typer · Rich · Poetry
- **Testing**: pytest · Vitest

---

## 🚀 Quick Start (Full-Stack)

### Prerequisites

- Python 3.12+
- Node.js 18+
- [Poetry](https://python-poetry.org)
- npm or yarn

### Installation

```bash
# Clone the repository
git clone https://github.com/williamceccon/phd-progress-tracker
cd phd-progress-tracker

# Install Python dependencies
poetry install

# Install frontend dependencies
cd web
npm install

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

### Running the Application

**Terminal 1 - Backend:**
```bash
poetry run uvicorn phd_progress_tracker.api.main:app --reload
# API available at http://localhost:8000
# Swagger UI at http://localhost:8000/docs
```

**Terminal 2 - Frontend:**
```bash
cd web
npm run dev
# Frontend available at http://localhost:3000
```

---

## 💻 Web Interface

### Páginas

| Página | URL | Descrição |
|--------|-----|-----------|
| Dashboard | `/` | Visão geral com estatísticas |
| Tarefas | `/tasks` | Gerenciar tarefas |
| Marcos | `/milestones` | Gerenciar marcos |

### Funcionalidades

- ✅ Criar, editar e excluir tarefas
- ✅ Status: A Fazer, Em Progresso, Concluída, Bloqueada
- ✅ Prioridades: Baixa, Média, Alta, Crítica
- ✅ Categorias: Geral, Coleta de Dados, Análise, Escrita, Revisão
- ✅ Criar, editar e excluir marcos
- ✅ Dashboard com estatísticas em tempo real
- ✅ Prazos próximos dos próximos 7 dias

---

## 💻 CLI (Legacy)

### Instalação

```bash
poetry install
```

### Comandos

**Tarefas**

```bash
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
```

**Marcos (Milestones)**

```bash
# Adicionar marco importante
poetry run phd milestone-add "Defesa de Qualificação" --date 2026-06-01

# Visualizar dashboard completo
poetry run phd dashboard
```

### Prioridades disponíveis

| Nível | Descrição |
|-------|------------|
| LOW | Baixa prioridade |
| MEDIUM | Média prioridade (padrão) |
| HIGH | Alta prioridade |
| CRITICAL | Crítica — prazo iminente |

### Status disponíveis

| Status | Emoji | Descrição |
|--------|-------|------------|
| TODO | ⏳ | Pendente |
| IN_PROGRESS | 🔄 | Em progresso |
| COMPLETED | ✅ | Concluída |
| BLOCKED | 🚫 | Bloqueada |

---

## 🧪 Testes

### Backend Tests

```bash
# Rodar testes com cobertura
poetry run pytest tests/ -v --cov=phd_progress_tracker

# Verificar formatação e qualidade
poetry run black --check .
poetry run flake8 phd_progress_tracker/
```

### Frontend Tests

```bash
cd web

# Run tests in watch mode
npm run test

# Run tests once
npm run test:run
```

---

## 🏗️ Estrutura do Projeto

```
phd-progress-tracker/
├── phd_progress_tracker/
│   ├── api/                    # FastAPI backend
│   │   ├── main.py            # App entry point
│   │   └── routes/            # API routes
│   │       ├── tasks.py       # Tasks endpoints
│   │       ├── milestones.py  # Milestones endpoints
│   │       └── dashboard.py   # Dashboard endpoints
│   ├── cli/                   # CLI commands (Typer)
│   │   └── commands.py
│   ├── models/                # Domain models
│   │   ├── task.py
│   │   └── milestone.py
│   └── utils/                 # Utilities
│       └── database.py
├── web/                       # Next.js frontend
│   ├── app/                   # App Router pages
│   ├── components/            # React components
│   ├── lib/                  # API client, types, utils
│   ├── tests/                # Component tests
│   └── package.json
├── tests/                     # Backend tests
├── pyproject.toml
└── README.md
```

---

## 🔄 Fluxo de Desenvolvimento

```bash
git pull origin main                    # Sincroniza
git checkout -b feature/nova-feature    # Cria branch
# ... desenvolve ...
poetry run black . && poetry run pytest # Valida
git push origin feature/nova-feature     # Push
# Abre PR → CI verde → Merge
```

---

## 📄 Licença

MIT © 2026 William Ceccon
