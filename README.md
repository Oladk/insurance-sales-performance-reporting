# Insurance Sales Performance Reporting (Synthetic Data Project)

## 1. Contexte du projet

Ce projet simule un cas réel de **pilotage de la performance commerciale** pour une compagnie d’assurance vie opérant en Afrique de l’Ouest.

Dans de nombreux contextes professionnels, les équipes data ne disposent pas immédiatement :
- d’une base de données SQL prête,
- ou de données exploitables pour démarrer l’analyse.

L’objectif ici est donc de **reproduire un environnement réaliste** de ventes assurance vie à partir de données synthétiques, afin de :
- structurer un modèle de données cohérent,
- définir des indicateurs commerciaux pertinents,
- analyser la performance du réseau de vente (conseillers, régions, produits).

Toutes les données utilisées dans ce projet sont **simulées**, mais reposent sur des **hypothèses métier réalistes** adaptées au contexte africain.

---

## 2. Objectifs métier

Les objectifs business du projet sont les suivants :

- Suivre la performance commerciale globale (primes collectées, contrats souscrits)
- Mesurer la performance vs objectifs (réalisation / cible) pour prioriser actions.
- Analyser le funnel de vente (leads → contacts → conversions)
- Comparer la performance par :
  - région,
  - conseiller,
  - produit,
  - source de lead
- Évaluer l’atteinte des objectifs commerciaux mensuels

---

## 3. Hypothèses de simulation (réalistes)

Les données ont été générées selon les hypothèses suivantes :

- Environ **40 conseillers commerciaux actifs**
- Répartition géographique sur **6 régions** majeures
- **6 produits d’assurance vie** (épargne, protection, mixte)
- Environ **3 200 leads** générés sur une année
- Environ **70 % des leads sont contactés**
- Taux de conversion moyen :
  - leads contactés : ~14 %
  - leads non contactés : ~2 %
- Les leads issus de recommandations ont une meilleure conversion
- Les campagnes marketing ont une conversion plus faible
- Les primes suivent une distribution réaliste autour d’une moyenne produit
- Objectifs commerciaux définis **mensuellement par conseiller**

Ces hypothèses sont volontairement documentées afin de rendre l’analyse **compréhensible, transparente et défendable**.

---

## 4. Modèle de données

Le projet repose sur cinq entités principales :

### Advisors (`advisors.csv`)
Informations sur le réseau commercial.
- advisor_id
- advisor_name
- region
- team_id
- hire_date
- status

### Products (`products.csv`)
Catalogue des produits d’assurance vie.
- product_id
- product_name
- product_type
- avg_premium

### Leads (`leads.csv`)
Pipeline commercial et prospection.
- lead_id
- created_at
- lead_source
- advisor_id
- region
- expected_premium_fcfa
- lead_status
- contacted_at

### Transactions (`transactions.csv`)
Contrats effectivement souscrits.
- transaction_id
- policy_number
- lead_id
- advisor_id
- product_id
- transaction_date
- premium_amount_fcfa
- region
- status

### Objectives (`objectives.csv`)
Objectifs commerciaux mensuels.
- level (advisor)
- level_id
- period_start
- period_end
- metric
- target_value

---

## 5. Structure du projet

```text
project-root/
│
├── data/
│   └── raw/              # Données brutes simulées (CSV)
│
├── src/
│   └── data_simulation.py  # Script de génération des données
│
├── notebooks/
│   └── 01_eda_sales_data.ipynb  # Analyse exploratoire (EDA)
│
└── README.md

## Key indicators (KPIs)
- Number of contracts
- Sales amount (premium / revenue)
- Conversion rate
- Performance vs objective (%)
- Time to close
- Advisor ranking (top / bottom)

## Target users
- Sales managers
- Network supervisors
- Commercial performance analysts

## Tools
- SQL
- Excel (Power Query)
- Power BI
- Python

## Project status
Project initialization – data modeling and KPI definition in progress.
