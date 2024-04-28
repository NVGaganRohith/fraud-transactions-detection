from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


def list_files_in_azure_blob_storage(connection_string, container_name):
    try:
        # Create a BlobServiceClient object
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Create a client to interact with the container
        container_client = blob_service_client.get_container_client(container_name)

        # List all blobs in the container
        blob_list = container_client.list_blobs()

        print("List of files in the container:")
        for blob in blob_list:
            print(blob.name)

    except Exception as e:
        print(f"Error listing files: {e}")


# Azure Blob Storage connection string and container name
connection_string = "DefaultEndpointsProtocol=https;AccountName=frauddatastore;AccountKey=NZkEnp/50rtXeB+B1Q8GtNIchp+bBKRubiF2ZYjo9TOKcGP0qGlzrLCjBd8LqYVfkN8XANucYQfP+AStyQPJSA==;EndpointSuffix=core.windows.net"
container_name = "frauddatastore"

list_files_in_azure_blob_storage(connection_string, container_name)
