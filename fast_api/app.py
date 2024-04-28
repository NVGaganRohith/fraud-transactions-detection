import pandas as pd
from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import List
import pickle
from my_transformations import do_transformations

# Load your pre-trained model
with open("dt_model_regularized.pkl", "rb") as f:
    model = pickle.load(f, encoding="latin1")

app = FastAPI()

class payload_received(BaseModel):
    Transaction_Id: str
    Sender_Country: str
    Sender_Sector: float
    Bene_Country: str
    USD_amount: float
    Transaction_Type: str
    Sender_Type: str
    Bene_Type: str
    Time: int
    Year: int
    Month: int
    Day: int

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

@app.get("/predict", status_code=status.HTTP_201_CREATED)
def create_post(InputData: payload_received):   
    # Convert received payload into DataFrame
    print(InputData)
    data = {"Transaction_Id": [InputData.Transaction_Id],
            "Sender_Country": [InputData.Sender_Country],
            "Sender_Sector": [InputData.Sender_Sector],
            "Bene_Country": [InputData.Bene_Country],
            "USD_amount": [InputData.USD_amount],
            "Transaction_Type": [InputData.Transaction_Type],
            "Sender_Type": [InputData.Sender_Type],
            "Bene_Type": [InputData.Bene_Type],
            "Time": [InputData.Time],
            "Year": [InputData.Year],
            "Month": [InputData.Month],
            "Day": [InputData.Day]}
    
    df = pd.DataFrame.from_dict(data)
    print(InputData, data,df)
    df = do_transformations(df)
    print(df)

    # Perform prediction
    predictions = model.predict(df)
    column_names = df.columns.tolist()

    return {"predictions": predictions.tolist(), "column_names": column_names}
