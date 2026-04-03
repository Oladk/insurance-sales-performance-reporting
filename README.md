# Insurance Sales Performance Reporting: Synthetic Data Project

> **Version 2.0** : Pipeline corrigé, 5 tables générées, cohérence simulation ↔ ML garantie.

---

## 1. Contexte du projet

Ce projet simule un cas réel de **pilotage de la performance commerciale** pour une compagnie d'assurance vie opérant en Afrique de l'Ouest (contexte Côte d'Ivoire).

Dans de nombreux contextes professionnels, les équipes data ne disposent pas immédiatement d'une base de données SQL prête ou de données exploitables pour démarrer l'analyse. L'objectif est donc de **reproduire un environnement réaliste** afin de :
- Structurer un modèle de données cohérent (5 tables relationnelles)
- Définir et calculer des KPIs commerciaux pertinents
- Analyser la performance du réseau de vente (conseillers, régions, produits, temps)
- Construire un **modèle de lead scoring** opérationnel

Toutes les données sont **simulées**, mais reposent sur des **hypothèses métier réalistes et documentées**.

---

## 2. Objectifs métier

- Suivre la performance commerciale globale (primes collectées, contrats souscrits)
- Mesurer la performance vs objectifs (réalisation / cible)
- Analyser le funnel de vente (leads → contacts → conversions)
- Comparer la performance par région, conseiller, produit, canal
- **Prioriser les leads** via un score de conversion (lead scoring ML)

---

## 3. Hypothèses de simulation

| Paramètre | Valeur |
|-----------|--------|
| Conseillers actifs | **40** |
| Régions | **6** (Abidjan, Bouaké, San-Pédro, Yamoussoukro, Korhogo, Daloa) |
| Produits | **6** (Épargne, Protection, Mixte) |
| Canaux de contact | **4** (Agence Physique, Courtage, Digital/Web, Télévente) |
| Leads / source externe | ~382000 (dataset Kaggle Health Insurance) |
| Taux de leads contactés | ~72% |
| Taux de conversion moyen | ~18% (variable par canal, région, ancienneté) |

**Logique de conversion (v2 — corrigée) :**
La probabilité de conversion est une **fonction déterministe des features observables** :
```
p_convert = base_channel_rate + region_bonus + seniority_bonus + premium_bonus + ε
```
Cela garantit la **cohérence end-to-end** : le modèle ML peut apprendre les drivers réels de la conversion car ils sont présents dans les features.

> ⚠️ **Fix v1 → v2 :** La version précédente basait la conversion sur un flag "elite" caché, non inclus dans les features ML. L'AUC-ROC résultante était mécaniquement de 0.50 (aléatoire).

---

## 4. Modèle de données

### `advisors.csv`
| Colonne | Description |
|---------|-------------|
| advisor_id | Identifiant unique (ex: ADV_001) |
| advisor_name | Nom fictif |
| region | Région d'affectation |
| team_id | Équipe (TEAM_A à TEAM_D) |
| hire_date | Date d'embauche |
| seniority_days | Ancienneté en jours (**feature ML**) |
| talent_tier | Senior / Mid / Junior (**feature ML**) |
| status | Active |

### `products.csv`
| Colonne | Description |
|---------|-------------|
| product_id | Identifiant produit |
| product_name | Nom commercial |
| product_type | Épargne / Protection / Mixte |
| avg_premium | Prime moyenne de référence (FCFA) |

### `leads.csv`
| Colonne | Description |
|---------|-------------|
| lead_id | Identifiant unique |
| created_at | Date de création |
| lead_source | Canal d'origine (**feature ML**) |
| advisor_id | Conseiller assigné |
| talent_tier | Niveau du conseiller assigné (**feature ML**) |
| seniority_days | Ancienneté du conseiller (**feature ML**) |
| region | Région (**feature ML**) |
| product_id | Produit associé |
| expected_premium_fcfa | Prime attendue (**feature ML**) |
| lead_status | Converted / Lost (**target**) |
| contacted_at | Date de contact (peut être null) |

### `transactions.csv`
| Colonne | Description |
|---------|-------------|
| transaction_id | Identifiant unique |
| policy_number | Numéro de police |
| lead_id | Lead source (FK → leads) |
| advisor_id | Conseiller vendeur |
| region | Région de la vente |
| product_id | Produit souscrit |
| transaction_date | Date de souscription |
| premium_amount_fcfa | Prime réelle collectée (FCFA) |
| status | In Force |

### `objectives.csv`
| Colonne | Description |
|---------|-------------|
| level | advisor |
| level_id | advisor_id concerné |
| period_start / period_end | Période de l'objectif (mensuel) |
| metric | nb_contracts ou premium_fcfa |
| target_value | Valeur cible |

---

## 5. Structure du projet

```
project-root/
│
├── data/
│   └── raw/
│       ├── advisors.csv
│       ├── products.csv
│       ├── leads.csv
│       ├── transactions.csv
│       └── objectives.csv
│
├── src/
│   ├── data_simulation_v2.py        # Générateur de données (v2)
├   └── data_simulation.py 
│
├── notebooks/
│   ├── 01_sales_performance_eda.ipynb   # EDA (6 analyses)
│   ├── 02_predictive_modeling.ipynb     # Lead Scoring ML
│   └── 03_advanced_modeling.ipynb       # XGBoost + SHAP
│
├── reports/
│   └── Synthese_commerciale.md
│
└── README.md
```

---

## 6. KPIs mesurés

| KPI | Description |
|-----|-------------|
| Taux de conversion | % leads convertis en contrats |
| Prime totale (FCFA) | Chiffre d'affaires total |
| Prime par lead | Valeur économique d'un lead (incl. non convertis) |
| Taux d'atteinte objectif | Réalisé / Cible (%) |
| Concentration Pareto | % de conseillers générant 80% du CA |
| Lead Score | Probabilité de conversion [0–100] |

---

## 7. Pipeline ML

| Étape | Choix technique | Justification |
|-------|----------------|---------------|
| Encodage catégoriel | `OneHotEncoder` | Pas de relation ordinale entre catégories |
| Déséquilibre des classes | `class_weight='balanced'` | Ratio 82/18 → le modèle sans balance prédit toujours 0 |
| Validation | `StratifiedKFold(5)` | Préserve la proportion de positifs dans chaque fold |
| Métriques | AUC-ROC + Average Precision + F1 | L'accuracy est trompeuse sur données déséquilibrées |
| Seuil de décision | Optimisé sur F1 classe 1 | Le seuil 0.5 par défaut n'est pas optimal |

---

## 8. Outils & Stack

- **Python 3.14.2** : pandas, numpy, scikit-learn, matplotlib, seaborn
- **Jupyter Notebooks** ! analyse et modélisation
- **CSV** : format de stockage (extensible vers SQL/Parquet)

---

## 9. Statut du projet

| Notebook | Statut |
|----------|--------|
| `data_simulation.py` | ✅ v2 — 5 tables, cohérence ML garantie |
| `01_sales_performance_eda.ipynb` | ✅ v2 — 6 analyses, visualisations pro |
| `02_predictive_modeling.ipynb` | ✅ v2 — Pipeline complet, AUC > baseline |
