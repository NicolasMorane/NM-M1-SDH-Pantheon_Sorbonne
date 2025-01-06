# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 12:30:42 2024

@author: NMO
"""

import sqlite3

# Connexion à la base de données
conn = sqlite3.connect("BdeD_etape_1.db")
cursor = conn.cursor()

# 1 - Création des tables

# 1.1 - Création tb Parcelles
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Parcelles (
                Numero NUMERIC PRIMARY KEY,
                Analyse TEXT,
                Complement_numero TEXT,
                CF BOOLEAN,
                E BOOLEAN,
                I BOOLEAN,
                IND BOOLEAN,
                DB NUMERIC,
                Surface NUMERIC,
                Avoine NUMERIC,
                Seigle NUMERIC,
                Boeuf NUMERIC,
                Cheval NUMERIC,
                Fascines NUMERIC,
                Chevron NUMERIC,
                Latte NUMERIC,
                Piece1 NUMERIC,
                Piece2 NUMERIC,
                NatureID INTEGER,
                ProprietaireID INTEGER,
                MasID INTEGER,
                GriefID INTEGER,
                FOREIGN KEY (NatureID) REFERENCES Nature(ID),
                FOREIGN KEY (ProprietaireID) REFERENCES Proprietaires(ID),
                FOREIGN KEY (MasID) REFERENCES Mas(ID),
                FOREIGN KEY (GriefID) REFERENCES Griefs(ID)
            )
    """)

# 1-2 - Creation table Mas
cursor.execute("""
     CREATE TABLE IF NOT EXISTS Mas (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Mas TEXT UNIQUE
            )
     """)

# 1.3 - Creation table Statut_Proprietaire
cursor.execute("""
     CREATE TABLE IF NOT EXISTS Statut_Proprietaire (
         ID INTEGER PRIMARY KEY AUTOINCREMENT,
         Statut TEXT UNIQUE
         )
""")

# 1.4 - Creation table Proprietaires
cursor.execute("""
     CREATE TABLE IF NOT EXISTS Proprietaires (
         ID INTEGER PRIMARY KEY AUTOINCREMENT,
         Proprietaire TEXT,
         StatutID INTEGER,
         FOREIGN KEY (StatutID) REFERENCES Statut_Proprietaire(ID)
         )
""")

# 1.5 - Creation table Griefs
cursor.execute("""
     CREATE TABLE IF NOT EXISTS Griefs (
         ID INTEGER PRIMARY KEY AUTOINCREMENT,
         No_Grief TEXT,
         Grief TEXT,
         Probleme TEXT
         )
""")

# 1.6 - Creation table Type_Sol
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Type_Sol (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Occ_Sol TEXT UNIQUE
    )
""")
# 1.7 - Creation table Nature
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Nature (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nature TEXT UNIQUE,
        TypeSolID INTEGER,
        FOREIGN KEY (TypeSolID) REFERENCES Type_Sol(ID)
    )
""")

# Validation des changements
conn.commit()

# Fermeture de la connexion
conn.close()