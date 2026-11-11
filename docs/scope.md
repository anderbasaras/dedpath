# dedpath — Alcance v1

> Documento de trabajo (español). Deriva del plan maestro aprobado (§1, §5, §8).
> Cualquier cambio de alcance se decide en el chat coordinador y se registra
> en el plan maestro antes de reflejarse aquí.

## 1. Objetivo

Convertir un programa G-code de DED hilo-láser (dialecto SINUMERIK 840D) en
datos analizables —una tabla de segmentos con métricas por segmento, pasada y
capa—, diagnosticar riesgos de proceso con reglas explicables, aplicar
transformaciones seguras y verificadas, y comunicar el resultado en un informe
HTML con visor 3D.

## 2. Alcance v1 (qué SÍ hace)

| Bloque | Incluido en v1 | Fase |
|---|---|---|
| Lectura | Programas SINUMERIK 840D en texto; lectura en streaming línea a línea; tokenizer y intérprete separados | F1 |
| Estado modal | `G0/G1/G2/G3`, `G90/G91`, `G17/G18/G19`, `G70/G71/G700/G710`, `G94`, `F` modal, `G4 F/S` | F1 |
| Arcos | `I/J/K` y `CR=`; longitud exacta analítica (r·θ); discretización solo para geometría/visualización | F1 |
| Activación láser/hilo | Por códigos M definidos **solo en el perfil de dialecto** (YAML dentro del paquete) | F1 |
| Avisos | Toda línea o palabra no reconocida genera un aviso con número de línea; en `--strict`, error | F1 |
| Modelo de datos | Tabla Polars, un registro por segmento, unidades en el nombre de columna (`_mm`, `_s`, `_w`, `_j`, `_mm_min`, `_g`); export Parquet/CSV; `to_pandas()` de cortesía | F1 |
| Generador sintético | Piezas paramétricas (pared, bloque, cilindro…) + inyector de defectos, con verdad conocida | F1 / F3 |
| Segmentación | Capas y pasadas; clasificación deposición / desplazamiento / espera | F2 |
| Métricas | Longitud depositada, tiempo (sin aceleraciones), energía, masa de hilo, stepover, tiempo entre capas | F2 |
| Diagnóstico | Motor de reglas explicables (cada hallazgo dice regla, umbral, valor y líneas afectadas) | F3 |
| Transformaciones | Inserción de `G4 F<s>` entre capas a nivel de línea + verificador por re-parseo | F4 |
| Salidas | Visor 3D (Plotly), gráficos por capa, informe HTML autocontenido (Jinja2), CLI (Typer) | F5 |
| Demo | Streamlit en Hugging Face Spaces | F5 |
| Distribución | PyPI (Trusted Publishing), docs MkDocs Material | F6 |

## 3. No-objetivos explícitos (qué NO hace v1)

1. **No predice temperaturas ni hace simulación térmica/FEM.** El índice térmico
   es un heurístico **relativo** que ordena capas dentro de un mismo programa.
2. **No genera trayectorias:** no es un CAM ni un slicer. Solo lee y modifica
   programas existentes, y solo en los puntos pedidos.
3. **No controla máquinas** ni envía programas a un CNC.
4. **No modela la dinámica de máquina** (aceleraciones, jerk, look-ahead): los
   tiempos son de velocidad constante y por tanto subestimados (⭐ análisis de
   sensibilidad con perfil trapezoidal, recortable).
5. **No cubre todo el lenguaje SINUMERIK.** Quedan fuera en v1, *detectados y
   avisados, nunca ignorados en silencio*: variables y parámetros R, saltos y
   bucles (`GOTO`, `IF`, `WHILE`…), subprogramas y ciclos, frames programables
   (`TRANS`, `ROT`, `SCALE`, `MIRROR`…), transformaciones multieje (`TRAORI`…),
   `G95` (avance por revolución).
6. **Ejes rotativos (A/B/C):** se leen y se avisa; la trayectoria v1 es en 3
   ejes cartesianos (X/Y/Z). *Decisión de alcance tomada en F0 — confirmar en
   el coordinador.*
7. **No soporta otros dialectos** (Marlin/RepRap, Fanuc, KRL…) en v1. La
   arquitectura de perfiles los permite más adelante.
