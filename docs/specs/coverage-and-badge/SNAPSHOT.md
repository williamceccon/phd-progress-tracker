# SNAPSHOT — coverage-and-badge

### Feature
Implementa infraestrutura de CI/CD com 100% de coverage de testes, integracao com Codecov e badge visual no README.

### Decisions Made
- **Pragma no cover no entry point**: Decisao de marcar `if __name__ == "__main__"` com `# pragma: no cover` ao inves de refatorar o codigo para torna-lo testavel, pois entry points de CLI nao sao testaveis no fluxo normal de testes e a diretiva e padrao do coverage.py.
- **Flags de coverage no CI**: Adicao de `--cov=phd_progress_tracker --cov-report=xml` ao comando pytest no workflow do GitHub Actions para gerar o relatorio XML necessario ao Codecov.
- **Badge sem token**: Utilizacao do formato publica do badge (`codecov.io/gh/<owner>/<repo>/badge.svg`) ao inves de token autenticado, seguindo melhores praticas para repositorios publicos.
- **Codecov Action v5**: Uso da versao fixa do action (`codecov/codecov-action@v5`) para evitar breaking changes futuras.

### Files Created/Modified
| File | Purpose | Status |
|------|---------|--------|
| `phd_progress_tracker/main.py` | Adiciona `# pragma: no cover` ao entry point (linha 25) | ✅ Modified |
| `.github/workflows/ci.yml` | Adiciona flags `--cov` e `--cov-report=xml` ao passo de pytest (linha 57) | ✅ Modified |
| `README.md` | Atualiza URL do badge Codecov com caminho correto do repositorio (linha 6) | ✅ Modified |
| `docs/specs/coverage-and-badge/PRD.md` | Documento de requisitos do produto | ✅ Created |
| `docs/specs/coverage-and-badge/SPEC.md` | Especificacao tecnica detalhada | ✅ Created |
| `docs/specs/coverage-and-badge/TEST_REPORT.md` | Relatorio de execucao de testes | ✅ Created |
| `docs/specs/coverage-and-badge/REVIEW_REPORT.md` | Relatorio de code review | ✅ Created |

### Test Results
- **Coverage final**: 100%
- **Total de testes**: 72 passando / 0 falhando
- **Modulos cobertos**: 10 modulos com 100% de cobertura

| Modulo | Cobertura |
|--------|-----------|
| `phd_progress_tracker/__init__.py` | 100% |
| `phd_progress_tracker/cli/__init__.py` | 100% |
| `phd_progress_tracker/cli/commands.py` | 100% |
| `phd_progress_tracker/main.py` | 100% |
| `phd_progress_tracker/models/__init__.py` | 100% |
| `phd_progress_tracker/models/milestone.py` | 100% |
| `phd_progress_tracker/models/task.py` | 100% |
| `phd_progress_tracker/utils/__init__.py` | 100% |
| `phd_progress_tracker/utils/database.py` | 100% |
| `phd_progress_tracker/utils/date_helper.py` | 100% |

**Limitacoes conhecidas**: O badge do Codecov depende de o usuario conectar manualmente o repositorio ao Codecov via interface web. O CI nao falha se o upload nao ocorrer (`fail_ci_if_error: false`).

### Known Technical Debt
- 🟡 **Imports nao utilizados (pre-existentes)**: `Progress` em `commands.py`, `json` e `patch` em `test_commands.py` — foram identificados durante o review mas nao sao bloqueio para merge.
- 🟢 **Badge duplicado no README**: Linhas 5 e 6 ambas contem badge do Codecov — redundancia cosmetica nao critica.

### State of the Application
O PhD Progress Tracker e uma aplicacao CLI Python que permite gerenciar tarefas, prazos e marcos de um doutorado. O projeto utiliza Typer para interface de linha de comando, Rich para formatacao visual, e SQLite/JSON para persistencia. Com a feature `coverage-and-badge`, a aplicacao agora possui infraestrutura de CI/CD completa no GitHub Actions que executa testes com 100% de coverage, faz upload automatico dos relatorios para o Codecov, e exibe badges visuais de qualidade no README. O pipeline inclui validacao de codigo com black, flake8 e mypy, garantindo que alteracoes futuras mantenham os padroes de qualidade estabelecidos.
