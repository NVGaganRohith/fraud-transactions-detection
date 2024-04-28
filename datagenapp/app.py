import pandas as pd
import streamlit as st
import generate_data_ctgan
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import datetime




st.title("Generating Data")

# Define a function to initialize session state variables
def init_session_state():
    st.session_state.data = pd.DataFrame([], columns=["Time_step", "Transaction_Id", "Sender_Id", "Sender_Account", "Sender_Country",
                                  "Sender_Sector", "Sender_lob", "Bene_Id", "Bene_Account", "Bene_Country",
                                  "USD_amount", "Label", "Transaction_Type"])

    st.session_state.number_of_records = 0
    st.session_state.type_of_data = "Fraud"
    st.session_state.percentage_of_fraud_data = "50%"

# Check if session state variables are initialized
if 'data' not in st.session_state:
    init_session_state()

# Sidebar section for user input
def user_input():
    num_records = st.sidebar.number_input("Number of records", min_value=0)
    st.session_state.number_of_records = num_records

    data_type = st.sidebar.selectbox("Data Type", ["Fraud", "No Fraud", "Both"])
    st.session_state.type_of_data = data_type
    if data_type == "Both":
        data_gen_percentage()
    st.sidebar.button("Generate Data",on_click= generate_data_base_data)
    st.sidebar.button("Upload Data to Cloud",on_click=upload_data_to_cloud)

def upload_data_to_cloud():
    connection_string = "DefaultEndpointsProtocol=https;AccountName=frauddataproject;AccountKey=X9yDy+C2CyV6oz7bmUYiyCROovcdxrSAVVHq+7GfGMitZhT7ImajRnohuHfkhosvxEFfYYaifqvR+AStb0GJBw==;EndpointSuffix=core.windows.net"
    container_name = "real-time-data"

    pd_data = pd.DataFrame(st.session_state.data)
    if pd_data.shape[0] > 0:
        try:
            now = datetime.datetime.now()
            file_path = f"generate_synthetic_data_file_{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}_{now.second}.csv"
            pd_data.to_csv(file_path)
            # Create a BlobServiceClient object
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)

            # Create a client to interact with the container
            container_client = blob_service_client.get_container_client(container_name)

            # Upload the file to the blob

            with open(file_path, "rb") as data:
                blob_client = container_client.upload_blob(name=file_path, data=data)
            st.success("File Uploaded Successfully")  # Display success message in Streamlit UI
        except Exception as e:
            print(f"Error uploading file: {e}")
    else:
        st.warning("No data Generated")



def generate_data_base_data():
    generated_data = generate_data_ctgan.synthetic_data_gen(no_of_records=st.session_state.number_of_records,
                                                                   type=st.session_state.type_of_data,
                                                                   percentage=st.session_state.percentage_of_fraud_data)
    st.session_state.data = generated_data

    print("generate_data", "====================================")
    if generated_data.shape[0]>0:
        st.success("Data Generation Successfully")
    else:
        st.warning("Number of records >= 1")


def data_gen_percentage():
    percentage_list = [str(i) + "%" for i in range(10, 100, 10)]
    percent_data = st.sidebar.selectbox("Percentage of Fraud", percentage_list)
    st.session_state.percentage_of_fraud_data = percent_data

user_input()

# Display the dataframe
st.dataframe(st.session_state.data)
