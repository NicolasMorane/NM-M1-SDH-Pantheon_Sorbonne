# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 13:50:59 2024

@author: NMO
"""

import sqlite3

# Connexion à la base de données
conn = sqlite3.connect("BdeD_etape_1.db")
cursor = conn.cursor()

try:
    # Suppression des tables
    cursor.execute("DROP TABLE IF EXISTS Parcelles")
    cursor.execute("DROP TABLE IF EXISTS Griefs")
    cursor.execute("DROP TABLE IF EXISTS Mas")
    cursor.execute("DROP TABLE IF EXISTS Nature")
    cursor.execute("DROP TABLE IF EXISTS Proprietaires")
    cursor.execute("DROP TABLE IF EXISTS Statut_Proprietaire")
    cursor.execute("DROP TABLE IF EXISTS Type_Sol")
    
    # Validation des modifications
    conn.commit()
    print("Tables supprimées avec succès.")

except sqlite3.Error as e:
    print(f"Erreur lors de la suppression des Tables : {e}")

finally:
    # Fermeture de la connexion
    conn.close()
