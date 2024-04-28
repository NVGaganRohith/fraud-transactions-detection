import os
import shutil
import argparse
from azureml.core import Workspace, Datastore
import subprocess

def select_file_from_directory(directory_path):
    # List files in the directory
    files = os.listdir(directory_path)

    # Select a file (example: select the first file)
    selected_file = files[0]

    return selected_file

def main():
    package_name = "azureml-fsspec"
    subprocess.check_call(["python", "-m", "pip", "install", package_name])
    parser = argparse.ArgumentParser(description="Select a file from the directory input")
    parser.add_argument("--input_folder", type=str, required=True, help="Input directory path")
    parser.add_argument("--selected_file_path", type=str, required=True, help="Output file path for the selected file")
    args = parser.parse_args()

    # Upload the CSV file to Azure ML datastore
    subscription_id = '24784a25-4b3b-4fbe-bd67-045821454fda'
    resource_group = 'Capstone_Project_Genpact'
    workspace_name = 'fraudML'

    # Get the workspace
    ws = Workspace(subscription_id=subscription_id, resource_group=resource_group, workspace_name=workspace_name)

    # Get the datastore
    datastore = Datastore.get(ws, datastore_name='workspaceblobstore')

    # Get the directory path from the input argument
    input_folder = args.input_folder

    # Select a file from the directory
    selected_file = select_file_from_directory(input_folder)

    # Construct the full path for the selected file
    selected_file_path = os.path.join(input_folder, selected_file)

    # Copy the selected file to the specified output path
    shutil.copy(selected_file_path, args.selected_file_path)

if __name__ == "__main__":
    main()
