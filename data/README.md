This folder contains raw and processed datasets used for sales performance reporting.
Data are simulated for demonstration purposes.

# Logique métier & règles importantes

Un contrat = transaction_type = 'new' et status = 'active' au moment du calcul.

Conversion rate (advisor) = # contrats new / # leads assigned (ou # leads contactés) dans la période. Préciser la source de leads.

CA / prime = somme premium_amount filtrée sur transaction_type IN ('new','renewal') et status='active'.

Annulations : si transaction_type='cancellation' et transaction_date dans la période, traiter en négatif (ou exclure selon l’indicateur). Décider d’une règle (ex : reporting net = GWP - cancellations).

Attribution lead → advisor : utiliser advisor_id dans leads ; si NULL, définir règle (unassigned / pool).

Objectifs : peuvent être mensuels/trimestriels ; joindre par niveau et période.

Période de calcul : habituellement mensuelle (mois calendaire), rolling 3 mois et year-to-date (YTD).