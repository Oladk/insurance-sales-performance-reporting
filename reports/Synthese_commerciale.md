# SYNTHÈSE MANAGEMENT - PERFORMANCE COMMERCIALE
## Réseau de Vente Assurance Vie | Afrique de l'Ouest

---

> **Usage :** Ce document est la synthèse exécutive destinée au management. Il repose sur l'analyse complète réalisée dans `01_sales_performance_eda.ipynb`.

---

## 1. Vue d'ensemble — Chiffres Clés

| KPI | Valeur | Commentaire |
|-----|--------|-------------|
| **Leads générés** | 381,109 | Périmètre total de l'analyse |
| **Contrats souscrits** | 16,477 | Leads effectivement convertis |
| **Taux de conversion global** | 4.3% | Reference : 14% - 18% dans le secteur |
| **CA total (FCFA)** | 3,548,407,865 FCFA | Prime collectée sur la période |
| **Prime moyenne / contrat** | 215,355 FCFA | Indicateur de valeur unitaire |
| **Prime moyenne / lead** | 9,311 FCFA | Efficacité économique brute |

**Lecture :** Le taux de conversion de 4.3% positionne le réseau en dessous de la norme sectorielle. Le principal levier d'amélioration est la qualification des leads / l'efficacité des conseillers juniors / le mix produit.

---

## 2. Performance par Canal — Le Funnel de Vente

| Canal | Leads | Taux de conversion | Valeur économique moyenne|
|-------|-------|-------------------|-----------------|
| Courtage | 4 | 25% | 54809 |
| Agence Physique | 1074 | 14.2% | 227132 |
| Télévente | 509 | 6.3% | 168735 |
| Digital/Web | 379522 | 4.3% | 215346 |

**Constats :**
- Le **Courtage** affiche le meilleur taux de conversion (25%), 2× supérieur à la moyenne mais ne représente que 0.001% du volume total de leads.
- Le **Digital** génère le plus grand volume (99.58% des leads) mais la conversion la plus faible (4.3%). Chaque lead digital a une valeur économique de 215346 FCFA vs 54809 FCFA pour le Courtage.

**Recommandation #1 :** Mettre en place un processus de qualification des leads Digital (scoring à l'entrée, délai de contact < 2h) pour rapprocher leur conversion de celle de l'Agence Physique. Un gain de 10% sur taux de conversion du Digital représente environ 815861014 FCFA de CA additionnel.

---

## 3. Performance des Conseillers — Analyse Pareto

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
| [Région 1] | [X XXX] | [XX]% | [XX XXX] | ✅ Forte valeur |
| [Région 2] | [XX XXX] | [XX]% | [XX XXX] | 🟡 Volume fort, valeur moyenne |
| [Région 3] | [X XXX] | [XX]% | [X XXX] | 🔴 Sous-performant |

**📌 Constats :**
- Des écarts de **[XX] pts** de taux de conversion existent entre les meilleures et les moins bonnes régions.
- [Région X] présente la meilleure **prime par lead** ([XX XXX] FCFA) avec un volume de leads modéré → **potentiel inexploité**.
- La Zone Rurale concentre [XX]% des leads mais génère seulement [X]% du CA.

**→ Recommandation #4 :** Rééquilibrer l'allocation des ressources commerciales en faveur de [Région X]. Réduire le volume de leads Zone Rurale au profit de régions à plus forte valeur unitaire.

---

## 5. Analyse Produits

| Produit | Contrats | Part CA | Prime moy. | Signal |
|---------|----------|---------|-----------|--------|
| Mixte Senior | [XXX] | [XX]% | [XXX XXX] FCFA | 💎 Forte valeur, sous-vendu |
| Mixte Vie & Épargne | [XXX] | [XX]% | [XXX XXX] FCFA | 💎 Forte valeur |
| Épargne Retraite | [X XXX] | [XX]% | [XXX XXX] FCFA | ✅ Équilibré |
| Protection Décès | [X XXX] | [X]% | [XX XXX] FCFA | ⚠️ Fort volume, faible valeur |

**📌 Constats :**
- Les produits **Mixte** représentent [XX]% du CA mais seulement [X]% du volume de contrats → ce sont les "cash cows" du portefeuille.
- La **Protection Décès** est le produit le plus vendu en volume mais contribue peu au CA ([X]% du CA pour [XX]% des contrats).

**→ Recommandation #5 :** Renforcer la formation commerciale sur les produits **Mixte Vie & Épargne** et **Mixte Senior**. Chaque contrat Mixte rapporte [X]× plus qu'un contrat Protection. Augmenter la part des Mixte de +5 pts de volume représente [XX XXX XXX] FCFA supplémentaires.

---

## 6. Atteinte des Objectifs

| Niveau | Taux d'atteinte moyen | % conseillers ≥ 100% |
|--------|-----------------------|----------------------|
| Senior | [XXX]% | [XX]% |
| Mid | [XX]% | [XX]% |
| Junior | [XX]% | [X]% |

**📌 Constats :**
- Les **Juniors** atteignent en moyenne [XX]% de leur objectif — un décrochage structurel, pas conjoncturel.
- Certains mois présentent un décrochage systématique ([mois X, Y]) → possible saisonnalité à anticiper.

**→ Recommandation #6 :** Réviser la méthode de fixation des objectifs pour les Juniors (progression par palier sur les 12 premiers mois). Utiliser le taux d'atteinte comme outil de dialogue, non de sanction.

---

## 7. Lead Scoring — Application ML

Le modèle de scoring (AUC-ROC = [X.XXX], vs 0.500 pour une prédiction aléatoire) permet de **prioriser les leads** avant contact :

| Segment | Lead Score | Taux de conv. réel | Action recommandée |
|---------|------------|-------------------|-------------------|
| 🔴 Fire | 75–100 | [XX]% | Contact immédiat, conseiller Senior |
| 🟠 Hot | 50–75 | [XX]% | Contact J+1, conseiller Mid/Senior |
| 🟡 Warm | 25–50 | [XX]% | Nurturing, contact J+3 |
| 🔵 Cold | 0–25 | [X]% | Campagne automatisée |

**Impact estimé :** En concentrant 60% des efforts commerciaux sur les segments Fire + Hot ([XX]% des leads), on capture [XX]% des conversions potentielles.

---

## 8. Recommandations Prioritaires

### Court terme (0–3 mois)
1. **Mettre en place le lead scoring** en production → prioriser les segments Fire/Hot
2. **Qualifier les leads Digital** à l'entrée (formulaire enrichi + score automatique)
3. **Suivi mensuel Objectifs vs Réalisé** par conseiller et par région

### Moyen terme (3–12 mois)
4. **Programme de mentorat Junior** (cible : +[XX] pts de conversion)
5. **Formation produits Mixte** pour les conseillers à fort volume / faible valeur
6. **Rééquilibrage territorial** des ressources vers les régions à forte prime par lead

### Impact financier estimé
Cumulé sur 12 mois, les recommandations #1, #2 et #5 représentent un potentiel de **+[XX]% de CA** sans augmentation du volume de leads.

---

*Analyse réalisée avec Python (pandas, scikit-learn). Données synthétiques basées sur hypothèses métier documentées. Reproduire les chiffres : exécuter `data_simulation.py` puis les deux notebooks dans l'ordre.*
