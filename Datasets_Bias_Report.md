# Reporte de Datasets "Dobles" para Detección de Sesgos con IA
**Proyecto:** Usar la IA como *lupa / exponenciador* de sesgos en estructura de datos y toma de decisiones humanas
**Fecha:** 2026-06-01
**Autor:** Eduardo Núñez

---

## 0. Qué es un dataset "doble" (criterio de selección)

Para este proyecto un dataset sirve solo si trae **las dos mitades**:

1. **Inputs (features):** características de los aplicantes/casos *antes* de la decisión.
2. **Output (decisión humana):** lo que un humano decidió/otorgó (aprobado/rechazado, sentenciado/absuelto, a favor/en contra, seleccionado/no seleccionado).

Y para que la "lupa" funcione, además necesitamos **variables protegidas** visibles o inferibles (sexo, edad, ubicación, ingreso, etnia/lengua indígena) para medir disparidad.

> **Regla de oro del proyecto:** le decimos al modelo que "lo correcto = lo que hicieron los humanos", lo entrenamos a imitarlos, y luego medimos *a quién* sistemáticamente le va peor. Si el modelo amplifica un patrón, es que el patrón ya estaba en la decisión humana. Eso es el sesgo expuesto.

---

## 5 Datasets encontrados (con data + resultados humanos)

| # | Dataset | País | Input | Decisión humana | Variables protegidas | Tiene rechazados/negativos | Formato |
|---|---------|------|-------|-----------------|----------------------|----------------------------|---------|
| 1 | **INEGI – ENPOL 2021** | 🇲🇽 | Perfil socioeconómico, delito, proceso | Sentencia / tiempo / debido proceso | Sexo, edad, escolaridad, ingreso, lengua indígena | ✅ (procesados vs sentenciados) | CSV/DBF/SAV |
| 2 | **ProPublica – COMPAS** | 🇺🇸 (referencia oro) | Historial criminal, edad | Score de riesgo + reincidencia real | Raza, sexo, edad | ✅ | CSV |
| 3 | **CONDUSEF – Reclamaciones / RECO** | 🇲🇽 | Producto, institución, monto, causa | Resolución a favor/en contra del usuario | Sexo, entidad, edad | ✅ | CSV/XLSX |
| 4 | **Kaggle – Loan Approval Datasets** | 🌐 (Mexico angle) | Ingreso, empleo, dependientes, crédito | Aprobado / Rechazado | Género, estado civil, educación | ✅ | CSV |
| 5 | **datos.gob.mx – Becas Benito Juárez** | 🇲🇽 | Perfil del estudiante, escuela, estado | Beneficiario (seleccionado) | Sexo, estado, nivel, marginación | ⚠️ solo aceptados | CSV/XLSX |

---

## 🥇 RANKING TOP 3 (por potencial de sesgo × calidad de datos × narrativa de gobernanza)

### #1 — INEGI · ENPOL 2021 (Encuesta Nacional de Población Privada de la Libertad)
**Fuente:** https://www.inegi.org.mx/programas/enpol/2021/
**Microdatos:** https://www.inegi.org.mx/rnm/index.php/catalog/711/ (descarga directa CSV/DBF/SAV + diccionario de datos)

- **Tamaño:** ~67,584 personas encuestadas en centros penitenciarios. Muestra robusta y representativa.
- **Input:** perfil demográfico y socioeconómico, delito imputado, condiciones de detención y proceso (cómo fue detenido, si tuvo abogado, si entendió el proceso, tiempo de proceso).
- **Decisión humana:** si fue **sentenciado** vs solo procesado, **tipo de sentencia**, **duración de la condena**, y trato durante el proceso judicial (debido proceso).
- **Variables protegidas (oro puro):** sexo, edad, **escolaridad**, **ingreso previo**, **hablante de lengua indígena**, entidad. Permite cruzar etnia/clase contra severidad de la pena.
- **Por qué #1:** es 100% mexicano, oficial, descargable, con *ambas mitades* y con variables de sesgo riquísimas. La narrativa de gobernanza es brutal: *"¿el sistema penal mexicano castiga más duro a los pobres / indígenas / con baja escolaridad ante delitos comparables?"*. Es exactamente tu "lupa" sobre una decisión humana de altísimo impacto.
- **Riesgo/cuidado:** es una *encuesta autorreportada* (no expediente judicial), y es población ya encarcelada (sesgo de selección: no ves a quien sí salió libre). Hay que encuadrarlo como análisis de severidad/proceso, no de culpabilidad. Tema sensible → cuidado ético en el artículo.

---

### #2 — ProPublica · COMPAS Recidivism
**Fuente / datos:** https://github.com/propublica/compas-analysis
**Metodología:** https://www.propublica.org/article/how-we-analyzed-the-compas-recidivism-algorithm

