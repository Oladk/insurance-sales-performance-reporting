# SYNTHÈSE MANAGEMENT - PERFORMANCE COMMERCIALE
## Réseau de Vente Assurance Vie | Afrique de l'Ouest

---

> **Usage :** Ce document est la synthèse exécutive destinée au management. Il repose sur l'analyse complète réalisée dans `01_sales_performance_eda.ipynb`.

---

## 1. Vue d'ensemble : Chiffres Clés

| KPI | Valeur | Commentaire |
|-----|--------|-------------|
| **Leads générés** | 381 109 | Périmètre total de l'analyse |
| **Contrats souscrits** | 16 477 | Leads effectivement convertis |
| **Taux de conversion global** | 4.3% | Reference : 14% - 18% dans le secteur |
| **CA total (FCFA)** | 3 548 407 865 FCFA | Prime collectée sur la période |
| **Prime moyenne / contrat** | 215 355 FCFA | Indicateur de valeur unitaire |
| **Prime moyenne / lead** | 9 311 FCFA | Efficacité économique brute |

**Lecture :** Le taux de conversion de 4.3% positionne le réseau en dessous de la norme sectorielle. Le principal levier d'amélioration est la qualification des leads / l'efficacité des conseillers juniors / le mix produit.

---

## 2. Performance par Canal : Le Funnel de Vente

| Canal | Leads | Taux de conversion | Valeur économique moyenne|
|-------|-------|-------------------|-----------------|
| Courtage | 4 | 25% | 54 809 |
| Agence Physique | 1074 | 14.2% | 227 132 |
| Télévente | 509 | 6.3% | 168735 |
| Digital/Web | 379 522 | 4.3% | 215 346 |

**Constats :**
- Le **Courtage** affiche le meilleur taux de conversion (25%), 2× supérieur à la moyenne mais ne représente que 0.001% du volume total de leads.
- Le **Digital** génère le plus grand volume (99.58% des leads) mais la conversion la plus faible (4.3%). Chaque lead digital a une valeur économique de 215 346 FCFA vs 54809 FCFA pour le Courtage.

**Recommandation #1 :** Mettre en place un processus de qualification des leads Digital (scoring à l'entrée, délai de contact < 2h) pour rapprocher leur conversion de celle de l'Agence Physique. Un gain de 10% sur taux de conversion du Digital représente environ 815861014 FCFA de CA additionnel.

---

## 3. Performance des Conseillers : Analyse Pareto

**Concentration :** 17 conseillers (42% du réseau) génèrent **80% du CA total**.

| Segment | Nb conseillers | Part du CA |
|---------|---------------|-----------|
| Top 20% (Senior) | 6 | 42.2% | 
| Mid 60% | 12 | 43.3% | 
| Bottom 20% (Junior) | 22 | 14% |

**📌 Constats :**
- Les **10 meilleurs conseillers** génèrent plus de CA que la moyenne.
- Les conseillers **Juniors** (< 299 jours d'ancienneté) génèrent une part du CA 3× inférieur aux Seniors.
- L'ancienneté est le **premier prédicteur de performance** identifié par le modèle ML.

**Recommandation #2 :** Mettre en place un programme de **mentorat structuré** (1 Senior pour 2 Juniors).

**Recommandation #3 :** Prioriser l'affectation des leads à **fort score ML** vers les Seniors pour maximiser la conversion en période de pic commercial.

---

## 4. Analyse Régionale

| Région | Leads | Taux conv. | Prime / lead (FCFA) | Signal |
|--------|-------|-----------|---------------------|--------|
| Abidjan | 1 008 | 8.2% | 18 186 | ✅ Forte valeur |
| Korhogo | 1 279 | 5.8% | 12 959 | 🟡 Volume fort, valeur moyenne |
| Zone rurale | 357,452 | 4.2% | 9,082 | 🔴 Sous-performant |

**📌 Constats :**
- Des écarts de **4 pts** de taux de conversion existent entre les meilleures et les moins bonnes régions.
- Abidjan présente la meilleure **prime par lead** (18 186 FCFA) avec un volume de leads faible : **potentiel inexploité**.

**→ Recommandation #4 :** Rééquilibrer l'allocation des ressources commerciales en faveur de Abidjan. Réduire le volume de leads Zone Rurale au profit de régions à plus forte valeur unitaire.

---

## 5. Analyse Produits

| Produit | Contrats | Part CA | Prime moy. | Signal |
|---------|----------|---------|-----------|--------|
| Mixte Senior | 2 731 | 31.6% | 410 684 FCFA | 💎 Forte valeur, sous-vendu |
| Mixte Vie & Épargne | 2 714 | 24.5% | 320 974 FCFA | 💎 Forte valeur |
| Épargne Retraite | 2 728 | 18.6% | 241 496 FCFA | ✅ Équilibré |
| Protection Décès | 2 755 | 4.7% | 59 974 FCFA | ⚠️ Fort volume, faible valeur |

**📌 Constats :**
- Les produits **Mixte** représentent 56.1% du CA mais seulement 33.1% du volume de contrats : ce sont les "cash cows" du portefeuille.
- La **Protection Famille** est le produit le plus vendu en volume mais contribue peu au CA (6.7% du CA pour 17.1% des contrats).

**→ Recommandation #5 :** Renforcer la formation commerciale sur les produits **Mixte Vie & Épargne** et **Mixte Senior**. Chaque contrat Mixte rapporte ~5× plus qu'un contrat Protection. Augmenter la part des Mixte de +5 pts de volume représente 124 083 054 FCFA supplémentaires.

---

## 6. Atteinte des Objectifs

| Niveau | Taux d'atteinte moyen | % conseillers ≥ 100% |
|--------|-----------------------|----------------------|
| Senior | 880% | 100% |
| Mid | 822% | 98% |
| Junior | 312% | 84% |

**📌 Constats :**
- 84% **Juniors** dépassent en moyenne  leur objectif, ce qui veut dire qu'on peut attendre beaucoup plus d'eux.


**→ Recommandation #6 :** Réviser la méthode de fixation des objectifs pour tout le monde. Utiliser le taux d'atteinte comme outil de dialogue, non de sanction.

---

## 7. Lead Scoring : Application ML

Le modèle de scoring (AUC-ROC = 0.761, vs 0.500 pour une prédiction aléatoire) permet de **prioriser les leads** avant contact :

| Segment | Lead Score | Taux de conv. réel | Action recommandée |
|---------|------------|-------------------|-------------------|
| 🔴 Fire | 75–100 | 14.8% | Contact immédiat, conseiller Senior |
| 🟠 Hot | 50–75 | 8.5% | Contact J+1, conseiller Mid/Senior |
| 🟡 Warm | 25–50 | 3.6% | Nurturing, contact J+3 |
| 🔵 Cold | 0–25 | 1.0% | Campagne automatisée |


---

## 8. Recommandations Prioritaires

### Court terme (0–3 mois)
1. **Mettre en place le lead scoring** en production → prioriser les segments Fire/Hot
2. **Qualifier les leads Digital** à l'entrée (formulaire enrichi + score automatique)
3. **Suivi mensuel Objectifs vs Réalisé** par conseiller et par région

### Moyen terme (3–12 mois)
4. **Programme de mentorat Junior** 
5. **Formation produits Mixte** pour les conseillers à fort volume / faible valeur
6. **Rééquilibrage territorial** des ressources vers les régions à forte prime par lead

---

*Analyse réalisée avec Python (pandas, scikit-learn). Données synthétiques basées sur hypothèses métier documentées. Reproduire les chiffres : exécuter `data_simulation_v2.py` puis les deux notebooks dans l'ordre.*
