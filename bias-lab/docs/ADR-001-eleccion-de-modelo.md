# ADR-001 — Elección del modelo de machine learning
> ADR = *Architecture Decision Record*. Registra una decisión técnica importante, sus
> alternativas y el porqué, para que cualquiera (o tú en 6 meses) entienda la razón.

- **Fecha:** 2026-06-01
- **Estado:** Aceptada
- **Contexto del proyecto:** "IA como lupa de sesgos" — article-forward, foco en gobernanza y explicabilidad.

## Decisión
Usar **Regresión Logística** como modelo principal para los Procesos 2–5 (blind vs aware,
proxies, amplificación, importancia de variables), tanto en COMPAS como en ENPOL.

## Alternativas consideradas
| Modelo | Precisión | Interpretable | Por qué NO (como principal) |
|---|---|---|---|
| **Regresión logística** ✅ | buena | altísima | — (elegida) |
| Árbol de decisión | media | alta | Inestable; cambia mucho con pocos datos distintos |
| Random Forest | alta | media | Caja parcial; requiere SHAP para explicar |
| XGBoost / Gradient Boosting | la más alta | baja | Caja negra; muchos hiperparámetros; contradice el objetivo de transparencia |
| Redes neuronales | no mejora en tablas chicas | nula | Exagerado para datos tabulares pequeños; nada interpretable |

## Razones de la decisión
1. **El objetivo no es máxima precisión, es exponer y explicar el sesgo.** Eso prioriza
   interpretabilidad sobre desempeño.
2. **Transparencia:** la regresión logística da un "peso" (coeficiente) por variable →
   se ve directamente cuánto influyó la raza/etnia en imitar la decisión humana.
3. **Coherencia narrativa:** usar una caja negra para *estudiar* sesgos sería contradictorio
   en un artículo de gobernanza.
4. **Comparabilidad:** ProPublica usó regresión logística → validar contra su resultado es honesto.
5. **Reproducibilidad:** pocos ajustes, fácil de documentar y volver a correr.
6. **Costo computacional:** entrena en <1 segundo en una laptop; sin GPU.

## Consecuencias
- ✅ Hallazgos fáciles de explicar y defender en el artículo.
- ✅ Pipeline simple y reproducible.
- ⚠️ Puede que no capture relaciones no lineales complejas → aceptable, no es el objetivo.

## Decisión futura abierta (no ahora)
Usar **XGBoost como prueba de robustez opcional**, conectado a la tesis de amplificación:
*¿un modelo más potente amplifica todavía más el sesgo?* Sería una sección extra, NO el
modelo principal. Se registrará en un ADR aparte si se hace.
