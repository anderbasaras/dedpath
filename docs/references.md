# Referencias

> Documento de trabajo (español). Las referencias con copyright **no se suben al
> repositorio**: se guardan en la carpeta local `refs/` (ignorada por git en
> `.gitignore`) en cada portátil.

## Manuales de Siemens (sintaxis SINUMERIK, plan maestro §7)

| ID | Documento | Edición / referencia | Uso | Ubicación local |
|---|---|---|---|---|
| SIE-PGsl | *SINUMERIK 840D sl / 828D — Fundamentals, Programming Manual* (Siemens) | 03/2013, 6FC5398-1BP40-3BA1, CNC software 4.5 SP2 | Fuente principal para verificar los puntos del §7 (I/J/K, `CR=`, `G4`, `G700/G710`, `G18`, `G95`, bloques sin `N`) | `refs/siemens/PGsl_0313_en_en-US.pdf` |
| SIE-PGAsl | *SINUMERIK 840D sl / 828D — Job Planning, Programming Manual* (Siemens) | 03/2013, 6FC5398-2BP40-3BA1 | Consulta secundaria: lenguaje avanzado (parámetros R, saltos, subprogramas, frames) que v1 detecta y avisa | `refs/siemens/PGAsl_0313_en_en-US.pdf` |

Descarga oficial (servidor de documentación de Siemens):

- SIE-PGsl: <https://cache.industry.siemens.com/dl/files/554/74475554/att_56792/v1/PGsl_0313_en_en-US.pdf>
- SIE-PGAsl: <https://cache.industry.siemens.com/dl/files/038/70265038/att_80019/v1/PGAsl_0313_en_en-US.pdf>

Existen ediciones posteriores en Siemens Industry Online Support
(<https://support.industry.siemens.com>, puede requerir registro). Si se usa una
edición más reciente, anotar aquí su referencia y fecha, y citarla en cada
verificación del §7 (p. ej. «SIE-PGsl, §x.y, p. N»).

**Regla:** cada hipótesis del §7 se cierra citando documento, sección y página.
Si el manual no lo deja claro, se documenta como supuesto y se marca para
verificar, sin inventar.

## Literatura técnica (pendiente de verificar)

| ID | Referencia | Estado | Fase |
|---|---|---|---|
| DING2015 | Ding et al. (2015), *Robotics and Computer-Integrated Manufacturing* — modelo de solape tangente en WAAM (paso ≈ 0,738·w) | **Sin verificar**: confirmar cifra, DOI y título; documentar que es WAAM, no hilo-láser | F2 |
