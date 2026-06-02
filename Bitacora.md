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
- ⬜ Proceso 2 — Blind vs Aware (aquí entra la IA por primera vez).
- ⬜ Proceso 4 — Medir amplificación (clímax).
- ⬜ Descarga manual de ENPOL (INEGI).

---

## Glosario rápido (para el artículo)
- **Falso positivo:** marcar a alguien "alto riesgo" que NO reincidió → injusticia.
- **Falso negativo:** marcar "bajo riesgo" a alguien que SÍ reincidió → beneficio de la duda.
- **Tasa base:** proporción cruda de un resultado en un grupo, sin modelo.
- **Blind vs Aware:** entrenar un modelo sin / con la variable protegida para ver si la usaba.
- **Amplificación:** el modelo discrimina MÁS que los humanos que imitó.
