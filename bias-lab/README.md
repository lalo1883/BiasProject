# bias-lab
Código del proyecto **"IA como lupa de sesgos"**. Tesis: la IA aprende los sesgos de las
decisiones humanas y los *amplifica*, volviéndolos visibles y medibles.

## Estructura
```
bias-lab/
├── data/raw/          # datasets originales (no se versionan)
├── data/processed/    # datos limpios
├── notebooks/         # exploración
├── src/               # scripts de cada proceso
│   └── proceso1_tasas_base.py
├── reports/figures/   # gráficas generadas
├── docs/              # datasheets, model cards (gobernanza)
├── requirements.txt
└── venv/              # entorno virtual (no se versiona)
```

## Cómo correr
```bash
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
./venv/bin/python src/proceso1_tasas_base.py
```

## Procesos (ver ../Procesos.md)
1. ✅ Tasas base (COMPAS) — disparidad cruda sin IA
2. ⬜ Blind vs Aware — el detector de sesgo
3. ⬜ Cazando proxies
4. ⬜ Medir amplificación (clímax)
5. ⬜ SHAP
6. ⬜ No-supervisado (confirmación)
7. ⬜ Métricas de equidad

## Datasets
- **COMPAS** (validación del método) — ProPublica, condado de Broward.
- **ENPOL 2021** (caso mexicano) — INEGI. *Pendiente de descarga manual.*
