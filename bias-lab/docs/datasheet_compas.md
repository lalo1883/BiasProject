# Datasheet — COMPAS (compas-scores-two-years.csv)
> Documentación del dataset siguiendo el espíritu de *"Datasheets for Datasets"* (Gebru et al.).
> Esta práctica es parte central del proyecto: gobernanza = saber qué dato usas y sus límites.

## Motivación
- **¿Para qué se creó?** ProPublica lo construyó para investigar si el sistema COMPAS (que asigna scores de riesgo de reincidencia a acusados) era racialmente sesgado.
- **Origen:** registros públicos del condado de Broward, Florida, EE.UU. (2013–2014).

## Composición
- **Unidad:** un acusado evaluado por COMPAS antes del juicio.
- **Filas:** 7,214 crudas → 6,172 tras el filtro estándar de ProPublica.
- **Columnas clave para nosotros:**
  - `race`, `sex`, `age`, `age_cat` — variables protegidas / demográficas.
  - `priors_count`, `juv_*_count`, `c_charge_degree` — historial criminal (features).
  - `decile_score` (1–10), `score_text` (Low/Medium/High) — **la decisión** (score de riesgo).
  - `two_year_recid` — **ground truth**: ¿reincidió en 2 años? (1/0).

## Filtro aplicado (reproducible)
`days_b_screening_arrest` ∈ [-30, 30] · `is_recid != -1` · `c_charge_degree != 'O'` · `score_text != 'N/A'`

## Variables protegidas detectadas (banderas de sesgo)
- **Raza** (foco principal del análisis), **sexo**, **edad**.
- Proxies potenciales de raza: `priors_count` (historial de arrestos) está **correlacionado** con la raza en estos datos. El *porqué* (sobre-vigilancia, factores socioeconómicos, etc.) NO se puede determinar con este dataset; solo observamos la correlación.

## Limitaciones / advertencias éticas
- Solo condado de Broward → no generaliza a otras jurisdicciones.
- `two_year_recid` mide *re-arresto*, no *re-delito* real → captura quién fue detenido de nuevo, que puede no equivaler a quién delinquió de nuevo.
- **Disparidad ≠ sesgo automáticamente:** los datos muestran diferencias por raza; calificarlas de "sesgo" exige elegir una definición de justicia, y distintas definiciones se contradicen (resultado de imposibilidad: Kleinberg 2016, Chouldechova 2017).
- **Lo que el dato muestra vs. lo que se interpreta:** distinguir ambos es parte del rigor de gobernanza. Las explicaciones causales requieren evidencia externa, no este dataset.
- Datos de personas reales (aunque públicos): no reidentificar, uso solo analítico/educativo.

## Hallazgo registrado (Proceso 1)
- Falsos positivos: **Afroamericanos 42.3%** vs **Caucásicos 22.0%**.
- Falsos negativos: Caucásicos 49.6% vs Afroamericanos 28.5%.
- ✅ Reproduce el resultado publicado por ProPublica → método validado.
