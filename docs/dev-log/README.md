# Dev-log

> Documento de trabajo (español).

Registro de cierre de cada fase del proyecto. Al validar una fase, su chat
genera el traspaso con el formato de [`_template.md`](_template.md) (plan
maestro §9) y se guarda aquí como `phase-N.md`. El mismo texto se pega en el
chat coordinador y en el chat de la fase siguiente.

| Fase | Fichero | Estado |
|---|---|---|
| F0 — Alcance, criterios, setup, CI | [`phase-0.md`](phase-0.md) | validada (tag `phase-0`) |
| F1 — Parser, modelo de datos, perfil de dialecto, generador sintético | `phase-1.md` | pendiente |

## Configuración local del equipo de desarrollo (no va al repo)

El clon necesita, una vez:

1. `uv sync` y `uv run pre-commit install`.
2. La lista privada de términos confidenciales en
   `%USERPROFILE%\.dedpath\forbidden-terms.txt` (un término por línea; `#` para
   comentarios). Sin ese fichero, el hook `forbidden-terms` bloquea los commits
   a propósito.
3. Identidad git del repo con el correo personal o el `noreply` de GitHub
   (`git config user.email ...` **dentro del repo**, nunca el corporativo).
4. Manuales de referencia descargados en `refs/` (ver `docs/references.md`).
5. Ningún software que inyecte DLLs en todos los procesos activo mientras se
   desarrolla (ver riesgo «Windhawk» en `phase-0.md`).
