from math import isnan
import pandas as pd
#all characters are unidcode in python3
#import unidecode as ud
import numpy as np
import re


class Cleaning:

    def __init__(self):
        self.link_towns_regions = "https://www.data.gouv.fr/fr/datasets/r/dbe8a621-a9c4-4bc3-9cae-be1699c5ff25"  
        self.df_nom_villes = pd.read_csv(self.link_towns_regions)[["libelle_acheminement","nom_commune_complet","nom_region"]]        
        self.df_nom_villes["nom_commune_complet"] = self.df_nom_villes["nom_commune_complet"].str.strip(" 1234567890")
        
        # TODO : on garde ou on dégage
        # self.methodes = {
        #     0: 'fillna',
        #     1: 'nettoyageCreatedAt',
        #     2: 'expertsVisibles',
        #     3: 'expertsDesinscrits'
        # }
        
        self.defaut_string = 'Inconnu'
        self.defaut_negatif_float = -1.0
        self.defaut_negatif_int = -1
          
        # liste colonne en format datetime
        self.liste_date = ['createdAt']
        # liste colonne en format float
        self.liste_nan_numeriques = ['hours_planned', 'daily_hourly.daily_prices',"daily_hourly_prices.daily_price_max",'percentage','note_communication','note_quality','note_level']
        # liste colonne en format str
        self.liste_nan_str = ['companyOrSchool', 'company.address', 'experienceTime','studyLevel', 'company.type','done','visible','isFake','temporarilyInvisible','sector']    
        # liste colonne contenant des ville
        self.liste_villes = ['company.address']
        # liste colonne des horaires
        self.liste_horaires = ['hours_planned']
        # liste colonne en format timestamp
        self.liste_timestamp = ['createdAt']
        # liste contenant des catégorie ages
        self.colonne_age_categories = 'experienceTime'
        # liste contenant des catégorie study
        self.colonne_study_categories = 'studyLevel'
    
    def __check(self):
        pass

    def process(self, df):
        #move columns and definitions in one single dict
        cleans = [{"name": "liste_date", "columns": ['createdAt'], "function": self.nettoyage_date},
        {"name": "liste_villes", "columns": ['company.address'], "function": self.nettoyage_villes},
          {"name": "liste_horaires", "columns": ['hours_planned'], "function": self.nettoyage_horaires},
          {"name": "liste_timestamp", "columns": ['createdAt'], "function": self.nettoyage_timestamp},
          {"name": "liste_nan_numeriques","columns":  ['hours_planned', 'daily_hourly.daily_prices',"daily_hourly_prices.daily_price_max",'percentage','note_communication','note_quality','note_level'], "function": self.fill_nan_num},
          {"name": "liste_nan_str", "columns": ['companyOrSchool', 'company.address', 'experienceTime','studyLevel', 'company.type','done','visible','isFake','temporarilyInvisible','sector'] , "function": self.fill_nan_str},
        ]

        #use regex to match columns because of columns aliasing in pd.merge...
        
        for clean in cleans:
            for colonne in clean["columns"]:
                a = re.compile(f"{colonne}")
                matches = list(filter(a.match, df.columns))
                for match_ in matches:
                    df = clean["function"](df, match_)
                if df is None:
                    break
                    #df[match_] = df[colonne].apply(clean["function"])

        a = re.compile(f"{self.colonne_age_categories}")
        matches = list(filter(a.match, df.columns))
        for match_ in matches:
            df[match_] = self.get_age_categories(df, match_)


        a = re.compile(f"{self.colonne_study_categories}")
        matches = list(filter(a.match, df.columns))
        for match_ in matches:
            df[match_] = self.get_study_levels(df, match_)

        """
        # changement de format de date
        for colonne in self.liste_date:
            if colonne in df.columns:
                df[colonne] = df[colonne].apply(self.nettoyage_date)

        # nettoyage ville
        for colonne in self.liste_villes:
            if colonne in df.columns:
                df[colonne] = df[colonne].apply(self.nettoyage_villes)

        # nettoyage horaires
        for colonne in self.liste_horaires:
            if colonne in df.columns:
                df[colonne] = df[colonne].apply(self.nettoyage_horaires)

        # nettoyage timestamp
        for colonne in self.liste_timestamp:
            if colonne in df.columns:
                df[colonne] = df[colonne].apply(self.nettoyage_timestamp)

        # nettoyage catégorie d'age
        if self.colonne_age_categories in df.columns:
            self.get_age_categories(df, self.colonne_age_categories)

        # nettoyage study levels
        if self.colonne_study_categories in df.columns:
            self.get_study_levels(df, self.colonne_study_categories)

        # fillna numériques
        for colonne in self.liste_nan_numeriques:
            if colonne in df.columns:
                df[colonne] = df[colonne].fillna(self.defaut_negatif_float, inplace=True)

        # fillna Inconnu
        for colonne in self.liste_nan_str:
            if colonne in df.columns:
                df[colonne] = df[colonne].fillna(self.defaut_string, inplace=True)"""
        return df, None


    def fill_nan_num(self, df, colonne):
          df[colonne].fillna(self.defaut_negatif_float, inplace=True)
          return df

    def fill_nan_str(self, df, colonne):
      df[colonne].fillna(self.defaut_string, inplace=True)
      return df    

    def create_flag(self, df, colonne):
        nom = f"dummy_value_{colonne}"
        df[nom] = df[colonne].apply(pd.isna)
        return df


    def nettoyage_date(self, df, colonne):
        df[colonne].apply(lambda chaine: '/'.join(str(int(x)) for x in chaine.split('/')) if '/' in chaine else chaine)
        #df[colonne].str.replace("\d{2}\/d{2}\/d{4}", r'\1', regex=True)
        def remove_n(df):
          if len(df[colonne]) < 3:
              df[colonne] = "01/12/2260"
              return df
          temp = df[colonne].split("/")
          df[colonne] = f"{temp[0][-2:]}/{temp[1][-2:]}/{temp[2][-4:]}"
          return df
        df.apply(remove_n, axis=1)
        df[colonne] = pd.to_datetime(df[colonne], format="%d/%m/%Y")
        return df
       

    def nettoyage_timestamp(self, df, colonne):
        df[colonne] = pd.to_datetime(df[colonne])
        return df
        

    def get_age_categories(self, df, colonne):
        df[colonne].replace(to_replace='mois de 10 ans', value='moins de 10 ans', inplace=True)
        df[colonne].replace(to_replace='+ de 30 ans', value='+ de 25 ans', inplace=True)
        df[colonne].replace(to_replace='moins de 10 ans', value=self.defaut_string, inplace=True)
        df[colonne].replace(to_replace='20 à 30 ans', value=self.defaut_string, inplace=True)
        df[colonne].replace(to_replace='10 à 20 ans', value=self.defaut_string, inplace=True)
        return df

    def get_study_levels(self, df, colonne):
        df[colonne].replace(to_replace='Bac +5', value='Bac5', inplace=True)
        df[colonne].replace(to_replace='Bac + 8', value='Bac8', inplace=True)
        df[colonne].replace(to_replace='Bac + 3', value='Bac3', inplace=True)
        df[colonne].replace(to_replace='Bac5', value='Bac+5', inplace=True)
        df[colonne].replace(to_replace='Bac4', value='Bac+4', inplace=True)
        df[colonne].replace(to_replace='Bac2', value='Bac+2', inplace=True)
        df[colonne].replace(to_replace='Bac3', value='Bac+3', inplace=True)
        df[colonne].replace(to_replace='Bac8', value='Bac+8', inplace=True)
        return df

    def is_a_dummy_value(self, val):
        try:
            float(val)
            return isnan(float(val))    
        except ValueError:
            return True
      
    def nettoyage_horaires(self, df, colonne):
        # hours_planned
        # nettoyage des erreurs redondantes
        df[colonne].replace(to_replace=",", value=".", inplace=True, regex=True)
        df[colonne].replace(to_replace=[" Heures", " heures"], value="", inplace=True, regex=True)

        mask_dummy_value = df[colonne].apply(self.is_a_dummy_value)
        df["dummy_value"] = df[colonne].apply(self.is_a_dummy_value)

        # Traitement NaN (on les met à 0 mais identifiées comme 'dummy_value'=True)
        df.fillna("0", inplace=True)

        # Traitement des autres valeurs erronées (on les met à 0 mais identifiées comme 'dummy_value'=True)
        df.loc[mask_dummy_value, colonne] = "0"

        # Formatage en float
        df[colonne] = df[colonne].astype('float')

        return df
    
    def nettoyage_villes(self, df, colonne):
        df[colonne].apply(self.get_town)
        return df
   

    def get_region(self, town):    
        '''This function takes a town name with accents and quotes. Output is the french region where this town is (ex: Nouvelle Aquitaine)'''
        if len(list(self.df_nom_villes[self.df_nom_villes["nom_commune_complet"] == town]["nom_region"])) > 0:
            return list(self.df_nom_villes[self.df_nom_villes["nom_commune_complet"] == town]["nom_region"])[0]
        else:
            return self.defaut_string

    def get_town(self, native_adress):
        '''This function takes an adress as input. Output is the name of the town in adress, with accents and quotes'''
        output_adress = ''
        if isinstance(native_adress, float):
            return self.defaut_string
        else:
            items_adress = native_adress.split(",")
            if np.nan == items_adress or len(items_adress) == 0:
                return self.defaut_string
            # pas de virgule : ville ou adresse complète sans virgules
            elif len(items_adress) == 1 and items_adress[0] != "":
                if len(items_adress[0].split(" ")) <= 2:
                    town = items_adress[0]
                    #output_adress = self.name_town_perfectly(town.strip(", ").upper()))
                    output_adress = self.name_town_perfectly(town.strip(", ").upper())
                else:
                    town = items_adress[0].split(" ")[-1]
                    output_adress = self.name_town_perfectly(town.strip(", ").upper())
            # virgules présentes et adresse finit par 'France'
            elif items_adress[-1].strip(", ").upper() == "FRANCE":
                adress = items_adress[-2]
                if len(adress.strip(" ").split(" ")) == 2: 
                    if adress.strip(" ").split(" ")[0].isnumeric():
                        output_adress = self.name_town_perfectly(adress.strip(" ").split(" ")[1].upper())
                    else:
                        output_adress = self.name_town_perfectly(adress.strip(", ").upper())
                if len(adress.split(" ")) > 2:
                    output_adress = self.name_town_perfectly(adress.split(" ")[-1].strip(", ").upper())
                else:
                    output_adress = self.name_town_perfectly(adress.strip(", ").upper())
            # virgules présentes mais pas de 'France'
            else:
                output_adress = self.name_town_perfectly(items_adress[-1].split(" ")[-1].upper())
        return output_adress
    
    def name_town_perfectly(self, town_upper):
        '''This function takes a town name in upper case as input. If this town is french, the function returns the name with accents and quotes'''
        mask = self.df_nom_villes["libelle_acheminement"] == town_upper
        if len(list(self.df_nom_villes[mask]["nom_commune_complet"])) == 0:
            return self.defaut_string
        else:
            return list(self.df_nom_villes[mask]["nom_commune_complet"])[0]
