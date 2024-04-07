from sdv.single_table import CTGANSynthesizer
import numpy as np
from sdv.sampling import Condition
import pandas as pd
import torch


def synthatic_data_gen(no_of_records=100,type="Both",percentage="50%"):
    type_list=[]
    if type == "Fraud":
        type_list = [1 for _ in range(no_of_records)]
    elif type == "No Fraud":
        type_list = [0 for _ in range(no_of_records)]
    else :
        prob_of_1 = int(percentage[:-1])/100
        type_list = np.random.choice([0,1],size=no_of_records,p=[1-prob_of_1,prob_of_1])
    condition = Condition({'Label': type_list},num_rows = no_of_records)
    # synthesizer = CTGANSynthesizer.load('my_ctgan_model.pkl')
    # synthesizer = net.load_state_dict(torch.load('classifier.pt', map_location=torch.device('cpu')))
    synthesizer = torch.load('my_ctgan_model.pkl', map_location=torch.device('cpu'))
    synthatic_data = synthesizer.sample(conditions=[condition])
    return synthatic_data

def synthatic_data_gen_sample(no_of_records=100,type="Both",percentage="50%"):
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
    data = synthatic_data_gen()
    print(data)

