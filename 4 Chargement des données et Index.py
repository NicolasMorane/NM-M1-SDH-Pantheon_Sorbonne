import sqlite3
import pandas as pd

# Connexion à la base de données
conn = sqlite3.connect("BdeD_etape_1.db")
cursor = conn.cursor()

##-------------------------------------------------------
# 2 - Chargement des Données et Index

# 2.1 - Chargement tb Nature et Type_Sol

# Chargement du fichier CSV dans un DataFrame
df = pd.read_csv("4_Type_Sol.csv")

# Insérer les données dans Type_Sol et Nature
for index, row in df.iterrows():
    # Insérer Occ_Sol dans Type_Sol
    cursor.execute("""
        INSERT OR IGNORE INTO Type_Sol (Occ_Sol)
        VALUES (?)
    """, (row['Occ_Sol'],))

    # Récupérer l'ID du Occ_Sol
    cursor.execute("""
        SELECT ID FROM Type_Sol WHERE Occ_Sol = ?
    """, (row['Occ_Sol'],))
    type_sol_id = cursor.fetchone()[0]

    # Insérer Nature avec la clé étrangère TypeSolID
    cursor.execute("""
        INSERT OR IGNORE INTO Nature (Nature, TypeSolID)
        VALUES (?, ?)
    """, (row['Nature'], type_sol_id))


# 2.2 - Chargement tb Mas
cursor.execute("""
        INSERT OR IGNORE INTO Mas (Mas)
            SELECT DISTINCT Mas FROM Beaufort_FICHIER_ATLAS_OK_V1  
    """)

# 2.3 - Chargement tb Griefs
cursor.execute("""
       INSERT OR IGNORE INTO Griefs (No_Grief, Grief, Probleme)
           SELECT DISTINCT No_Grief, Grief, Problemes
           FROM Beaufort_FICHIER_ATLAS_OK_V1
           WHERE No_Grief IS NOT NULL OR Grief IS NOT NULL OR Problemes IS NOT NULL;

    """)


# 2.4 - Chargement tb Statut_Proprietaire
cursor.execute("""
        INSERT OR IGNORE INTO Statut_Proprietaire (Statut)
            SELECT DISTINCT Statut
            FROM Beaufort_FICHIER_ATLAS_OK_V1
    """)
# 2.5 - Chargement tb Proprietaires
cursor.execute("""
        INSERT INTO Proprietaires (Proprietaire, StatutID)
        SELECT 
            bf.Proprietaires,
            (SELECT sp.ID FROM Statut_Proprietaire sp WHERE sp.Statut = bf.Statut)
        FROM Beaufort_FICHIER_ATLAS_OK_V1 bf
        WHERE bf.Statut IS NOT NULL AND EXISTS (
            SELECT 1 FROM Statut_Proprietaire sp WHERE sp.Statut = bf.Statut
   )
    """)

# 2.6 - Chargement tb Parcelles
cursor.execute("""
    INSERT INTO Parcelles (
                Numero, Analyse, Complement_numero, CF, E, I, IND, DB, Surface,
                Avoine, Seigle, Boeuf, Cheval, Fascines, Chevron, Latte, Piece1, Piece2,
                NatureID, ProprietaireID, MasID, GriefID
            )
            SELECT 
                bf.Numero,
                bf.Analyse,
                bf.Complement_numero,
                bf.CF,
                bf.E,
                bf.I,
                bf.IND,
                bf.DB,
                bf.Surface,
                bf.Avoine,
                bf.Seigle,
                bf.Boeuf,
                bf.Cheval,
                bf.Fascines,
                bf.Chevron,
                bf.Latte,
                bf.Piece1,
                bf.Piece2,
                (SELECT n.ID FROM Nature n WHERE n.Nature = bf.Nature),
                (SELECT p.ID FROM Proprietaires p WHERE p.Proprietaire = bf.Proprietaires AND EXISTS (
                    SELECT 1 FROM Statut_Proprietaire sp
                    WHERE sp.ID = p.StatutID AND sp.Statut = bf.Statut
                    )
                ),
                (SELECT m.ID FROM Mas m WHERE m.Mas = bf.Mas),
                (SELECT g.ID FROM Griefs g WHERE g.No_Grief = bf.No_Grief AND g.Grief = bf.Grief AND g.Probleme = bf.Problemes)
            FROM Beaufort_FICHIER_ATLAS_OK_V1 bf
""")


# Validation des changements
conn.commit()

# Fermeture de la connexion
conn.close()
