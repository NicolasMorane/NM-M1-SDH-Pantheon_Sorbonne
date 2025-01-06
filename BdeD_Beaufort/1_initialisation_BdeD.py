# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 11:20:38 2024

@author: NMO
"""
import sqlite3
import pandas as pd

try:
    # Création et connexion à la base de données
    conn = sqlite3.connect("BdeD_etape_1.db")
    cursor = conn.cursor()

    # Création de la table "Beaufort_FICHIER_ATLAS_OK_V1"
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS "Beaufort_FICHIER_ATLAS_OK_V1" (
        "Analyse" TEXT,
        "Numero" NUMERIC,
        "Complement_numero" TEXT,
        "CF" TEXT,
        "E" TEXT,
        "I" TEXT,
        "Proprietaires" TEXT,
        "Statut" TEXT,
        "IND" TEXT,
        "Mas" TEXT,
        "Nature" TEXT,
        "DB" INTEGER,
        "Surface" INTEGER,
        "Avoine" TEXT,
        "Seigle" TEXT,
        "Boeuf" TEXT,
        "Cheval" TEXT,
        "Fascines" TEXT,
        "Chevron" TEXT,
        "Latte" TEXT,
        "Piece1" TEXT,
        "Piece2" TEXT,
        "No_Grief" TEXT,
        "Grief" TEXT,
        "Problemes" TEXT
    )
    """)

    # Chargement des données à partir du fichier CSV
    df = pd.read_csv("Beaufort_FICHIER_ATLAS_OK_V1.csv" , sep=';')

    # Gestion des valeurs nulles
    df = df.where(pd.notnull(df), None)

    # Insertion des données dans la table Beaufort_FICHIER_ATLAS_OK_V1
    df.to_sql('Beaufort_FICHIER_ATLAS_OK_V1', conn, if_exists='append', index=False)


# Créer une série avec les valeurs de 1 à 100
    valeurs = range(1, 17692)

# Créer un DataFrame avec une seule colonne
    df2 = pd.DataFrame(valeurs, columns=['Parcelle_no'])

# Création de la table Parcelle
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Parcelles_theoriques (
            Parcelle_no INTEGER
            )
        """)

# Insertion des valeurs dans la table Parcelle
    df2.to_sql('Parcelles_theoriques', conn, if_exists='append', index=False)
  
# Validation des changements
    conn.commit()

    print("Données insérées avec succès.")



finally:
    # Fermeture de la connexion
    if conn:
        conn.close()
