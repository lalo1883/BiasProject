"""
Proceso 3 — Cazando proxies
===========================
Pregunta: Si borré la raza y el modelo SIGUE discriminando, ¿qué variable la está
sustituyendo? Hipótesis: `priors_count` (delitos previos), que refleja la sobre-vigilancia
policial, no la peligrosidad real.

Plan:
  1) Medir si `priors_count` está correlacionado con la raza (¿un grupo tiene más arrestos
     previos registrados?).
  2) Entrenar un modelo "blind SIN proxies" (sin raza Y sin historial criminal) y ver si
     por fin baja la brecha. Si baja -> los proxies eran los culpables.
  3) Comparar las brechas de los 3 escenarios.
"""

import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)  # BLAS macOS: avisos espurios

import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "data" / "raw" / "compas-scores-two-years.csv"
FIG = BASE / "reports" / "figures"

# ---------------------------------------------------------------
# 1. Cargar y filtrar (igual que antes)
# ---------------------------------------------------------------
df = pd.read_csv(RAW)
df = df[
    (df["days_b_screening_arrest"] <= 30)
    & (df["days_b_screening_arrest"] >= -30)
    & (df["is_recid"] != -1)
    & (df["c_charge_degree"] != "O")
    & (df["score_text"] != "N/A")
].copy()
df = df[df["race"].isin(["African-American", "Caucasian"])].copy()
df["marcado_alto_riesgo"] = (df["score_text"] != "Low").astype(int)

# ---------------------------------------------------------------
# 2. ¿`priors_count` está correlacionado con la raza?
# ---------------------------------------------------------------
print("=== ¿El proxy carga la raza? Promedio de delitos previos por raza ===")
prom = df.groupby("race")["priors_count"].mean()
for r, v in prom.items():
    print(f"    {r:<20} {v:.2f} delitos previos (promedio)")
aa = prom["African-American"]
ca = prom["Caucasian"]
print(f"    >> Los afroamericanos tienen {aa/ca:.1f}x más arrestos previos REGISTRADOS")
print("       OJO: esto es una CORRELACIÓN. Con estos datos NO podemos saber el porqué")
print("       (sobre-vigilancia, factores socioeconómicos, etc.). Solo vemos la relación.")

# ---------------------------------------------------------------
# 3. Tres escenarios de features
# ---------------------------------------------------------------
num_full = ["age", "priors_count", "juv_fel_count", "juv_misd_count", "juv_other_count"]
num_sin_proxy = ["age"]               # quitamos TODO el historial criminal
cat_base = ["sex", "c_charge_degree"]

y = df["marcado_alto_riesgo"]
raza = df["race"]

escenarios = {
    "AWARE (raza + historial)":      (num_full, cat_base + ["race"]),
    "BLIND (sin raza, con historial)": (num_full, cat_base),
    "BLIND SIN PROXIES (sin raza ni historial)": (num_sin_proxy, cat_base),
}

idx_train, idx_test = train_test_split(df.index, test_size=0.2, stratify=y, random_state=42)
raza_test = raza.loc[idx_test]


def evaluar(nums, cats):
    """Devuelve (brecha racial, accuracy) del modelo en el set de examen."""
    prep = ColumnTransformer([
        ("num", StandardScaler(), nums),
        ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"), cats),
    ])
    modelo = Pipeline([("prep", prep), ("clf", LogisticRegression(max_iter=1000))])
    X = df[nums + cats]
    modelo.fit(X.loc[idx_train], y.loc[idx_train])
    pred = pd.Series(modelo.predict(X.loc[idx_test]), index=idx_test)
    aa = pred[raza_test == "African-American"].mean()
    ca = pred[raza_test == "Caucasian"].mean()
    acc = accuracy_score(y.loc[idx_test], pred)
    return aa - ca, acc


print("\n=== Brecha racial Y accuracy según qué ve el modelo ===")
print(f"    {'ESCENARIO':<45} {'BRECHA':>8}  {'ACCURACY':>9}")
resultados = {}
for nombre, (nums, cats) in escenarios.items():
    g, acc = evaluar(nums, cats)
    resultados[nombre] = g
    print(f"    {nombre:<45} {g:>+7.1%}  {acc:>8.1%}")

print("\nInterpretación:")
print("  - Si la brecha CAE al quitar el historial -> los proxies eran los culpables.")
print("  - Lo que quede es el sesgo que NO se explica por esas variables.")

# ---------------------------------------------------------------
# 4. Gráfica comparativa
# ---------------------------------------------------------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

nombres = list(resultados.keys())
valores = list(resultados.values())
colores = ["#C44E52", "#DD8452", "#55A868"]

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.barh(range(len(nombres)), valores, color=colores)
ax.set_yticks(range(len(nombres)))
ax.set_yticklabels([n.replace(" (", "\n(") for n in nombres], fontsize=9)
ax.set_xlabel("Brecha racial en predicciones (AA − Caucásico)")
ax.set_title("Cazando el proxy: la brecha al ir quitando información")
ax.axvline(0, color="black", linewidth=0.8)
for i, v in enumerate(valores):
    ax.text(v, i, f" {v:+.1%}", va="center")
plt.tight_layout()
out = FIG / "proceso3_cazando_proxies.png"
plt.savefig(out, dpi=120)
print(f"\nGráfica guardada en: {out}")
