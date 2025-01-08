from llama_index.core import download_loader, VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import StorageContext
from pinecone import Pinecone
import tempfile
from io import BytesIO
import os


pinecone_index = pinecone_client.Index("demo")


def listofURLs(DATA_URL):
    BeautifulSoupWebReader = download_loader("BeautifulSoupWebReader")

    loader = BeautifulSoupWebReader()
    # print(f'Datttta: {DATA_URL.items}    dddd')
    documents = loader.load_data(urls=DATA_URL.items)

    # Create a PineconeVectorStore using the specified pinecone_index
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

    # Create a StorageContext using the created PineconeVectorStore
    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )

    # Use the chunks of documents and the storage_context to create the index
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context
    )

    return index

def pdfdataLoader(file: BytesIO):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(file.getvalue())
        temp_file_path = temp_file.name

    try:
        # Now that we have a file path, you can use SimpleDirectoryReader
        doc = SimpleDirectoryReader(input_files=[temp_file_path]).load_data()
        vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

        storage_context = StorageContext.from_defaults(
            vector_store=vector_store
        )

        index = VectorStoreIndex.from_documents(
            doc,
            storage_context=storage_context
        )
        
    finally:
        # Make sure to delete the temporary file after processing
        os.remove(temp_file_path)

    return index


def vsAlreadyExists():
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    return index
