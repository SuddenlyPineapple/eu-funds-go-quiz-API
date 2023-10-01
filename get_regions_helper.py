import json

import pandas as pd
def custom_replace(text):
    if text == "Cały Kraj":
        return text
    elif pd.isna(text):
        return "Nie zdefiniowano"
    else:
        return text
def get_regions_helper(df):
    # Kopiowanie DataFrame do nowego obiektu
    df_copy = df.copy()

    # Rozdzielanie kolumny na nowe wiersze
    df_copy['Miejscerealizacjiprojektu/Projectlocation'] = df_copy[
        'Miejscerealizacjiprojektu/Projectlocation'].str.split('|')
    df_copy = df_copy.explode('Miejscerealizacjiprojektu/Projectlocation')

    # Rozdzielanie kolumny na nowe wiersze
    df_copy['Miejscerealizacjiprojektu/Projectlocation'] = df_copy['Miejscerealizacjiprojektu/Projectlocation'].apply(lambda x: custom_replace(x.strip()))

    # Wyodrębnienie województw
    df_copy['Wojewodztwo'] = df_copy['Miejscerealizacjiprojektu/Projectlocation'].str.extract(r'WOJ\.: ([^\d,]+)')
    df_copy['Wojewodztwo'] = df_copy['Wojewodztwo'].str.capitalize()

    df_copy['Wojewodztwo'] = df_copy['Wojewodztwo'].fillna(df_copy['Miejscerealizacjiprojektu/Projectlocation'])

    # Wyodrębnienie listy powiatów dla każdego województwa
    df_copy['Powiat'] = df_copy['Miejscerealizacjiprojektu/Projectlocation'].str.extract(r'POW\.: (.*)')
    df_copy['Powiat'] = df_copy['Powiat'].str.capitalize()

    # Usunięcie duplikatów
    df_copy = df_copy.drop_duplicates().reset_index(drop=True)

    # Wyświetlenie nowego DataFrame z województwami i listą powiatów
    # print(df_copy)

    df_copy = df_copy.dropna(subset=['Powiat'])
    df_copy = df_copy.drop_duplicates(subset=['Wojewodztwo', 'Powiat'])
    # Grupowanie danych według województwa i agregacja powiatów do listy
    grouped = df_copy.groupby('Wojewodztwo')['Powiat'].apply(list).reset_index()

    # Przekształcenie DataFrame na listę słowników w formacie JSON
    result = []
    for _, row in grouped.iterrows():
        wojewodztwo = row['Wojewodztwo']
        powiaty = row['Powiat']
        if not powiaty:
            powiaty = ["Brak przypisanego powiatu"]
        result.append({'name': wojewodztwo, 'items': powiaty})

    # Dodanie "Cały Kraj" do wynikowej listy, jeśli nie istnieje w danych
    if not any(entry['name'] == 'Cały Kraj' for entry in result):
        result.append({'name': 'Cały Kraj', 'items': []})

    return result
