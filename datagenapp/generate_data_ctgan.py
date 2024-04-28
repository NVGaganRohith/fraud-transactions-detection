from sdv.single_table import CTGANSynthesizer
import numpy as np
from sdv.sampling import Condition
import pandas as pd
from datetime import datetime


def synthetic_data_gen(no_of_records=100,type="Both",percentage="50%"):
    """
    synthetic_data_gen used to generate the synthatic data

    parameters:
    no_of_records: int , minimum value is 1
                   no_of_records will tell to the model how many records need to be generated
    type:str ["Fraud","No Fraud","Both"]
              type is tell to model what type of data need to be generated
    Percentage:str  tell to the model how mch fruad data  need to be generated .

    """
    type_list=[]
    if type == "Fraud":
        type_list = [1 for _ in range(no_of_records)]
    elif type == "No Fraud":
        type_list = [0 for _ in range(no_of_records)]
    else :
        prob_of_1 = int(percentage[:-1])/100
        type_list = np.random.choice([0,1],size=no_of_records,p=[1-prob_of_1,prob_of_1])
    conditions = pd.DataFrame({'Label': type_list})
    synthesizer = CTGANSynthesizer.load('my_ctgan_model.pkl')
    synthetic_data = synthesizer.sample_remaining_columns(conditions)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    synthetic_data["Time_step"] = dt_string
    synthetic_data["Transaction_Id"]= (synthetic_data["Time_step"].str.replace(" ","_").str.replace("-","_").str.replace(":","_") + "_" + synthetic_data["Transaction_Id"].str.replace(" ","_").str.replace("-","_").str.replace(":","_"))

    return synthetic_data


def synthetic_data_gen_sample(no_of_records=100,type="Both",percentage="50%"):
    type_list=[]
    if type == "Fraud":
        type_list = [1 for _ in range(no_of_records)]
    elif type == "No Fraud":
        type_list = [0 for _ in range(no_of_records)]
    else :
        prob_of_1 = int(percentage[:-1])/100
        type_list = np.random.choice([0,1],size=no_of_records,p=[1-prob_of_1,prob_of_1])
    prob_of_1 = int(percentage[:-1]) / 100
    data = {"col1":np.random.choice([0,1],size=no_of_records,p=[1-prob_of_1,prob_of_1]),
            "col2":np.random.choice([0,1],size=no_of_records,p=[1-prob_of_1,prob_of_1]),
            "col3":np.random.choice([0,1],size=no_of_records,p=[1-prob_of_1,prob_of_1])}
    data = pd.DataFrame(data)
    return  data
if __name__ == "__main__":
    data = synthetic_data_gen()
    print(data)

