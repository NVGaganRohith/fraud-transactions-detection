import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from azureml.core import Workspace, Datastore
import argparse
import subprocess

from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication



# Now you can use `ws` to access your workspace
# print(ws.name, ws.location, ws.resource_group)





def preprocess_data(input_folder: str, preprocessed_folder: str):
    # Load the data from the URI folder into a DataFrame
    df = pd.read_csv(input_folder+"/real.csv")  # Update path to read from the URI folder

    # Scale the 'Time' column using StandardScaler
    df['Time'] = (df['Time'] - 43151.538158807896) / 24891.49100895904

    # Scale the 'Year' column using MinMaxScaler
    year_min, year_max = 2022, 2054
    month_min, month_max = 1, 12
    day_min, day_max = 1, 31

    # Scale the 'Year' column
    df['Year'] = (df['Year'] - year_min) / (year_max - year_min)

    # Scale the 'Month' column
    df['Month'] = (df['Month'] - month_min) / (month_max - month_min)

    # Scale the 'Day' column
    df['Day'] = (df['Day'] - day_min) / (day_max - day_min)

    # Perform one-hot encoding for categorical columns
    categorical_columns = ['Sender_Country', 'Bene_Country', 'Transaction_Type', 'Sender_Type', 'Bene_Type']
    one_hot_encoder = OneHotEncoder(handle_unknown='ignore')
    encoded_features = one_hot_encoder.fit_transform(df[categorical_columns])
    df.drop(categorical_columns, axis = 1, inplace = True)
    df.drop(["Transaction_Id"],axis=1, inplace = True)

    # Concatenate the encoded features with the original dataframe
    encoded_df = pd.DataFrame(encoded_features.toarray(), columns=one_hot_encoder.get_feature_names_out(categorical_columns))
    df = pd.concat([df, encoded_df], axis=1)

    # Concatenate additional columns
    df = pd.concat([df, df[['Sender_Sector', 'USD_amount']]], axis=1)

    # Save the preprocessed data to a CSV file
    csv_file = "preprocessed_data.csv"  # Update path to save to the URI folder
    df.to_csv(csv_file, index=False)

    
    # Define your service principal details
    tenant_id = '82d8af3b-d3f9-465c-b724-0fb186cc28c7'
    service_principal_id = 'f17afae0-e1d2-44f4-ad65-f8710ad76c3b'
    service_principal_password = 'h0j8Q~yeCCyV4oEZ4U1tUsGBmwocQv7hlMnkldmh'
    subscription_id = '24784a25-4b3b-4fbe-bd67-045821454fda'
    resource_group = 'Capstone_Project_Genpact'
    workspace_name = 'fraudML'

    # Create a service principal authentication object
    svc_pr = ServicePrincipalAuthentication(
        tenant_id=tenant_id,
        service_principal_id=service_principal_id,
        service_principal_password=service_principal_password
    )

    # Get the workspace
    ws = Workspace(subscription_id=subscription_id,
                resource_group=resource_group,
                workspace_name=workspace_name,
                auth=svc_pr)
    
    # Upload the CSV file to Azure ML datastore
    # subscription_id = '24784a25-4b3b-4fbe-bd67-045821454fda'
    # resource_group = 'Capstone_Project_Genpact'
    # workspace_name = 'fraudML'

    # Get the workspace
    # ws = Workspace(subscription_id=subscription_id, resource_group=resource_group, workspace_name=workspace_name)

    # Get the datastore
    datastore = Datastore.get(ws, datastore_name='workspaceblobstore')

    # Upload the CSV file to the datastore
    datastore.upload_files(files=[csv_file], target_path=preprocessed_folder, overwrite=True)

def main() -> None:
    package_name = "azureml-fsspec"
    subprocess.check_call(["python", "-m", "pip", "install", package_name])
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_folder", dest="input_folder")
    parser.add_argument("--preprocessed_folder", dest="preprocessed_folder")
    args = parser.parse_args() 

    preprocess_data(**vars(args))

if __name__ == "__main__":
    main()
