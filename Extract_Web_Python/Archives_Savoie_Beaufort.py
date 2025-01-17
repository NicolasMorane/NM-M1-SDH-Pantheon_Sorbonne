# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 09:58:14 2025

@author: NMO
"""



import requests
import time
from bs4 import BeautifulSoup
import pandas as pd

# URL de base
base_url = "https://recherche-archives.savoie.fr"

session = requests.Session()

start_url = base_url + "/?label_fulltext=Recherche+libre&form_search_fulltext=&form_op_fulltext=ET&label_geogname=Lieux&form_search_geogname=%22Beaufort+%28Savoie%2C+France%29%22+OU+&form_op_geogname=ET&label_v2_field_1408970854eVDFlm=Origine+%28producteur+%2F+versant%29&form_search_v2_field_1408970854eVDFlm=&form_op_v2_field_1408970854eVDFlm=ET&form_req_v2_field_1408970854eVDFlm=%7B%3Acorpname%7D__VAL_+OU+%7B%3Afamname%7D__VAL_+OU+%7B%3Afamname%7D__VAL_+OU+%7B%3Aorigination%7D__VAL_&form_search_unitdate1=1000&form_search_unitdate2=1790&label_unitdate=Date&label_unitdate_pref=entre&label_unitdate2=et&form_op_unitdate=ET&form_search_unitdate3=&form_search_unitdate=1000&label_dao=Documents+num%C3%A9ris%C3%A9s&label_unitid=Recherche+par+cote&form_search_unitid=&form_op_unitid=ET&display_thesaurus=autocomplete&action=search&id=recherche_guidee_inventaire_web"
#start_url_template = base_url + "/?id=recherche_guidee_inventaire_web&doc=&page={page}&page_ref="

#response = session.get(start_url)


# En-têtes HTTP pour imiter un navigateur
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


#Fonction qui extrait les données d'une page à partir de son contenu HTML. 
def extract_data_from_page(html_content):
   
    # Analyse le contenu du code source avec BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Cherche les éléments <li>
    list_items = soup.find_all('li')

    # Parcourir les éléments et extraire les infos
    print("Extraction des données")
    data = []
    for item in list_items:
        date_tag = item.find('div', class_='date')
        cote_tag = item.find('div', class_='cote')
        various_tag = item.find('a', class_='various')
        description_tag = item.find('div', class_='description')
        source_tag = item.find('div', class_='source')
        ariane_tags = item.find_all('a', class_='various link_ariane')

        date = f'"{date_tag.get_text(strip=True)}"' if date_tag else ""
        cote = f'"{cote_tag.get_text(strip=True)}"' if cote_tag else ""
        various = f'"{various_tag.get_text(strip=True)}"' if various_tag else ""
        description = f'"{description_tag.get_text(strip=True)}"' if description_tag else ""
        source = f'"{source_tag.get_text(strip=True)}"' if source_tag else ""
        ariane = f'"{" > ".join([ariane.get_text(strip=True) for ariane in ariane_tags])}"' if ariane_tags else ""

        # Ajouter les infos si elles existent
        if date or cote or various or description or source or ariane:
            data.append({
                "date": date,
                "cote": cote,
                "various": various,
                "description": description,
                "source": source,
                "ariane": ariane
            })
            
    return data


# Extraire les données de toutes les pages
all_data = []

# Traiter la première page
print("ouverture première page")
reponse_page1 = session.get(start_url)

 # Attendre 60 secondes entre le get et la réponse
time.sleep(40)

first_html_content = reponse_page1.text
page_data = extract_data_from_page(first_html_content)
all_data.extend(page_data)

# Traiter les pages suivantes
for page_number in range(2, 4):
    current_url = base_url + "?id=recherche_guidee_inventaire_web&doc=&page=" + str(page_number) + "&page_ref="
    response_current_page = session.get(current_url)
    print(f"Ouverture de la page : {current_url}")
 
    # Attendre 60 secondes entre chaque page
    print("Attente de 60 secondes pour attendre le retourd su serveur...")
    time.sleep(40)

    current_url_content = response_current_page.text
   
    page_data = extract_data_from_page(current_url_content)

    # Si pas d'info stop boucle
    if not page_data:
        print(f"Aucune donnée trouvée sur la page {page_number}. Stop boucle.")
        break

    # ajout des données de la page aux précédentes
    all_data.extend(page_data)

   

# Conversion de la liste en DataFrame puis CSV
print(f"Nombre total d'enregistrements extraits : {len(all_data)}")
df = pd.DataFrame(all_data)
df.to_csv('Extract_Archives_Beaufort.csv', index=False, encoding='utf-8', sep=';')
print("Les données ont été sauvegardées dans 'Extract_Archives_Beaufort.csv'")
