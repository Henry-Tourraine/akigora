import json
import pandas as pd
import numpy as np


class Operations:
  # comparateur pour préciser si on a un type inf a value ou sup
    def filtre(df, colonnes):
      comparateur = {"inf": lambda name, types: lambda x : x[name] < types, "sup": lambda name, types: lambda x : x[name] > types }
      if colonnes is None and len(colonnes)<1 :
        return df
      else:
        for colonne in colonnes:
          if colonne["type"] is not None:
            if "comparateur" in colonne:
              df = df.loc[comparateur[colonne["comparateur"]](colonne["name"], colonne["type"])]
              return df
            print("filtre")
            df = df.loc[df[colonne["name"]] == colonne["type"]]
        return df[[colonne["name"] for colonne in colonnes]]

# ici on implémente nos méthodes de calcul
    def longueur(df, colonne, result=None, value=None):
        df = Operations.filtre(df, colonne)
        length = len(df)
        return length

    def somme(df, colonne, result=None, value=None):
        df = Operations.filtre(df, colonne)
        return sum(df)

    def moyenne(df, colonne, result=None, value=None):
        df = Operations.filtre(df, colonne)
        return df.mean() if result is None else result.mean()

    def moyenne_buffer(buffer=[]):
        return buffer[-1].mean() if len(buffer)>0 else 'buffer not good'

    def contient(df, colonne, valeur):
        print('fonction == contient')
        return df[colonne].str.contains(str(valeur)).any()

    def unique(df, colonne):
        return df[colonne].unique()

    def value_counts(df, colonne, result=None):
        print(f"value count {colonne[0]['name']}")
        return df[colonne[0]["name"]].value_counts()

    def div(df, colonne, result=None, value=None):
        value_to_use = value if value is not None else 'pas de value'
        return result / value_to_use if result is not None else 'pas de result'

    def div_buffer(buffer=[], value=None):
        if value is not None and len(buffer) > 0:
          return buffer[-1] / value
        elif len(buffer) > 1:
          return buffer[-2]/buffer[-1]
        else:
          return 'erreur de buffer'


    def add(df, colonne, result=None, value=None):
      df = Operations.filtre(df, colonne)
      if value is not None:
        df["value"] = value
      values_to_use = df.sum(axis = 1) if colonne is not None else "colonne pas bon"
      return pd.Series(values_to_use)

    def mul(df, colonne, result=None, value=None):
      values_to_use = df[list(colonne)[0]] * df[list(colonne)[1]] if value is None else value
      return pd.Series(values_to_use)

    def mul_buffer(buffer=[], value=None):
        value_to_use = value if value is not None else "pas de value"
        return buffer[-1] * value_to_use if buffer is not None else "not enough in buffer"
    
    def group_by(df, joinColumns, columns, operation):
      columns = [i["name"] for i in columns]
      if operation == "sum":
         temp = df.groupby(joinColumns, as_index=False)[columns].sum()
         return temp[joinColumns], temp[columns]
      elif operation == "mean":
        temp = df.groupby(joinColumns, as_index=False)[columns].mean()
        return temp[joinColumns], temp[columns]
      elif operation == "min":
        temp = df.groupby(joinColumns, as_index=False)[columns].min()
        return temp[joinColumns], temp[columns]
      elif operation == "max":
        temp = df.groupby(joinColumns, as_index=False)[columns].max()
        return temp[joinColumns], temp[columns]
      elif operation == "count":
          print("groupy count")
          temp = df.groupby(joinColumns, as_index=False)[columns].count()
          print(temp)
          #return temp[[*joinColumns, *columns]]
          return temp[joinColumns], temp[columns]
      else:
          return np.NaN, np.NaN

    operations = {
        "longueur": longueur,
        "somme": somme,
        "moyenne": moyenne,
        "contient": contient,
        "unique": unique,
        "value_counts": value_counts,
        "div": div,
        "add": add,
        "mul" : mul,
        "div_buffer" : div_buffer,
        "mul_buffer" : mul_buffer,
        "moyenne_buffer": moyenne_buffer,
        "group_by": group_by
    }


class Engineering:
# filters sera pour gerer les filtre pour les plot
    def apply_filter(df, list_filtre):
      for lf in list_filtre:
        if lf["name"]=="select":
          df = df.loc[df[lf.colonne] == lf.values[lf.selected]]
        elif lf["name"]=="slider":
          df = df.loc[(df[lf.colonne] >= lf.range[0]) & (df[lf.colonne] <= lf.range[1]) ]
        else:
          return "erreur de filters"
      return df

# on check que les colonne indiquer dans le dictionnaire sont bien présent dans le df
    def check(df, engineer_description):
        if not all(c['name'] in df.columns for c in engineer_description):
            return None, "One or more specified columns do not exist in the DataFrame"
        return True
    
# process va venir effectuer les calcul et faire autant de tour nécessaire si plusieurs calculs à faire
    def process(engineer_descriptions, df, filters=[]):#filters for interactivity
        df_cleaning = df.copy()
        df = Engineering.apply_filter(df, filters)
        buffer = []
        for description in engineer_descriptions:
            operation = description["operation"]
            colonnes = description["colonnes"]

            #On va boucler sur le nombre d'opérations présentes dans chaque description
            result = None

            print(operation['fonction'])
            #work on buffer
            if len(colonnes) > 0 and colonnes[0]["name"] == "result":
              # handling for div_buffer
              if operation['fonction'] == 'div':
                  print(f' buffer lenght :{len(buffer)}')
                  result = Operations.div_buffer(buffer=buffer, value=operation.get('value'))
                  print(f"print 1: {result}")
                  buffer.append(result)
                  print(f"print 2: {buffer}")

              elif operation['fonction'] == 'moyenne':
                  print(f' buffer lenght :{len(buffer)}')
                  result = Operations.moyenne_buffer(buffer=buffer)
                  print(f"print 1: {result}")
                  buffer.append(result)
                  print(f"print 2: {buffer}")

              # handling for mul_buffer
              elif operation['fonction'] == 'mul':
                  print(f' buffer lenght :{len(buffer)}')
                  result = Operations.mul_buffer(buffer=buffer, value=operation.get('value'))
                  buffer.append(result)


            # penser a implementer la logique de contient
            if operation['fonction'] == 'contient':
                print('fonction == contient')
            elif operation['fonction'] == 'add' or operation['fonction'] == 'div' or operation['fonction'] == 'mul':
                print(colonnes)
                col_list = colonnes
                for col in col_list:
                    if not pd.api.types.is_numeric_dtype(df[col["name"]]):
                        raise ValueError(f"Column '{col}' is not numeric")

                # Modification du code pour passer le paramètre 'value' pour l'opération 'div'
                result = Operations.operations[operation['fonction']](df, col_list, result=result, value=operation.get('value'))
                print(f"print 1: {result}")
                buffer.append(result)
                print(f"print 2: {buffer}")
            # handling for group_by
            elif operation['fonction'] == 'group_by':
              print("groupby result")
              print(operation.get("aggfunc"))
              result = Operations.group_by(df, operation.get("groupColumns"), colonnes, operation.get("aggfunc"))
              print(result)
              buffer.append(result[0])
              buffer.append(result[1])

            else:
                result = Operations.operations[operation['fonction']](df, colonnes, result=result)
                print(f"print 3: {result}")
                buffer.append(result)
                print(f"print 4: {buffer}")



        return buffer, df_cleaning, filters
