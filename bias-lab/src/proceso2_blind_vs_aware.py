"""
Proceso 2 — Blind vs Aware (¡aquí entra la IA por primera vez!)
==============================================================
Pregunta: ¿El sistema humano estaba USANDO la raza para decidir el riesgo?

Cómo: entrenamos DOS modelos desde cero a imitar la decisión humana ("alto riesgo"):
  - BLIND : nunca ve la raza.
  - AWARE : sí ve la raza.
Y comparamos:
  1) ¿Cuál imita MEJOR la decisión humana? (si aware gana -> la raza traía info usada)
  2) ¿Cómo reparte cada uno el "alto riesgo" entre razas? (disparidad)

Modelo: Regresión logística (ver docs/ADR-001) -> transparente y explicable.
Etiqueta (lo que el modelo aprende a copiar): marcado_alto_riesgo (decisión humana).
"""

import warnings
# El BLAS de macOS (Accelerate) lanza RuntimeWarnings espurios en matmul con Python 3.9.
# No afectan los resultados; los silenciamos para una salida limpia.
warnings.filterwarnings("ignore", category=RuntimeWarning)

import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, roc_auc_score

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "data" / "raw" / "compas-scores-two-years.csv"
FIG = BASE / "reports" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------
# 1. Cargar y filtrar (mismo filtro que el Proceso 1)
# ---------------------------------------------------------------
df = pd.read_csv(RAW)
df = df[
    (df["days_b_screening_arrest"] <= 30)
    & (df["days_b_screening_arrest"] >= -30)
    & (df["is_recid"] != -1)
    & (df["c_charge_degree"] != "O")
    & (df["score_text"] != "N/A")
].copy()

# Nos quedamos con los dos grupos del análisis clásico (raza binaria = interpretación limpia)
df = df[df["race"].isin(["African-American", "Caucasian"])].copy()

# La ETIQUETA: la decisión humana que queremos que el modelo copie
df["marcado_alto_riesgo"] = (df["score_text"] != "Low").astype(int)

print(f"Casos usados: {len(df)}")
print(f"  Afroamericanos: {(df['race']=='African-American').sum()}")
print(f"  Caucásicos:     {(df['race']=='Caucasian').sum()}")

# ---------------------------------------------------------------
# 2. Definir features (lo que el modelo VE) y la etiqueta
# ---------------------------------------------------------------
num_features = ["age", "priors_count", "juv_fel_count", "juv_misd_count", "juv_other_count"]
cat_base = ["sex", "c_charge_degree"]   # categóricas que ambos modelos ven

y = df["marcado_alto_riesgo"]

# Dos conjuntos de columnas de entrada:
X_blind = df[num_features + cat_base]                 # SIN raza
X_aware = df[num_features + cat_base + ["race"]]      # CON raza

# Guardamos raza y reincidencia real APARTE, para auditar (el modelo blind no las usa)
raza = df["race"]
reincidio_real = df["two_year_recid"]

# ---------------------------------------------------------------
# 3. Partir en entrenamiento (aprende) y prueba (examen)
#    Usamos los MISMOS índices para que ambos modelos se examinen con la misma gente.
# ---------------------------------------------------------------
idx_train, idx_test = train_test_split(
    df.index, test_size=0.2, stratify=y, random_state=42
)
print(f"\nEntrenamiento: {len(idx_train)} casos | Examen: {len(idx_test)} casos")


def construir_modelo(columnas_categoricas):
    """Arma el pipeline: preparar datos + regresión logística."""
    prep = ColumnTransformer([
        ("num", StandardScaler(), num_features),
        ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"), columnas_categoricas),
    ])
    return Pipeline([
        ("prep", prep),
        ("clf", LogisticRegression(max_iter=1000)),
    ])


def entrenar_y_evaluar(nombre, X, columnas_categoricas):
    """Entrena un modelo y reporta qué tan bien imita la decisión humana."""
    modelo = construir_modelo(columnas_categoricas)
    modelo.fit(X.loc[idx_train], y.loc[idx_train])

    pred = modelo.predict(X.loc[idx_test])
    proba = modelo.predict_proba(X.loc[idx_test])[:, 1]

    acc = accuracy_score(y.loc[idx_test], pred)
    auc = roc_auc_score(y.loc[idx_test], proba)
    print(f"\n[{nombre}] Qué tan bien imita la decisión humana:")
    print(f"    Accuracy (aciertos): {acc:.3f}")
    print(f"    AUC (capacidad de distinguir): {auc:.3f}")
    return modelo, pred


# ---------------------------------------------------------------
# 4. Entrenar los DOS modelos
# ---------------------------------------------------------------
modelo_blind, pred_blind = entrenar_y_evaluar("BLIND (sin raza)", X_blind, cat_base)
modelo_aware, pred_aware = entrenar_y_evaluar("AWARE (con raza)", X_aware, cat_base + ["race"])

# ---------------------------------------------------------------
# 5. ¿Cómo reparte cada modelo el "alto riesgo" entre razas?
#    (disparidad en las PREDICCIONES sobre el set de examen)
# ---------------------------------------------------------------
raza_test = raza.loc[idx_test]


def tasa_por_raza(predicciones, etiqueta):
    print(f"\n{etiqueta}: % que el modelo predijo 'alto riesgo', por raza")
    s = pd.Series(predicciones, index=idx_test)
    for r in ["African-American", "Caucasian"]:
        val = s[raza_test == r].mean()
        print(f"    {r:<20} {val:6.1%}")
    aa = s[raza_test == "African-American"].mean()
    ca = s[raza_test == "Caucasian"].mean()
    print(f"    >> Brecha (AA - Caucásico): {aa - ca:+.1%}")
    return aa - ca


brecha_blind = tasa_por_raza(pred_blind, "BLIND (sin raza)")
brecha_aware = tasa_por_raza(pred_aware, "AWARE (con raza)")

# ---------------------------------------------------------------
# 6. El coeficiente de la raza en el modelo AWARE (transparencia)
#    Cuánto "empuja" ser afroamericano hacia que lo marquen alto riesgo.
# ---------------------------------------------------------------
nombres = modelo_aware.named_steps["prep"].get_feature_names_out()
coefs = modelo_aware.named_steps["clf"].coef_[0]
print("\n=== Peso (coeficiente) de la variable RAZA en el modelo AWARE ===")
for n, c in zip(nombres, coefs):
    if "race" in n.lower():
        print(f"    {n}: {c:+.3f}  (positivo = empuja hacia 'alto riesgo')")

# ---------------------------------------------------------------
# 7. Gráfica: brecha blind vs aware
# ---------------------------------------------------------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.bar(["BLIND\n(sin raza)", "AWARE\n(con raza)"], [brecha_blind, brecha_aware],
       color=["#55A868", "#C44E52"])
ax.set_title("Brecha racial en las predicciones del modelo\n(% AA marcado alto riesgo − % Caucásico)")
ax.set_ylabel("Brecha (puntos porcentuales)")
ax.axhline(0, color="black", linewidth=0.8)
for i, v in enumerate([brecha_blind, brecha_aware]):
    ax.text(i, v, f"{v:+.1%}", ha="center", va="bottom" if v >= 0 else "top")
plt.tight_layout()
out = FIG / "proceso2_brecha_blind_vs_aware.png"
plt.savefig(out, dpi=120)
print(f"\nGráfica guardada en: {out}")
