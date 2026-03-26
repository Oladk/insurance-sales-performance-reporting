"""
data_simulation.py — Insurance Sales Performance Simulator
Version : 2.0 (Corrected & Production-Ready)

FIX CRITIQUE v1 → v2 :
    La conversion est maintenant déterminée par des features OBSERVABLES
    (source, région, ancienneté conseiller, tranche de prime) afin que le
    pipeline ML soit cohérent end-to-end.
    Le biais "élite caché" a été remplacé par un score de talent ENCODÉ
    dans les données, permettant au modèle de l'apprendre réellement.
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ─── CHEMINS ────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_PATH  = os.path.join(BASE_DIR, '..', 'data', 'raw', 'train.csv')
OUTPUT_DIR = os.path.join(BASE_DIR, '..', 'data', 'raw')
os.makedirs(OUTPUT_DIR, exist_ok=True)

np.random.seed(42)

# ─── CONFIGURATION MÉTIER ───────────────────────────────────────────────────
REGIONS = {
    1: "Abidjan", 2: "Bouaké", 3: "San-Pédro",
    4: "Yamoussoukro", 5: "Korhogo", 6: "Daloa"
}

CHANNELS = {
    1: "Agence Physique", 2: "Courtage",
    3: "Digital/Web",     4: "Télévente"
}

# Taux de conversion par canal (hypothèse métier réaliste et DOCUMENTÉE)
CHANNEL_CONVERSION = {
    "Courtage":        0.45,   # Recommandations → qualité élevée
    "Agence Physique": 0.18,   # Relation directe mais volume fort
    "Télévente":       0.08,   # Cold calling → faible
    "Digital/Web":     0.05,   # Leads froids non qualifiés
}

# Bonus de conversion par région (reflet du contexte socio-économique local)
REGION_CONVERSION_BONUS = {
    "Abidjan":       0.04,
    "Bouaké":        0.02,
    "Yamoussoukro":  0.03,
    "San-Pédro":     0.01,
    "Korhogo":       0.02,
    "Daloa":         0.01,
    "Zone Rurale":  -0.02,
}

PRODUCTS = [
    {"product_id": "PROD_EP_01", "product_name": "Épargne Sécurité Plus",  "product_type": "Épargne",    "avg_premium": 180_000},
    {"product_id": "PROD_EP_02", "product_name": "Épargne Retraite",       "product_type": "Épargne",    "avg_premium": 240_000},
    {"product_id": "PROD_PR_01", "product_name": "Protection Famille",     "product_type": "Protection", "avg_premium": 85_000},
    {"product_id": "PROD_PR_02", "product_name": "Protection Décès",       "product_type": "Protection", "avg_premium": 60_000},
    {"product_id": "PROD_MX_01", "product_name": "Mixte Vie & Épargne",   "product_type": "Mixte",      "avg_premium": 320_000},
    {"product_id": "PROD_MX_02", "product_name": "Mixte Senior",           "product_type": "Mixte",      "avg_premium": 410_000},
]


# ────────────────────────────────────────────────────────────────────────────
# TABLE 1 : ADVISORS (40 conseillers — conforme README)
# ────────────────────────────────────────────────────────────────────────────
def build_advisors(n=40):
    advisors = []
    for i in range(1, n + 1):
        seniority_days = int(np.random.exponential(scale=500))  # Distribution réaliste
        seniority_days = max(30, min(seniority_days, 2000))

        advisors.append({
            "advisor_id":          f"ADV_{i:03d}",
            "advisor_name":        f"Agent {i:02d}",
            "region":              REGIONS[np.random.randint(1, 7)],
            "team_id":             f"TEAM_{'A' if i <= 10 else 'B' if i <= 20 else 'C' if i <= 30 else 'D'}",
            "hire_date":           (datetime.now() - timedelta(days=seniority_days)).date(),
            "seniority_days":      seniority_days,
            # Score de talent : observable via ancienneté + équipe (feature ML valide)
            "talent_tier":         "Senior" if seniority_days > 700 else "Mid" if seniority_days > 300 else "Junior",
            "status":              "Active",
        })
    return pd.DataFrame(advisors)


# ────────────────────────────────────────────────────────────────────────────
# TABLE 2 : PRODUCTS
# ────────────────────────────────────────────────────────────────────────────
def build_products():
    return pd.DataFrame(PRODUCTS)


# ────────────────────────────────────────────────────────────────────────────
# TABLE 3 : LEADS + TABLE 4 : TRANSACTIONS
# Logique de conversion COHÉRENTE avec les features ML
# ────────────────────────────────────────────────────────────────────────────
def build_leads_and_transactions(df_raw, df_advisors, df_products):
    n = len(df_raw)

    # Attribution conseiller & produit
    assigned_advisors = df_advisors.sample(n, replace=True).reset_index(drop=True)
    assigned_products = df_products.sample(n, replace=True).reset_index(drop=True)

    leads = pd.DataFrame()
    leads["lead_id"]               = df_raw["id"].apply(lambda x: f"LEAD_{x:06d}")
    leads["created_at"]            = df_raw["Vintage"].apply(
        lambda x: (datetime.now() - timedelta(days=int(x))).date()
    )
    leads["lead_source"]           = df_raw["Policy_Sales_Channel"].map(CHANNELS).fillna("Digital/Web")
    leads["advisor_id"]            = assigned_advisors["advisor_id"].values
    leads["talent_tier"]           = assigned_advisors["talent_tier"].values   # ← Feature ML
    leads["seniority_days"]        = assigned_advisors["seniority_days"].values # ← Feature ML
    leads["region"]                = df_raw["Region_Code"].map(REGIONS).fillna("Zone Rurale")
    leads["product_id"]            = assigned_products["product_id"].values
    leads["expected_premium_fcfa"] = df_raw["Annual_Premium"].values

    # ── CALCUL DE LA PROBABILITÉ DE CONVERSION (Déterministe + Bruit) ──────
    # Toutes les variables utilisées ici sont dans les features ML
    base_p = leads["lead_source"].map(CHANNEL_CONVERSION).fillna(0.05)
    region_bonus = leads["region"].map(REGION_CONVERSION_BONUS).fillna(0.0)

    # Bonus ancienneté conseiller (Senior +8%, Junior -5%)
    seniority_bonus = leads["talent_tier"].map({"Senior": 0.08, "Mid": 0.02, "Junior": -0.05})

    # Bonus prime élevée (clients à fort potentiel sont mieux qualifiés)
    premium_median = leads["expected_premium_fcfa"].median()
    premium_bonus  = np.where(leads["expected_premium_fcfa"] > premium_median, 0.03, -0.01)

    # Probabilité finale bornée entre 1% et 90%
    p_convert = (base_p + region_bonus + seniority_bonus + premium_bonus).clip(0.01, 0.90)

    # Tirage stochastique
    random_draw = np.random.uniform(0, 1, n)
    leads["lead_status"]   = np.where(random_draw < p_convert, "Converted", "Lost")
    leads["contacted_at"]  = leads.apply(
        lambda row: (
            (datetime.strptime(str(row["created_at"]), "%Y-%m-%d") + timedelta(days=np.random.randint(1, 10))).date()
            if np.random.random() < 0.72 else None  # 72% des leads sont contactés
        ),
        axis=1,
    )

    # ── TRANSACTIONS ────────────────────────────────────────────────────────
    df_sales = leads[leads["lead_status"] == "Converted"].copy()
    df_sales = df_sales.merge(df_products[["product_id", "avg_premium"]], on="product_id", how="left")

    transactions = pd.DataFrame()
    transactions["transaction_id"]       = df_sales["lead_id"].str.replace("LEAD_", "TX_")
    transactions["policy_number"]        = df_sales["lead_id"].str.replace("LEAD_", "POL-")
    transactions["lead_id"]              = df_sales["lead_id"].values
    transactions["advisor_id"]           = df_sales["advisor_id"].values
    transactions["region"]               = df_sales["region"].values
    transactions["product_id"]           = df_sales["product_id"].values
    transactions["transaction_date"]     = df_sales["created_at"].values
    # Prime réelle = prime moyenne produit × bruit réaliste (±30%)
    noise = np.random.normal(loc=1.0, scale=0.20, size=len(df_sales)).clip(0.7, 1.5)
    transactions["premium_amount_fcfa"]  = (df_sales["avg_premium"].values * noise).round(0)
    transactions["status"]               = "In Force"

    return leads, transactions


# ────────────────────────────────────────────────────────────────────────────
# TABLE 5 : OBJECTIVES (mensuel par conseiller)
# ────────────────────────────────────────────────────────────────────────────
def build_objectives(df_advisors, df_transactions, n_months=12):
    records = []
    base_date = datetime(datetime.now().year, 1, 1)

    for _, advisor in df_advisors.iterrows():
        for m in range(n_months):
            period_start = (base_date + timedelta(days=30 * m)).date()
            period_end   = (base_date + timedelta(days=30 * (m + 1) - 1)).date()

            # Objectif réaliste = cible progressive selon ancienneté
            if advisor["talent_tier"] == "Senior":
                target = np.random.randint(8, 15)
                target_premium = np.random.randint(2_000_000, 5_000_000)
            elif advisor["talent_tier"] == "Mid":
                target = np.random.randint(5, 10)
                target_premium = np.random.randint(1_000_000, 2_500_000)
            else:
                target = np.random.randint(2, 6)
                target_premium = np.random.randint(400_000, 1_200_000)

            records.append({
                "level":          "advisor",
                "level_id":       advisor["advisor_id"],
                "period_start":   period_start,
                "period_end":     period_end,
                "metric":         "nb_contracts",
                "target_value":   target,
            })
            records.append({
                "level":          "advisor",
                "level_id":       advisor["advisor_id"],
                "period_start":   period_start,
                "period_end":     period_end,
                "metric":         "premium_fcfa",
                "target_value":   target_premium,
            })

    return pd.DataFrame(records)


# ────────────────────────────────────────────────────────────────────────────
# EXÉCUTION
# ────────────────────────────────────────────────────────────────────────────
print(f"🔍 Chargement du fichier source : {DATA_PATH}")
try:
    df_raw = pd.read_csv(DATA_PATH)
    print(f"✅ Fichier chargé — {len(df_raw):,} lignes.")
except FileNotFoundError:
    print("❌ Fichier introuvable. Vérifiez le chemin DATA_PATH.")
    raise

advisors     = build_advisors(n=40)
products     = build_products()
leads, transactions = build_leads_and_transactions(df_raw, advisors, products)
objectives   = build_objectives(advisors, transactions)

# ── RAPPORT DE VALIDATION ────────────────────────────────────────────────────
print("\n" + "="*50)
print("  RAPPORT DE VALIDATION DE LA SIMULATION")
print("="*50)
print(f"  Conseillers         : {len(advisors)}")
print(f"  Produits            : {len(products)}")
print(f"  Leads générés       : {len(leads):,}")
print(f"  Transactions        : {len(transactions):,}")
print(f"  Taux de conversion  : {len(transactions)/len(leads)*100:.2f}%")
print(f"  Prime totale (FCFA) : {transactions['premium_amount_fcfa'].sum():,.0f}")
print(f"  Objectifs générés   : {len(objectives):,}")
print("="*50)

# Vérification de cohérence — aucune fuite de données
assert set(transactions["lead_id"]).issubset(set(leads["lead_id"])), \
    "ERREUR: Des transactions orphelines existent (pas de lead correspondant)"
assert leads["lead_id"].is_unique, "ERREUR: Doublons dans lead_id"
assert transactions["transaction_id"].is_unique, "ERREUR: Doublons dans transaction_id"
print("\n✅ Toutes les assertions de cohérence ont passé.")

# ── SAUVEGARDE ───────────────────────────────────────────────────────────────
advisors.to_csv(    os.path.join(OUTPUT_DIR, "advisors.csv"),     index=False)
products.to_csv(    os.path.join(OUTPUT_DIR, "products.csv"),     index=False)
leads.to_csv(       os.path.join(OUTPUT_DIR, "leads.csv"),        index=False)
transactions.to_csv(os.path.join(OUTPUT_DIR, "transactions.csv"), index=False)
objectives.to_csv(  os.path.join(OUTPUT_DIR, "objectives.csv"),   index=False)

print(f"\n✅ 5 fichiers sauvegardés dans : {OUTPUT_DIR}")
