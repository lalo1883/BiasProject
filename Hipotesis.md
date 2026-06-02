# Hipótesis.md — Banco de ideas del proyecto
> Aquí vamos tirando ideas e hipótesis conforme avanzamos. No todas se probarán; es un cuaderno vivo.

---

## ⭐ Tesis central (decisión: opción A)
**"La IA no es objetiva: aprende los sesgos de las decisiones humanas y los *amplifica*. Por eso sirve como una lupa que los hace visibles y medibles."**

- La gente cree que un modelo es neutral. Vamos a mostrar lo contrario *con un número*.
- El número estrella: comparar la **disparidad en las decisiones humanas** vs la **disparidad en las predicciones del modelo** sobre la misma gente. Si el modelo discrimina *más* que los humanos → probamos la amplificación.

---

## Cómo detectamos el sesgo (idea base)
Quitamos/agregamos variables y medimos **dos cosas a la vez**:
1. **¿Cuánto baja la capacidad de predecir?** → qué tanto "usaba" el modelo esa variable.
2. **¿Cambió a quién beneficia?** → la disparidad entre grupos protegidos.

> El caso más revelador: quitas la variable protegida (ej. raza), la precisión **casi no baja**, pero el modelo **sigue discriminando** → la está colando por *proxies*. "Ser ciego al color" no elimina el sesgo.

---

## Hipótesis por dataset

### COMPAS (validación del método)
- **H0 (disparidad cruda) ✅ CONFIRMADA (Proceso 1, 2026-06-01):** ya existe disparidad en la decisión humana antes de cualquier IA. Falsos positivos: Afroamericanos **42.3%** vs Caucásicos **22.0%**. Reproduce a ProPublica.
- **H1 (pendiente — Proceso 2):** El modelo predice mejor el score de riesgo cuando se le da la raza → los humanos/el sistema usaban la raza.
- **H2 (proxies — pendiente):** Aun quitando la raza, el modelo sigue marcando más "alto riesgo" a negros, vía arrestos previos / zona.
- **H3 (amplificación — pendiente, Proceso 4):** La tasa de falsos positivos por raza del modelo es *mayor* que la del score humano original.

### ENPOL (caso mexicano)
- **H4:** A delito comparable, las sentencias son más severas para personas con menor escolaridad / ingreso.
- **H5:** Ser hablante de lengua indígena se asocia con peor trato (sentencia más larga o menos debido proceso), controlando por delito.
- **H6 (amplificación):** Un modelo entrenado en las sentencias humanas aplica la disparidad de forma más consistente (100% de los casos) que los jueces (que la aplican a veces) → disparidad agregada mayor.

---

## Ideas sueltas / para después
- ¿La disparidad varía por estado (ENPOL) → mapa de calor de sesgo regional?
- Comparar disparidad entre hombres y mujeres en ambos datasets.
- (Solo describir, no simular) bucle de retroalimentación: decisiones sesgadas → datos futuros sesgados → modelo peor.
