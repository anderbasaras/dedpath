## Traspaso Fase 0 — dedpath
**Estado:** validada
**Commit/tag de cierre:** tag `phase-0` (commit «docs: phase 0 hand-off»; esqueleto en `29ee73d`)

### Checklist final
| Tarea | Definido | Implementado | Validado |
|---|---|---|---|
| Nombre `dedpath` libre en PyPI y GitHub + alternativas (`dedtrace`, `depopath`, `gcode-ded`) | ✅ | ✅ | ✅ |
| Repo en la cuenta personal `anderbasaras/dedpath`, clonado en `C:\dev\dedpath` | ✅ | ✅ | ✅ |
| uv + `pyproject.toml` (hatchling, layout `src/`, Python 3.12, grupo `dev`) | ✅ | ✅ | ✅ |
| ruff (lint + format), mypy strict, pytest + Hypothesis + pytest-cov, pre-commit | ✅ | ✅ | ✅ |
| CI GitHub Actions: Ubuntu + Windows × Python 3.12 / 3.13 + build del wheel | ✅ | ✅ | ✅ (run #1, 5/5 verde) |
| LICENSE Apache-2.0, README (EN + resumen ES), CHANGELOG, `.gitignore`, `.gitattributes` | ✅ | ✅ | ✅ |
| `docs/scope.md` (alcance, no-objetivos, casos de uso, criterios medibles) | ✅ | ✅ | ✅ (revisado y aprobado por el autor) |
| `docs/dev-log/` con plantilla del §9 | ✅ | ✅ | ✅ |
| Perfil YAML dentro de `src/` y presente en el wheel | ✅ | ✅ | ✅ (local + CI, instalación limpia del wheel) |
| Manual Siemens descargado y ubicación anotada (`docs/references.md`) | ✅ | ✅ | ✅ |
| ⭐ `devcontainer.json` para Codespaces | ✅ | ✅ | ❌ sin probar (opcional) |

### Decisiones tomadas en la fase (y por qué)
- **Versión única** en `src/dedpath/__init__.py`, leída por hatchling (`[tool.hatch.version]`). Un test comprueba que coincide con los metadatos instalados → imposible publicar con versiones desincronizadas.
- **Dependencias de desarrollo en `[dependency-groups] dev`** (PEP 735): no viajan con el paquete publicado. Sin dependencias de ejecución todavía (llegan en F1).
- **Metadatos de licencia PEP 639** (`license = "Apache-2.0"`, `license-files`) con hatchling ≥ 1.27; texto canónico de la licencia. Autor sin email en `pyproject.toml` (privacidad).
- **ruff**: `line-length = 100`, reglas `E,W,F,I,B,UP,SIM,N,PT,RUF,D(google),PL,PTH,C4,NPY`; tests exentos de `D` y `PLR2004`; `line-ending = "lf"`. Los docstrings Google alimentarán mkdocstrings en F6.
- **mypy** `strict` sobre `src/` + `warn_unreachable` y códigos `ignore-without-code`, `redundant-expr`, `truthy-bool`.
- **pytest** con `--strict-markers --strict-config --import-mode=importlib`, `filterwarnings = error`, `xfail_strict`, marker `slow`. **Cobertura** con ramas y `fail_under = 80` desde F0 (criterio C8 exigido desde el inicio).
- **Hypothesis** con perfiles `dev` (50 ejemplos) y `ci` (300, derandomizado), seleccionables con `HYPOTHESIS_PROFILE`.
- **pre-commit con hooks locales vía `uv run`**: ruff y mypy usan las versiones de `uv.lock` (las mismas que CI). Hooks de higiene `pre-commit-hooks` v6.0.0 y `uv lock --check`.
- **Guardianes de confidencialidad**:
  - Lista privada de términos **fuera del repo** (`%USERPROFILE%\.dedpath\forbidden-terms.txt`, sobrescribible con `DEDPATH_FORBIDDEN_TERMS`); se comprueba en contenido, rutas y mensaje de commit; falla si la lista no existe; nunca imprime el término. `uv.lock` excluido (falsos positivos de términos cortos dentro de hashes sha256; es 100 % generado).
  - Todo fichero G-code (`.mpf .spf .nc .ngc .gcode .cnc`) debe contener la marca `DEDPATH-SYNTHETIC`.
- **CI** en Ubuntu **y Windows** (entorno real de desarrollo), `uv sync --locked`, más un job que inspecciona el wheel y lo instala en un venv limpio. Acciones: `actions/checkout@v7`, `astral-sh/setup-uv@v10.3.3` (setup-uv ya no publica tags mayores flotantes).
- **`.gitattributes`** con `eol=lf` para evitar diffs espurios Windows/Linux.
- **`refs/` ignorado por git**: los manuales con copyright nunca se suben.
- **Alcance** (aprobado por el autor el 2026-11-11): ejes rotativos A/B/C fuera de v1 (se leen y se avisa); nuevo criterio C9 de seguridad de transformaciones propuesto para F4.

### Cambios respecto al plan maestro
| Cambio | Motivo | Acción en el coordinador |
|---|---|---|
| Desarrollo solo en el portátil personal (Windows + PowerShell); el criterio de F0 «en los dos portátiles» pasa a «en el portátil personal» | Decisión del autor | Registrar en §10 y actualizar §3 «Entorno de desarrollo» |
| CI ampliada a Windows además de Ubuntu | Detectar problemas de rutas y finales de línea del entorno real | Informativo |
| Ejes A/B/C fuera de v1 (lectura + aviso) | Acotar F1–F2 a cinemática cartesiana | Añadir a no-objetivos |
| Nuevo criterio C9 (diff = solo líneas insertadas; re-parseo idéntico salvo esperas) | Hacer medible la «transformación segura» de F4 | Añadir a §5 |
| Nuevos directorios `scripts/` (herramientas de desarrollo) y `docs/references.md` | Guardián de confidencialidad y trazabilidad de fuentes | Añadir a §4 |
| Marca obligatoria `DEDPATH-SYNTHETIC` en ficheros G-code | Confidencialidad verificable por máquina | Requisito para el generador de F1 |

### Interfaces públicas creadas (módulos, funciones, firmas clave, columnas del esquema)
- `dedpath.__version__: str` → `"0.1.0.dev0"`.
- Subpaquete `dedpath.dialects` (solo docstring; el esquema Pydantic llega en F1).
- Recurso de paquete del perfil genérico, accesible siempre vía `importlib.resources`:
  `files("dedpath").joinpath("dialects", "profiles", "sinumerik_generic.yaml")` — placeholder con `schema_version: 0`, `name: sinumerik_generic`, `description`.
- Marcador PEP 561 `dedpath/py.typed`.
- Herramienta de desarrollo (no API pública): `scripts/check_forbidden_terms.py`, `main(argv: list[str]) -> int`.
- Esquema de columnas: ninguno todavía (F1).

### Cómo reproducir (comandos PowerShell: instalar, tests, demo)
```powershell
# Requisitos: Git for Windows y uv (https://docs.astral.sh/uv/). Windhawk u otros inyectores de DLL desactivados.
cd C:\dev
git clone https://github.com/anderbasaras/dedpath.git
cd dedpath
git config user.email "<ID>+anderbasaras@users.noreply.github.com"
uv sync                                            # .venv + dependencias del lock + dedpath editable
New-Item -ItemType Directory -Force "$HOME\.dedpath" | Out-Null
notepad "$HOME\.dedpath\forbidden-terms.txt"       # lista privada de términos
uv run pre-commit install

uv run python -c "import dedpath; print(dedpath.__version__, dedpath.__file__)"
uv run pytest --cov
uv run ruff check .; uv run ruff format --check .; uv run mypy src
uv run pre-commit run --all-files
uv build
uv run python -m zipfile -l dist\dedpath-0.1.0.dev0-py3-none-any.whl
# Demo: no aplica en F0.
```

### Resultados de validación (números frente a criterios)
| Comprobación | Resultado |
|---|---|
| `uv sync` (Windows, CPython 3.12.9) | 28 paquetes del lock instalados; `dedpath` editable desde `src\dedpath` |
| `uv run pytest` | 5 passed; cobertura 100 % (umbral C8: 80 %) |
| `ruff check` / `ruff format --check` / `mypy src` | Limpios |
| `uv build` | Wheel con `dialects/profiles/sinumerik_generic.yaml` y `py.typed` |
| `pre-commit run --all-files` | 10/10 ejecuciones sin fallos (con Windhawk desactivado) |
| Guardián de mensaje de commit | Bloquea un término real (`exit code: 1`, término no mostrado) |
| CI run #1 (commit `29ee73d`) | 5/5 verde en 50 s (4 × checks + build and inspect wheel) |
| Manuales Siemens | `PGsl_0313` (8,6 MB) y `PGAsl_0313` (7,3 MB) en `refs\siemens\`, ignorados por git |
| Criterios C1–C7, C9 | No aplican en F0 |

### Deuda técnica, riesgos abiertos y pendientes para fases siguientes
**Riesgos resueltos**
- **Windhawk 1.7.3** inyectaba `windhawk.dll` y tumbaba procesos lanzados en paralelo (`0xC0000005` en `git.exe`, `python.exe`, `uv.exe`, hooks). Diagnosticado con el visor de eventos (ID 1000); Windhawk desactivado durante el proyecto. Si reaparecen exit codes `3221225477`, revisar primero inyectores de DLL.
- Falsos positivos del guardián dentro de hashes de `uv.lock` → `uv.lock` excluido.

**Riesgos abiertos**
- PyPI no reserva el nombre hasta la primera subida (bajo; F6).
- Manual Siemens de 03/2013 (CNC SW 4.5 SP2): posibles diferencias con versiones recientes; cada punto del §7 se cierra citando documento, sección y página.
- `ubuntu-latest` migra a Ubuntu 26: si rompe algo, fijar `ubuntu-24.04`.
- `devcontainer.json` sin probar.

**Deuda técnica**
- `scripts/check_forbidden_terms.py` validado a mano, sin tests unitarios; mypy solo revisa `src/`.
- Perfil YAML es un placeholder sin validar.

**Pendientes para F1**
- Definir el esquema del perfil con Pydantic v2 y cargarlo vía `importlib.resources`; añadir dependencias de ejecución (pydantic, pyyaml, polars, numpy).
- Verificar los puntos de sintaxis del §7 con el manual (cita de sección y página).
- El generador sintético debe escribir `; DEDPATH-SYNTHETIC` en la cabecera de cada programa.
- Tests de propiedades (Hypothesis) para C6: toda línea produce segmento, cambio de estado o aviso.
- Preparar `benchmarks/` para C7 anotando CPU y RAM del portátil de referencia.
