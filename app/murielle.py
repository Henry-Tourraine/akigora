import pymongo
import os
import pandas as pd
import json
from app.components.dating import Dating
from app.components.cleaning import Cleaning
from app.components.engineering import Engineering
from app.components.ploting import Plotting

class MurielleController:
  def __init__(self):
    myclient = pymongo.MongoClient(os.environ["MONGODB"])
    self.db = myclient[os.environ["DB"]]
    self.config_file = pd.read_csv(os.environ["CONFIG"])
    self.data = Dating(db=myclient[os.environ["DB"]])
    self.cleaning = Cleaning()
    self.engineering = Engineering
    self.ploting = Plotting()

  def get_departments(self):
    return self.config_file["department"].unique()

  def get_all_indicators_by_department(self, department_name):
    indicators_to_process = self.config_file.loc[self.config_file["department"] == department_name]
    indicators_to_process_list_dict = indicators_to_process.to_dict(orient="records")
    results = []
    for indicator_row in indicators_to_process_list_dict:
      print("---------------------------------------------------------------------------------------------->")
      print(f'departement : {indicator_row["department"]}')
      print(f'indicateur : {indicator_row["name"]}')
      print("---------------------------------------------------------------------------------------------->")
      print("data")
      data = json.loads(indicator_row["data"])
      #DATA PASS
      (df, err) = self.data.process(data)
      if err is not None:
        return None, f"Failed at data : {err}"
      print("df_data :")
      print(df)
      print("---------------------------------------------------------------------------------------------->")
      print("cleaning")
      #CLEANING PASS
      if self.cleaning is not None:
        #cleaning = json.loads(indicator_row["cleaning"])
        (df, err) = self.cleaning.process(df)
        if err is not None:
          return None, f"Failed at cleaning : {err}"
      print(type(df))
      print(df)

      print("---------------------------------------------------------------------------------------------->")
      print("engineering")
      #ENGINEERING PASS
      #CHECK IF REFRESH IS NEEEDED
      if self.engineering is not None:
        engineering = json.loads(indicator_row["engineering"])
        (df, df_cleaning, filters) = self.engineering.process(engineering, df)

      if err is not None:
        return None, f"Failed at engineering : {err}"

      print("---------------------------------------------------------------------------------------------->")
      print("plotting")
      #PLOTING
      if self.ploting is not None:
        ploting = json.loads(indicator_row["plotting"])
        (plot, err) = self.ploting.process(ploting, df)
        if err is not None:
          return None, f"Failed at ploting : {err}"
        results.append({"department": indicator_row["department"],"indicatorName": indicator_row["name"], "plot":  plot, "df_cleaned": df_cleaning, "ploting": ploting, "engineering": engineering})
    return results


  def render_one_indicator(self, indicator_row):
    print("---------------------------------------------------------------------------------------------->")
    print(f'departement : {indicator_row["department"]}')
    print(f'indicateur : {indicator_row["name"]}')
    print("---------------------------------------------------------------------------------------------->")
    print("data")
    data = json.loads(indicator_row["data"])
    #DATA PASS
    (df, err) = self.data.process(data)
    if err is not None:
      return None, f"Failed at data : {err}"
    print("df_data :")
    print(df)
    print("---------------------------------------------------------------------------------------------->")
    print("cleaning")
    #CLEANING PASS
    if self.cleaning is not None:
      #cleaning = json.loads(indicator_row["cleaning"])
      (df, err) = self.cleaning.process(df)
      if err is not None:
        return None, f"Failed at cleaning : {err}"
    print(type(df))
    print(df)

    print("---------------------------------------------------------------------------------------------->")
    print("engineering")
    #ENGINEERING PASS
    #CHECK IF REFRESH IS NEEEDED
    if self.engineering is not None:
      engineering = json.loads(indicator_row["engineering"])
      (df, df_cleaning, filters) = self.engineering.process(engineering, df)

    if err is not None:
      return None, f"Failed at engineering : {err}"

    print("---------------------------------------------------------------------------------------------->")
    print("plotting")
    #PLOTING
    if self.ploting is not None:
      ploting = json.loads(indicator_row["plotting"])
      (plot, err) = self.ploting.process(ploting, df)
      if err is not None:
        return None, f"Failed at ploting : {err}"
      return {"department": indicator_row["department"],"indicatorName": indicator_row["name"], "plot":  plot, "df_cleaned": df_cleaning, "ploting": ploting, "engineering": engineering}
  
  #in case engineering must be rerun
  def refresh(self, resfresh_dict):
    #refresh dict
    df = resfresh_dict["df_cleaned"]
    engineering_description = resfresh_dict["engineering"]
    ploting_description = resfresh_dict["ploting"]

    (df, err) = self.engineering.process(engineering_description, df, ploting_description["filters"])
    if err is not None:
      return None, "engineering failed"
    (plot, err) = self.ploting.process(ploting_description, df)
    if err is not None:
      return None, "ploting failed"
    resfresh_dict["plot"] = plot
    return resfresh_dict