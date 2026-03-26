import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# On récupère le chemin du dossier où se trouve le script actuel (src/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# On construit le chemin vers le fichier de manière propre
# On remonte d'un cran (parent de src) puis on descend dans data/raw
DATA_PATH = os.path.join(BASE_DIR, '..', 'data', 'raw', 'train.csv')

print(f"🔍 Recherche du fichier ici : {DATA_PATH}")

try:
    df_raw = pd.read_csv(DATA_PATH)
    print("Fichier trouvé et chargé avec succès !")
except FileNotFoundError:
    print("Erreur : Le fichier n'est toujours pas là. Vérifie bien l'orthographe du nom.")

# --- CONFIGURATION EXPERT : MAPPING MÉTIER ---
REGIONS_CI = {1: "Abidjan", 2: "Bouaké", 3: "San-Pédro", 4: "Yamoussoukro", 5: "Korhogo"}
CHANNELS = {1: "Agence Physique", 2: "Courtage", 3: "Digital/Web", 4: "Télévente"}

def transform_to_professional_schema(df):
    # --- A. TABLE : ADVISORS ---
    # On crée 20 conseillers fictifs basés sur les channels
    advisors_data = []
    for i in range(1, 21):
        advisors_data.append({
            'advisor_id': f"ADV_{i:03d}",
            'advisor_name': f"Agent {chr(64+i)}",
            'region': REGIONS_CI.get(np.random.randint(1, 6), "Autre"),
            'team_id': f"TEAM_{'A' if i < 6 else 'B'}",
            'hire_date': (datetime.now() - timedelta(days=np.random.randint(300, 1000))).date(),
            'status': 'Active'
        })
    df_advisors = pd.DataFrame(advisors_data)

    # --- B. TABLE : LEADS ---
    df_leads = pd.DataFrame()
    df_leads['lead_id'] = df['id'].apply(lambda x: f"LEAD_{x:06d}")
    df_leads['created_at'] = df['Vintage'].apply(lambda x: (datetime.now() - timedelta(days=x)).date())
    df_leads['lead_source'] = df['Policy_Sales_Channel'].map(CHANNELS)
    # Attribution aléatoire d'un conseiller
    df_leads['advisor_id'] = np.random.choice(df_advisors['advisor_id'], len(df))
    df_leads['region'] = df['Region_Code'].map(REGIONS_CI).fillna("Zone Rurale")
    df_leads['expected_premium_fcfa'] = df['Annual_Premium']
    df_leads['lead_status'] = df['Response'].apply(lambda x: 'Converted' if x == 1 else 'Lost')
    
    # --- C. TABLE : TRANSACTIONS ---
    # --- LOGIQUE PARETO (Le secret des experts) ---
    # 1. On donne un "Score de Talent" à chaque conseiller
    # On définit les 18% d'élite
    num_advisors = len(df_advisors)
    num_elite = max(1, int(num_advisors * 0.2))
    elite_advisors = df_advisors.sample(num_elite)['advisor_id'].values
    
    # 2. On modifie les probabilités de conversion
    # Si le lead est affecté à une élite, il a bcp plus de chance de signer
    def apply_pareto_logic(row):
        is_elite = row['advisor_id'] in elite_advisors
        if is_elite:
            # L'élite convertit 70% de ses leads
            return np.random.choice(['Converted', 'Lost'], p=[0.70, 0.30])
        else:
            # Les autres convertissent beaucoup moins (ex: 5%)
            return np.random.choice(['Converted', 'Lost'], p=[0.05, 0.95])

    df_leads['lead_status'] = df_leads.apply(apply_pareto_logic, axis=1)
    
    # 3. On crée les transactions basées sur ce nouveau statut
    df_sales = df_leads[df_leads['lead_status'] == 'Converted'].copy()
    
    # Pour que l'élite génère aussi des primes PLUS HAUTES (70% du CA)
    def scale_premium(row):
        is_elite = row['advisor_id'] in elite_advisors
        return row['expected_premium_fcfa'] * (2.5 if is_elite else 0.8)
    
    df_sales['premium_amount_fcfa'] = df_sales.apply(scale_premium, axis=1)
    
    df_transactions = pd.DataFrame()
    df_transactions['transaction_id'] = df_sales['lead_id'].str.replace('LEAD_', 'TX_')
    df_transactions['policy_number'] = df_sales['lead_id'].str.replace('LEAD_', 'POL-')
    df_transactions['lead_id'] = df_sales['lead_id']
    df_transactions['advisor_id'] = df_sales['advisor_id']
    df_transactions['region'] = df_sales['region']
    df_transactions['product_id'] = "PROD_LIFE_01"
    df_transactions['transaction_date'] = datetime.now().date()
    df_transactions['premium_amount_fcfa'] = df_sales['premium_amount_fcfa']
    df_transactions['status'] = 'In Force'

    return df_advisors, df_leads, df_transactions

# Exécution
advisors, leads, transactions = transform_to_professional_schema(df_raw)

# --- VÉRIFICATION D'EXPERT ---
print(f"Leads générés : {len(leads)}")
print(f"Transactions (Conversions) : {len(transactions)}")
print(f"Taux de conversion réel : {(len(transactions)/len(leads)*100):.2f}%")

# --- SAUVEGARDE DES TABLES ---

# On définit le dossier de destination (data/raw)
output_dir = os.path.join(BASE_DIR, '..', 'data', 'raw')

# On s'assure que le dossier existe (au cas où)
os.makedirs(output_dir, exist_ok=True)

# Sauvegarde des fichiers
advisors.to_csv(os.path.join(output_dir, 'advisors.csv'), index=False)
leads.to_csv(os.path.join(output_dir, 'leads.csv'), index=False)
transactions.to_csv(os.path.join(output_dir, 'transactions.csv'), index=False)

print(f"Succès ! Les 3 fichiers ont été générés dans : {output_dir}")