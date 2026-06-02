# Bitácora del proyecto — IA como lupa de sesgos
> Registro vivo de decisiones y avances. Parte de la gobernanza: que cualquiera pueda
> reconstruir QUÉ se hizo, POR QUÉ y CUÁNDO.

---

## Decisiones de diseño (sesión de planeación)
| # | Decisión | Elección | Por qué |
|---|----------|----------|---------|
| 1 | Entregable | **Artículo + repo, pero article-forward** | El fuerte técnico a mostrar es documentación/proceso de IA, no código lucido |
| 2 | Alcance | **2 datasets**: COMPAS (validación) + ENPOL (caso MX) | Arco limpio: método validado → hallazgo nuevo |
| 3 | Decisión a auditar en ENPOL | **Severidad de la sentencia** (controlando por delito) | Es lo más parecido estructuralmente a COMPAS → el método transfiere |
| 4 | Tesis central | **Amplificación**: la IA aprende y exagera el sesgo humano | Una idea memorable, contraintuitiva y demostrable con un número |
| 5 | Entorno | **Local** (venv) ahora, Colab después | Control y aprendizaje; luego portabilidad |
| 6 | Punto de arranque | **COMPAS primero** | Datos limpios, valida el pipeline antes de pelear con datos sucios |
| 7 | Modelo de ML | **Regresión logística** (ver `bias-lab/docs/ADR-001`) | Interpretable > preciso; el objetivo es *explicar* el sesgo, no maximizar accuracy. XGBoost queda como prueba de robustez futura |

---

## Avance

### 2026-06-01 — Setup + Proceso 1 (COMPAS)
**Hecho:**
- Estructura de proyecto creada en `bias-lab/` + entorno virtual con pandas, numpy, scikit-learn, matplotlib, seaborn.
- COMPAS descargado (`data/raw/compas-scores-two-years.csv`): 7,214 filas → 6,172 tras filtro ProPublica.
- **Proceso 1 (tasas base) — SOLO análisis descriptivo, sin IH:**
  - `src/proceso1_tasas_base.py` corre y reproduce el hallazgo publicado.
  - Falsos positivos: **Afroamericanos 42.3%** vs **Caucásicos 22.0%**.
  - Falsos negativos: Caucásicos 49.6% vs Afroamericanos 28.5%.
  - Gráfica: `reports/figures/proceso1_falsos_positivos.png`.
- Documentación: `docs/datasheet_compas.md`, `README.md`, `.gitignore`.
- Versión Colab del Proceso 1 entregada (celdas auto-contenidas).

**Naturaleza de lo hecho:** estadística descriptiva (contar). **Aún NO se entrena ningún modelo.**

**Pendiente inmediato:**
- ⬜ Proceso 4 — Medir amplificación (clímax).
- ⬜ Descarga manual de ENPOL (INEGI).

### 2026-06-01 — Proceso 3 (Cazando proxies)
**Hecho:** `src/proceso3_proxies.py` + `reports/figures/proceso3_cazando_proxies.png`.
**Hallazgos:**
1. `priors_count` correlaciona con raza: AA 4.24 vs Caucásico 2.29 delitos previos (**1.9×**).
2. Brechas: AWARE +42.5% → BLIND +27.9% → BLIND SIN PROXIES (sin raza ni historial) **+17.4%**.
   Quitar el historial baja la brecha → era un proxy real.
3. **Giro:** queda +17.4% residual aun sin raza ni historial → el sesgo está repartido en
   toda la estructura (edad, sexo, cargo). **Es estructural; no se borra quitando columnas.**

### 2026-06-01 — Proceso 2 (Blind vs Aware) — primer modelo de IA
**Hecho:** `src/proceso2_blind_vs_aware.py`. Dos regresiones logísticas (sin/con raza) entrenadas
a imitar la decisión humana "alto riesgo". 5,278 casos (AA + Caucásicos), 80/20 train/test.
Gráfica: `reports/figures/proceso2_brecha_blind_vs_aware.png`.

**Hallazgos (honestos, incluido el inesperado):**
1. **H1 NO se confirmó:** el modelo *aware* NO imita mejor (75.7% vs 76.6%). La raza explícita no agrega poder predictivo → no era *necesaria*.
2. **H2 confirmada (proxies):** el modelo *blind* (sin raza) igual discrimina fuerte (brecha +27.9 pp). "Ser ciego al color" no elimina el sesgo.
3. Darle la raza *empeora* la brecha (+27.9 → +42.5 pp); coeficiente caucásico −0.45.

**Lección de gobernanza:** quitar la variable protegida es una "solución" engañosa; el sesgo
persiste vía proxies. Esto es material central para el artículo.

**Nota técnica:** se silencian RuntimeWarnings espurios del BLAS de macOS (Accelerate); no afectan resultados.

---

## Glosario rápido (para el artículo)
- **Falso positivo:** marcar a alguien "alto riesgo" que NO reincidió → injusticia.
- **Falso negativo:** marcar "bajo riesgo" a alguien que SÍ reincidió → beneficio de la duda.
- **Tasa base:** proporción cruda de un resultado en un grupo, sin modelo.
- **Blind vs Aware:** entrenar un modelo sin / con la variable protegida para ver si la usaba.
- **Amplificación:** el modelo discrimina MÁS que los humanos que imitó.
- **Proxy:** una variable que *parece* neutral pero **carga con la información de otra** (la protegida). Ej: `priors_count` está correlacionado con la raza, así que el modelo lo usa como sustituto. Por eso borrar la raza no elimina la disparidad.
- **Disparidad ≠ sesgo:** una diferencia de resultados por grupo es un *hecho*; llamarla "sesgo" es un *juicio de valor* que depende de qué definición de justicia uses.

## ⚠️ Rigor: lo que el dato muestra vs. lo que se interpreta
- **Sí demostrado:** AA tienen 1.9× más `priors` registrados; `priors` correlaciona con raza; el modelo lo usa.
- **NO demostrado por estos datos:** el *porqué* (sobre-vigilancia vs. otros factores). Eso es conocimiento externo, no un hallazgo de este análisis. (Corrección registrada 2026-06-01: antes se afirmó "sobre-vigilancia" como hecho; era interpretación.)
- **Resultado de imposibilidad (Kleinberg 2016 / Chouldechova 2017):** con tasas base distintas, ningún modelo cumple todas las definiciones de justicia a la vez. Por eso Northpointe y ProPublica "ambos tenían razón".

## 💡 Ideas-tesis para el artículo (frases clave)
1. **El dato puede nacer cargado del proceso humano que lo generó.** Un número que parece objetivo (`priors_count`) puede arrastrar las decisiones humanas previas — pero atribuir la *causa* exige evidencia externa.
2. **La IA no inventa los sesgos, hereda los patrones de las decisiones humanas** y los aplica de forma consistente, volviéndolos visibles y medibles.
3. **Borrar la variable protegida es una solución engañosa:** la disparidad sobrevive en los proxies.
4. **Disparidad no es lo mismo que sesgo:** el sesgo más claro aquí está en la *desigualdad de errores* (Proceso 1), no en las tasas crudas. Y reducir la brecha *cuesta precisión* (trade-off equidad-exactitud: 76.6% → 66.2%).