8. **No infiere el ancho de cordón** ni otros parámetros de proceso: vienen del
   perfil con valores genéricos y referencia pública.
9. **No se valida con datos reales de máquina** (regla de confidencialidad): la
   validación es con piezas sintéticas de verdad conocida y geometrías públicas.
10. **Sin interfaz gráfica de edición** de programas.

## 4. Casos de uso priorizados

Prioridad MoSCoW. Actor principal: ingeniero/a de proceso DED.

| # | Prioridad | Caso de uso | Resultado esperado |
|---|---|---|---|
| CU1 | Must | Inspeccionar un programa antes de fabricar | Nº de capas, longitud depositada, tiempo, energía y masa de hilo estimados, por capa y totales |
| CU2 | Must | Detectar riesgos de proceso | Lista de hallazgos explicables (p. ej. capas con tiempo de enfriamiento insuficiente, stepover fuera de rango, saltos Z anómalos) con líneas afectadas |
| CU3 | Must | Insertar esperas entre capas de forma segura | Programa nuevo con `G4 F<s>` solo donde se pide, diff mínimo y verificación por re-parseo |
| CU4 | Must | Compartir el análisis | Informe HTML autocontenido con visor 3D y gráficos por capa |
| CU5 | Should | Analizar con herramientas propias | Tabla de segmentos exportada a Parquet/CSV o como DataFrame Polars/pandas |
| CU6 | Should | Usarlo desde terminal o scripts | CLI (`dedpath analyze`, `dedpath report`, `dedpath add-dwells`…) con códigos de salida útiles |
| CU7 | Could | Probarlo sin instalar nada | Demo web pública con programas sintéticos |
| CU8 | Could ⭐ | Detección no supervisada de capas atípicas | Isolation Forest como complemento de las reglas (recortable) |
| CU9 | Could ⭐ | Reescalar el paso Z | Transformación `zstep` verificada (recortable) |

## 5. Criterios de éxito medibles (v1)

Umbrales del plan maestro §5; la columna «Cómo se mide» fija el protocolo para
que la validación sea reproducible.

| # | Criterio | Umbral | Cómo se mide | Fase |
|---|---|---|---|---|
| C1 | Nº de capas en piezas sintéticas | Exacto | Comparación con el nº de capas del generador, en todo el catálogo sintético | F2 |
| C2 | Longitud depositada | Error relativo < 0,1 % | Frente a la longitud analítica del generador (rectas + arcos r·θ) | F2 |
| C3 | Tiempo estimado (sin aceleraciones) | Error relativo < 0,5 % | Frente al tiempo analítico Σ(L/F) + esperas del generador | F2 |
| C4 | Stepover estimado | < 2 % del programado | Frente al stepover parametrizado en el generador | F2 |
| C5 | Defectos inyectados | Recall ≥ 95 %, falsos positivos ≤ 5 % | Inyector de defectos con etiquetas conocidas; matriz de confusión por regla | F3 |
| C6 | Líneas no soportadas descartadas en silencio | 0 | Tests de propiedades (Hypothesis): toda línea produce segmento, estado o aviso | F1 |
| C7 | Rendimiento | 10⁶ líneas en < 60 s | `benchmarks/` en el portátil de referencia (CPU y RAM anotadas en el resultado) | F1 / F6 |
| C8 | Cobertura del núcleo | > 80 % | `pytest --cov`; `fail_under = 80` en `pyproject.toml` desde F0 | Todas |
| C9 | Seguridad de transformaciones | Diff = solo líneas insertadas; re-parseo idéntico salvo esperas | Verificador `transforms/verify.py` en cada transformación | F4 |

C9 no está en el plan maestro §5: se propone como criterio de cierre de F4
(pendiente de aprobar en el coordinador).

## 6. Supuestos físicos

Se documentan en `docs/physics.md` (F2), partiendo del plan maestro §8.
Resumen: velocidad constante sin aceleraciones; potencia y velocidad de hilo
constantes por tramo; ancho de cordón constante del perfil; masa de hilo
m = ρ·(π d²/4)·v_hilo·t_deposición con eficiencia ≈ 1; índice térmico
relativo, no temperatura.