- **Input:** historial criminal, edad, cargos, conteo de delitos previos del condado de Broward (2013–2014).
- **Decisión humana/algorítmica:** el **score de riesgo COMPAS (1–10)** asignado a cada acusado + la **reincidencia real a 2 años** (ground truth). Doble decisión: la del algoritmo y la realidad.
- **Variables protegidas:** **raza**, sexo, edad — explícitas.
- **Por qué #2:** es el caso de estudio **canónico** mundial de sesgo algorítmico. Ya tiene análisis publicado (puedes *replicar y luego extender*), datos limpios en CSV, y le da credibilidad académica inmediata a tu portfolio. Sirve como "vara de medir": validas tu pipeline contra un resultado conocido antes de aplicarlo a datos mexicanos.
- **Mexico angle:** úsalo como *benchmark / espejo* — "esto pasó en EE.UU. con un algoritmo; veamos si la decisión humana mexicana (ENPOL) muestra el mismo patrón sin necesidad de algoritmo".
- **Riesgo/cuidado:** no es mexicano. Posiciónalo como referencia metodológica, no como dato local.

---

### #3 — CONDUSEF · Reclamaciones / Buró de Entidades Financieras (RECO)
**Portal de datos abiertos CONDUSEF:** https://www.condusef.gob.mx/?p=datos-abiertos
**Plataforma nacional:** https://datos.gob.mx/dataset/?organization=condusef

- **Input:** producto financiero, institución reclamada, monto reclamado, causa de la queja, canal, entidad federativa.
- **Decisión humana:** **resolución** — si la reclamación se resolvió **a favor del usuario** o de la institución, dictamen, conciliación.
- **Variables protegidas:** sexo del usuario, entidad federativa (proxy de región/nivel socioeconómico), a veces rango de edad.
- **Por qué #3:** mexicano, oficial, descargable (CSV/XLSX), con decisión binaria clara y volumen alto. Narrativa de gobernanza financiera fuerte: *"¿a quién le resuelven a favor — y a quién no — ante reclamos comparables? ¿hay disparidad por región o por institución?"*. Encaja perfecto con tu idea de "dar X beneficio a Y aplicantes".
- **Riesgo/cuidado:** las variables demográficas individuales son más limitadas que ENPOL; el sesgo se mide más a nivel institución/región que a nivel persona. Hay que revisar el diccionario del año específico (la estructura cambia entre años).

---

## Menciones (lugares 4 y 5)

### #4 — Kaggle · Loan Approval Datasets *(motor de simulación)*
- https://www.kaggle.com/datasets/architsharma01/loan-approval-prediction-dataset
- https://www.kaggle.com/datasets/taweilo/loan-approval-classification-data
- **Uso recomendado:** NO como dato mexicano real, sino como **banco de pruebas limpio** para construir y depurar tu modelo (aprobado/rechazado + ingreso, dependientes, educación, autoempleo). Tiene ambas clases (aprobado y rechazado), ideal para el A/B supervisado vs no-supervisado antes de tocar datos mexicanos. *Mexico angle:* renombrar/mapear variables a un contexto de crédito mexicano para la demo.

### #5 — datos.gob.mx · Becas Benito Juárez / SUBES
- https://datos.gob.mx/dataset/programa_nacional_becas_bienestar_benito_juarez_2025_programa_s283
- **Limitación clave:** el *padrón de beneficiarios* solo contiene a los **aceptados**, no a los rechazados → no hay clase negativa directa. **No sirve para clasificación aprobado/rechazado**, pero **sí** para análisis de *representación/distribución*: ¿la composición de beneficiarios (sexo, estado, marginación) refleja a la población elegible, o hay sub/sobre-representación? Es una "lupa" distinta (equidad distributiva, no decisión binaria). Buen complemento, mal candidato principal.

---

## Recomendación de arranque

1. **Construye y valida el pipeline con COMPAS (#2)** — datos limpios, resultado conocido.
2. **Aplica la metodología a ENPOL (#1)** — tu estrella mexicana, donde está la narrativa fuerte.
3. **Refuerza con CONDUSEF (#3)** — segundo caso mexicano, dominio financiero, otra cara de la gobernanza.
4. Usa **Kaggle (#4)** solo como sandbox y **Becas (#5)** como análisis distributivo complementario.

---

## Fuentes
- [INEGI ENPOL 2021 (programa)](https://www.inegi.org.mx/programas/enpol/2021/)
- [INEGI ENPOL 2021 (microdatos / catálogo)](https://www.inegi.org.mx/rnm/index.php/catalog/711/)
- [INEGI ENPOL 2016 (microdatos)](https://www.inegi.org.mx/rnm/index.php/catalog/268)
- [ProPublica COMPAS (datos + análisis)](https://github.com/propublica/compas-analysis)
- [ProPublica – How We Analyzed COMPAS](https://www.propublica.org/article/how-we-analyzed-the-compas-recidivism-algorithm)
- [CONDUSEF Datos Abiertos](https://www.condusef.gob.mx/?p=datos-abiertos)
- [CONDUSEF en la Plataforma Nacional de Datos Abiertos](https://datos.gob.mx/dataset/?organization=condusef)
- [Kaggle Loan Approval Prediction Dataset](https://www.kaggle.com/datasets/architsharma01/loan-approval-prediction-dataset)
- [Kaggle Loan Approval Classification Data](https://www.kaggle.com/datasets/taweilo/loan-approval-classification-data)
- [datos.gob.mx – Becas Benito Juárez 2025 (S283)](https://datos.gob.mx/dataset/programa_nacional_becas_bienestar_benito_juarez_2025_programa_s283)
- [Portal de Datos Abiertos del Estado de Chihuahua](https://transparencia.chihuahua.gob.mx/) · [Datos Abiertos Municipio Chihuahua](https://datos.mpiochih.gob.mx/)
