import numpy as np
import pandas as pd


class Dating:
  def __init__(self, db=None):
    self.db = db

  def __check(self):
    return True

  def process_dict(self, dict_descriptor):
    if "collection" in dict_descriptor:
      temp = self.db[dict_descriptor["collection"]]
      if "data" in dict_descriptor:
        keys = list(set(["_id", *dict_descriptor["data"].keys()]))
        if "rightKey" in dict_descriptor:
          keys.append(dict_descriptor["rightKey"])
          new_df = pd.DataFrame(temp.find())[keys]
        for f in [f for f in dict_descriptor["data"].keys() if dict_descriptor["data"][f] is not None]:
          new_df = new_df[new_df[f] == dict_descriptor["data"][f]]
        return new_df, None
      return pd.DataFrame(temp.find()), None
    else:
      return None, "descriptor has no collection name"

  def process_list(self, list_descriptor):
    temp = list_descriptor.pop(0)
    (temp, err) = self.process_dict(temp)
    if err is not None:
      return temp, err
    for desc in list_descriptor:
      (join, err) = self.process_dict(desc)
      if err is not None:
        return join, err
      if "key" in desc:
        temp = pd.merge(temp, join, on=[desc["key"]], how="left")
      elif "leftKey" in desc and "rightKey" in desc:
        temp = pd.merge(temp, join, left_on=[desc["leftKey"]], right_on=[desc["rightKey"]], how="left")
      else:
        return None, "No key"
    return temp


  def process(self, data_descriptor):
    print(data_descriptor)
    if not self.__check():
      raise Exception("data error")

    if type(data_descriptor) == list and len(data_descriptor) > 1:
      print("type is list")
      return self.process_list(data_descriptor)

    elif type(data_descriptor) == dict:
      print("type is dict")
      return self.process_dict(data_descriptor)

    else:
      return None, "Wrong data_descriptor type"

  def apply_process(self, df):
    print("apply process")
    results = []
    for d in df["Précisions sur les datas à utiliser"]:
      if "{" in d and "}" in d:
        results.append(self.process(d))

    return results