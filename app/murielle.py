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
    myclient.drop_database(os.environ["DB"])
    self.db = myclient[os.environ["DB"]]
    self.config_file = pd.read_csv(os.environ["configFile"])
    self.data = Dating(db=myclient[os.environ["DB"]])
    self.cleaning = Cleaning()
    self.engineering = Engineering()
    self.ploting = Plotting()

  def get_department(self):
    return self.config_file["department"].unique()

  def get_all_indicators_by_department(self, department_name):
    indicators_to_process = self.config_file.loc[self.config_file["department"] == department_name]
    indicators_to_process_list_dict = indicators_to_process.to_dict(orient="records")
    results = []
    for indicator_row in indicators_to_process_list_dict:
      data = json.loads(indicator_row["data"])
      #DATA PASS
      (df, err) = self.data.process(data)
      if err is None:
        return None, "Failed at data"

      #CLEANING PASS
      if self.cleaning is not None:
        #cleaning = json.loads(indicator_row["cleaning"])
        (df, err) = self.cleaning.process(df)
        if err is None:
          return None, "Failed at cleaning"

      #ENGINEERING PASS
      #CHECK IF REFRESH IS NEEEDED
      if self.engineering is not None:
        engineering = json.loads(indicator_row["engineering"])
        (df, df_cleaning, filters) = self.engineering.process(engineering, df)

      if err is None:
        return None, "Failed at engineering"

      #PLOTING
      if self.ploting is not None:
        ploting = json.loads(indicator_row["plotting"])
        (plot, err) = self.ploting.process(ploting, df)
        if err is None:
          return None, "Failed at ploting"
        results.append({"department": indicator_row["department"],"indicatorName": indicator_row["name"], "plot":  plot, "df_cleaned": df_cleaning, "ploting": ploting, "engineering": engineering})
    return results

  #in case engineering must be rerun
  def refresh(self, resfresh_dict):
    #refresh dict
    df = resfresh_dict["df_cleaned"]
    engineering_description = resfresh_dict["engineering"]
    ploting_description = resfresh_dict["ploting"]
    (df, err) = self.engineering.process(df, engineering_description, ploting_description["filters"])
    if err is not None:
      return None, "engineering failed"
    (plot, err) = self.ploting.process(df, ploting_description)
    if err is not None:
      return None, "ploting failed"
    resfresh_dict["plot"] = plot
    return resfresh_dict