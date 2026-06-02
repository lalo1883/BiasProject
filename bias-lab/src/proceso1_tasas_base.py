"""
Proceso 1 — Tasas base (sin IA, el calentamiento)
==================================================
Pregunta: ¿Ya hay disparidad cruda en las decisiones humanas, sin tocar ningún modelo?

Dataset: COMPAS (ProPublica) — acusados del condado de Broward, FL (2013-2014).
- Decisión humana/algorítmica:  decile_score (1-10) y score_text (Low/Medium/High)
- Ground truth real:            two_year_recid (¿reincidió en 2 años? 1=sí, 0=no)
- Variable protegida:           race

NO usamos IA aquí. Solo contamos. Esto es media historia.
"""

import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "data" / "raw" / "compas-scores-two-years.csv"
FIG = BASE / "reports" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------
# 1. Cargar
# ---------------------------------------------------------------
df = pd.read_csv(RAW)
print(f"Filas crudas: {len(df)}")

# ---------------------------------------------------------------
# 2. Filtro estándar de ProPublica (para quedarnos con casos válidos)
#    - el screening ocurrió cerca del arresto (+/- 30 días)
#    - se sabe si reincidió (is_recid != -1)
#    - el cargo no es de tipo "O"
#    - hay texto de score
# ---------------------------------------------------------------
df = df[
    (df["days_b_screening_arrest"] <= 30)
    & (df["days_b_screening_arrest"] >= -30)
    & (df["is_recid"] != -1)
    & (df["c_charge_degree"] != "O")
    & (df["score_text"] != "N/A")
].copy()
print(f"Filas tras filtro ProPublica: {len(df)}")

# "Alto riesgo" = el sistema lo marcó Medium o High (score 5-10)
df["marcado_alto_riesgo"] = (df["score_text"] != "Low").astype(int)

# Nos enfocamos en los dos grupos del análisis clásico
foco = df[df["race"].isin(["African-American", "Caucasian"])]

# ---------------------------------------------------------------
# 3. TASA BASE: ¿a qué % de cada raza lo marcaron "alto riesgo"?
# ---------------------------------------------------------------
print("\n=== TASA BASE: % marcado 'alto riesgo' (Medium/High) por raza ===")
tasa = df.groupby("race")["marcado_alto_riesgo"].mean().sort_values(ascending=False)
for raza, val in tasa.items():
    print(f"  {raza:<20} {val:6.1%}")

# ---------------------------------------------------------------
# 4. EL HALLAZGO DE ProPublica: falsos positivos por raza
#    Entre los que NO reincidieron, ¿a quién lo marcaron alto riesgo
#    por error? (falso positivo = injusticia)
# ---------------------------------------------------------------
print("\n=== FALSOS POSITIVOS: de los que NO reincidieron, % marcado 'alto riesgo' ===")
no_reincidio = foco[foco["two_year_recid"] == 0]
fp = no_reincidio.groupby("race")["marcado_alto_riesgo"].mean()
for raza, val in fp.items():
    print(f"  {raza:<20} {val:6.1%}  (marcados alto riesgo SIN reincidir)")

print("\n=== FALSOS NEGATIVOS: de los que SÍ reincidieron, % marcado 'bajo riesgo' ===")
si_reincidio = foco[foco["two_year_recid"] == 1]
fn = si_reincidio.groupby("race")["marcado_alto_riesgo"].apply(
    lambda s: (s == 0).mean()
)
for raza, val in fn.items():
    print(f"  {raza:<20} {val:6.1%}  (marcados bajo riesgo PESE a reincidir)")

# ---------------------------------------------------------------
# 5. Gráfica simple del hallazgo de falsos positivos
# ---------------------------------------------------------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ax = fp.sort_values().plot(kind="barh", color=["#4C72B0", "#C44E52"])
ax.set_title("Falsos positivos por raza (COMPAS)\nMarcados 'alto riesgo' SIN haber reincidido")
ax.set_xlabel("Proporción")
for i, v in enumerate(fp.sort_values()):
    ax.text(v + 0.005, i, f"{v:.0%}", va="center")
plt.tight_layout()
out = FIG / "proceso1_falsos_positivos.png"
plt.savefig(out, dpi=120)
print(f"\nGráfica guardada en: {out}")
