# Steps.md — Proyecto "IA como Lupa de Sesgos"
**Objetivo:** Entrenar un modelo a imitar decisiones humanas ("lo correcto = lo que hizo el humano") y usar esa imitación para **exponer y exponenciar** el sesgo latente en los datos y en la decisión. A/B testing supervisado vs no-supervisado.

---

## Fase 0 — Encuadre y ética (antes de tocar código)
- [ ] Escribir en 1 párrafo la **hipótesis de sesgo** por dataset (ej. "ENPOL: a menor escolaridad/ingreso, mayor severidad de pena ante delito comparable").
- [ ] Definir las **variables protegidas** a auditar: sexo, edad, ubicación, ingreso, etnia/lengua indígena.
- [ ] Definir la **métrica de "beneficio"** (aprobación, sentencia leve, resolución a favor) = la variable objetivo.
- [ ] Nota ética: datos sensibles (penal/financiero) → agregar disclaimer, no reidentificar, no concluir causalidad de culpabilidad.

## Fase 1 — Adquisición de datos
- [x] Descargar **COMPAS** (GitHub ProPublica) → validar pipeline con caso conocido.  *(2026-06-01)*
- [ ] Descargar **ENPOL 2021** microdatos (INEGI, CSV/DBF) + **diccionario de datos**.
- [ ] Descargar **CONDUSEF Reclamaciones** (datos.gob.mx) del año con mejor diccionario.
- [ ] (Sandbox) Descargar un **Loan Approval** de Kaggle para pruebas rápidas.
- [ ] Guardar todo en `/data/raw/` + un `SOURCES.md` con URL, fecha de descarga y licencia.

## Fase 2 — Exploración y limpieza (EDA)
- [x] Identificar y confirmar la **columna de decisión** (output) y las **features** (input) — *hecho para COMPAS (2026-06-01)*
- [ ] Mapear/normalizar nombres de columnas; documentar el esquema en `/data/SCHEMA.md`.
- [ ] Tratar nulos, codificar categóricas, normalizar numéricas.
- [x] **Auditoría descriptiva de base rates:** % de "beneficio" por cada grupo protegido (tabla de disparidad cruda). *(COMPAS hecho — Proceso 1, 2026-06-01)*
- [ ] Separar columnas protegidas en dos sets: (a) las que el modelo *verá*, (b) las que *no verá* pero usaremos para auditar.

## Fase 3 — Modelo Supervisado (la "lupa": imitar al humano)
- [ ] Train/test split estratificado.
- [ ] Entrenar clasificador a **predecir la decisión humana** (LogisticRegression + RandomForest/XGBoost).
- [ ] Objetivo NO es accuracy alto por sí mismo, sino **capturar el patrón de decisión humana**.
- [ ] **Experimento de amplificación (exponenciador):**
  - [ ] Variante A — *blind*: entrenar SIN las variables protegidas.
  - [ ] Variante B — *aware*: entrenar CON las variables protegidas.
  - [ ] Comparar: si B mejora prediciendo la decisión humana, la variable protegida *importaba* → el humano la estaba usando.
- [ ] **Importancia de variables** (SHAP / feature importance) → ¿cuánto pesa sexo/ingreso/etnia en reproducir la decisión?

## Fase 4 — Modelo No-Supervisado (sesgo sin etiquetas)
- [ ] Clustering (K-Means / DBSCAN) **solo sobre las features de input**.
- [ ] Cruzar clusters contra la decisión humana y contra las variables protegidas.
- [ ] Detectar: ¿se forman clusters que coinciden con grupos protegidos y que reciben sistemáticamente menos "beneficio"?
- [ ] Detección de anomalías (Isolation Forest): ¿quiénes recibieron una decisión "inesperada" dado su perfil? ¿tienen un patrón demográfico?

## Fase 5 — A/B Testing Supervisado vs No-Supervisado
- [ ] Definir qué "descubre" cada enfoque sobre el mismo sesgo.
- [ ] Supervisado responde: *"¿el humano usó la variable protegida para decidir?"*
- [ ] No-supervisado responde: *"¿existe estructura/segregación en los datos aunque nadie la etiquetara?"*
- [ ] Tabla comparativa de hallazgos A/B por dataset.

## Fase 6 — Métricas de equidad (cuantificar el sesgo)
- [ ] Calcular: **Demographic Parity**, **Equal Opportunity**, **Disparate Impact (regla 80%)**, **Equalized Odds**.
- [ ] (Opcional) usar librería `Fairlearn` o `Aequitas` para el dashboard de fairness.
- [ ] Reportar disparidad por cada grupo protegido, con intervalos de confianza.

## Fase 7 — Visualización y narrativa
- [ ] Gráficas: base rates por grupo, importancia de variables protegidas, mapa de disparidad por estado.
- [ ] La historia central: *"La IA no inventó el sesgo; lo aprendió de nosotros y lo hizo visible/medible."*
- [ ] Conectar cada hallazgo con una recomendación de **gobernanza de datos**.

## Fase 8 — Entregable / artículo de portfolio
- [ ] Notebook reproducible (`/notebooks/`) + README con cómo correrlo.
- [ ] Artículo de gobernanza de datos con: hallazgos, límites, ética, recomendaciones.
- [ ] Sección de limitaciones honesta (sesgo de selección, auto-reporte, correlación ≠ causalidad).

---

### Stack sugerido
`Python` · `pandas` · `scikit-learn` · `xgboost` · `shap` · `fairlearn` / `aequitas` · `matplotlib/seaborn` · `jupyter`

### Estructura de carpetas sugerida
```
proyecto-sesgos/
├── data/{raw,processed}/
├── notebooks/
├── src/
├── reports/figures/
├── SOURCES.md
└── README.md
```
