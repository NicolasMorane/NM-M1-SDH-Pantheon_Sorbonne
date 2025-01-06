# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 16:57:49 2024

@author: NMO
"""

import sqlite3

# Création et connexion à la base de données
conn = sqlite3.connect("BdeD_etape_1.db")
cursor = conn.cursor()

# SQL1 Pracelles OK
cursor.execute("""
        UPDATE [Beaufort_FICHIER_ATLAS_OK_V1]
        SET Analyse = 'Parcelle ok'
        WHERE Beaufort_FICHIER_ATLAS_OK_V1.Numero In (
            SELECT Beaufort_FICHIER_ATLAS_OK_V1.Numero 
            FROM [Parcelles_theoriques] 
            INNER JOIN [Beaufort_FICHIER_ATLAS_OK_V1] 
            ON Parcelles_theoriques.Parcelle_no = [Beaufort_FICHIER_ATLAS_OK_V1].Numero
            )
""")

# SQL2 Parcelles non reférencées
cursor.execute("""
        INSERT INTO Beaufort_FICHIER_ATLAS_OK_V1 (Numero, Analyse)
        SELECT p.Parcelle_no, 'Parcelle non référencée'
        FROM Parcelles_theoriques p
        WHERE p.Parcelle_no NOT IN (
            SELECT b.Numero
            FROM Beaufort_FICHIER_ATLAS_OK_V1 b
        )
""")

# SQL3 Parcelles décimales
cursor.execute("""
        UPDATE Beaufort_FICHIER_ATLAS_OK_V1
        SET Analyse = 'Parcelle décimale'
        WHERE Numero LIKE '%.%'
        AND CAST(Numero AS FLOAT) != CAST(Numero AS INTEGER)
""")

# SQL4 Parcelles avec même numéros
cursor.execute("""
        WITH Doublons AS (
            SELECT 
                Numero
            FROM Beaufort_FICHIER_ATLAS_OK_V1
            GROUP BY Numero
            HAVING COUNT(*) > 1
        )
        UPDATE Beaufort_FICHIER_ATLAS_OK_V1
        SET Analyse = 'Doublon'
        WHERE Numero IN (SELECT Numero FROM Doublons)

""")

# SQL5 identification premier Doublon Doublon1 et les autres Doublon2
cursor.execute("""
        WITH DoublonsClassement AS (
            SELECT 
                ROWID AS OriginalRowID, -- Garde une référence pour la mise à jour
                Numero,
                ROW_NUMBER() OVER (PARTITION BY Numero ORDER BY ROWID) AS RangDoublon
        FROM Beaufort_FICHIER_ATLAS_OK_V1
        WHERE Analyse = 'Doublon'
        )
        UPDATE Beaufort_FICHIER_ATLAS_OK_V1
        SET Analyse = CASE
            WHEN (SELECT RangDoublon FROM DoublonsClassement d WHERE d.OriginalRowID = Beaufort_FICHIER_ATLAS_OK_V1.ROWID) = 1 THEN 'Doublon1'
            ELSE 'Doublon2'
        END
        WHERE ROWID IN (SELECT OriginalRowID FROM DoublonsClassement)
""")

# SQL6 Doublon + Décimal
cursor.execute("""
        UPDATE Beaufort_FICHIER_ATLAS_OK_V1
        SET Analyse = Analyse || ' Parc Dec'
        WHERE Analyse IN ('Doublon1', 'Doublon2')
            AND Numero LIKE '%.%'
            AND CAST(Numero AS FLOAT) != CAST(Numero AS INTEGER)
""")

# SQL7 la Parcelle sans numéro (no = 0)
cursor.execute("""
        UPDATE Beaufort_FICHIER_ATLAS_OK_V1
        SET Analyse = 'Parcelle non numérotée'
        WHERE Numero = 0

""")

# SQL8.1 alteration no parcelle pour doublon1
cursor.execute("""
        UPDATE Beaufort_FICHIER_ATLAS_OK_V1
        SET Numero = Numero + 0.01
        WHERE Analyse LIKE 'Doublon1%'
""")
# SQL8.1 alteration no parcelle pour doublon2
cursor.execute("""
        UPDATE Beaufort_FICHIER_ATLAS_OK_V1
        SET Numero = Numero + 0.02
        WHERE Analyse LIKE 'Doublon2%'
""")
# SQL9 Minuscules pour Mas et Nature
cursor.execute("""
        UPDATE Beaufort_FICHIER_ATLAS_OK_V1
        SET Mas = LOWER(Mas),
            Nature = LOWER(Nature)
""")

# Validation des changements
conn.commit()

print("traitements SQL effectués avec succès.")



# Fermeture de la connexion
if conn:
   conn.close()