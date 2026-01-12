# Import librairies
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from pathlib import Path

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

DATA_PATH = Path("data/raw")
DATA_PATH.mkdir(parents=True, exist_ok=True)

# Simulation des conseillers
n_advisors = 40
regions = ["Cotonou", "Porto-Novo", "Abomey-Calavi", "Parakou", "Bohicon", "Djougou"]

advisors = []

for i in range(n_advisors):
    advisors.append({
        "advisor_id": f"A{i+1:03d}",
        "advisor_name": f"Advisor {i+1}",
        "region": random.choice(regions),
        "team_id": f"T{random.randint(1,6):02d}",
        "hire_date": (datetime(2018,1,1) + timedelta(days=random.randint(0,2000))).date(),
        "status": "active"
    })

df_advisors = pd.DataFrame(advisors)

# Simulation des produits
products = [
    {"product_id": "P001", "product_name": "Épargne Éducation", "type": "epargne", "avg_premium": 80000},
    {"product_id": "P002", "product_name": "Retraite Plus", "type": "epargne", "avg_premium": 150000},
    {"product_id": "P003", "product_name": "Temporaire Décès", "type": "protection", "avg_premium": 30000},
    {"product_id": "P004", "product_name": "Mixte Avantage", "type": "mixte", "avg_premium": 100000},
]

df_products = pd.DataFrame(products)

#Simulation des leads
n_leads = 3200
start_date = datetime(2025, 1, 1)

leads = []

for i in range(n_leads):
    created_at = start_date + timedelta(days=random.randint(0, 364))
    contacted = random.random() < 0.7

    leads.append({
        "lead_id": f"L{i+1:05d}",
        "created_at": created_at,
        "advisor_id": random.choice(df_advisors["advisor_id"]),
        "product_id": np.random.choice(df_products["product_id"]),
        "lead_source": random.choice(["terrain", "recommendation", "enterprise", "campaign"]),
        "lead_status": "contacted" if contacted else "new"
    })

df_leads = pd.DataFrame(leads)

# Simulation des transactions
transactions = []

for _, lead in df_leads.iterrows():
    if lead["lead_status"] == "contacted" and random.random() < 0.14:
        transactions.append({
            "policy_number": f"POL{random.randint(100000,999999)}",
            "lead_id": lead["lead_id"],
            "advisor_id": lead["advisor_id"],
            "transaction_date": lead["created_at"] + timedelta(days=random.randint(1,45)),
            "premium_amount_fcfa": int(np.random.normal(80000, 30000)),
            "status": "active"
        })

df_transactions = pd.DataFrame(transactions)

# =========================
# Simulation des objectifs commerciaux
# =========================

objectives = []

for _, advisor in df_advisors.iterrows():
    tenure_years = (datetime(2025, 1, 1) - pd.to_datetime(advisor["hire_date"])).days / 365

    # objectif de base selon ancienneté
    if tenure_years < 1:
        base_target = 1_500_000
    elif tenure_years < 3:
        base_target = 3_000_000
    else:
        base_target = 5_000_000

    for month in range(1, 13):
        objectives.append({
            "advisor_id": advisor["advisor_id"],
            "month": f"2025-{month:02d}",
            "target_premium_fcfa": int(
                np.random.normal(base_target, base_target * 0.15)
            )
        })

df_objectives = pd.DataFrame(objectives)


# Sauvegarde des datasets
df_advisors.to_csv(DATA_PATH / "advisors.csv", index=False)
df_products.to_csv(DATA_PATH / "products.csv", index=False)
df_leads.to_csv(DATA_PATH / "leads.csv", index=False)
df_transactions.to_csv(DATA_PATH / "transactions.csv", index=False)
df_objectives.to_csv(DATA_PATH / "objectives.csv", index=False)

