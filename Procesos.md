# Procesos.md — Los experimentos, explicados fácil
> Cada proceso responde UNA pregunta. Aquí está qué hace, cómo, y qué resultado esperar.

---

## Proceso 1 — Tasas base (sin IA, el calentamiento)
**Pregunta:** ¿Ya hay disparidad cruda en las decisiones humanas, sin tocar ningún modelo?
**Cómo:** Cuentas el % de "beneficio" (sentencia leve / score bajo) por cada grupo protegido. Una tabla simple.
**Resultado posible:** Si los grupos ya reciben tasas muy distintas → tienes el punto de partida. Esto es media historia y no necesita IA.

---

## Proceso 2 — Blind vs Aware (EL detector de sesgo)
**Pregunta:** ¿El humano estaba *usando* la variable protegida para decidir?
**Cómo:** Entrenas el MISMO modelo dos veces:
- **A (blind):** SIN la variable protegida.
- **B (aware):** CON la variable protegida.
**Mides dos cosas:**
1. ¿Predice mejor B que A? (qué tanto importaba la variable)
2. ¿Cambia la disparidad entre A y B?
**Resultado posible:**
- B predice mejor → el humano usaba esa variable → sesgo.
- A y B predicen igual PERO ambos discriminan → el sesgo entra por *proxies* (ver Proceso 3).

---

## Proceso 3 — Cazando proxies
**Pregunta:** Si quito la variable protegida, ¿el modelo deja de discriminar de verdad?
**Cómo:** Tomas el modelo *blind* (sin raza/etnia) y revisas si sus predicciones siguen siendo desiguales por grupo.
**Resultado posible:** Casi siempre **sigue discriminando**, porque otras variables (zona, arrestos previos) cargan la info de la protegida. Hallazgo contraintuitivo y potente.

---

## Proceso 4 — Medir la AMPLIFICACIÓN (el clímax)
**Pregunta:** ¿El modelo discrimina MÁS que los humanos?
**Cómo:** Comparas dos disparidades sobre la misma gente:
- Disparidad en las **decisiones humanas reales**.
- Disparidad en las **predicciones del modelo** entrenado para imitarlas.
**Resultado posible:** Si `disparidad_modelo > disparidad_humano` → la IA *amplificó* el sesgo. Ese es el gráfico estrella del artículo.
**Por qué pasa:** los humanos aplican el sesgo de forma inconsistente; el modelo lo destila en una regla y lo aplica al 100%.

---

## Proceso 5 — Importancia de variables (SHAP)
**Pregunta:** ¿Cuánto pesa cada variable protegida al reproducir la decisión?
**Cómo:** Aplicas SHAP al modelo *aware* → te dice cuántos "puntos" de la decisión explica el sexo, el ingreso, la etnia, etc.
**Resultado posible:** Un ranking visual: "la escolaridad pesó X en la sentencia". Convierte el sesgo en algo cuantificado.

---

## Proceso 6 — No-supervisado (confirmar por otro camino)
**Pregunta:** ¿Existe la segregación en los datos aunque nadie la etiquete?
**Cómo:** Clustering (K-Means) usando SOLO las features de input, sin la decisión. Luego ves si los clusters coinciden con grupos protegidos y reciben distinto "beneficio".
**Resultado posible:** Si se forman grupos que coinciden con etnia/ingreso y reciben peor trato → confirma el hallazgo supervisado desde otro ángulo. (Este es el "Eje 2": supervisado vs no-supervisado.)

---

## Proceso 7 — Métricas de equidad (el veredicto formal)
**Pregunta:** En lenguaje técnico estándar, ¿qué tan injusto es?
**Cómo:** Calculas métricas reconocidas: Demographic Parity, Equal Opportunity, Disparate Impact (regla del 80%).
**Resultado posible:** Números comparables con la literatura → le da rigor académico al artículo. (Librerías: `fairlearn` o `aequitas`.)

---

### Orden sugerido de ejecución
1 → 2 → 3 → 4 (clímax) → 5 → 6 (confirmación) → 7 (cierre formal)
