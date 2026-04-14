import asyncio
import argparse
import os
import pandas as pd
from typing import List
from dotenv import load_dotenv

from app.infrastructure.factory import get_vector_store
from app.services.vector_service import VectorService
from app.services.ingestion_service import IngestionService
from app.embeddings.factory import EmbeddingFactory
from app.ingestion.excel_ingestor import ExcelIngestor
from app.utils.file_processor import FileProcessor

async def main():
    parser = argparse.ArgumentParser(description="Ingest Excel data into Pinecone/Vector Store")
    parser.add_argument("file_path", help="Path to the Excel file (.xlsx or .xls)")
    parser.add_argument("--id_column", help="Column name to use as record ID", default=None)
    parser.add_argument("--text_columns", help="Comma-separated column names to include in the embedding text", default=None)
    parser.add_argument("--sheet", help="Sheet name to read (default is first sheet)", default=0)
    parser.add_argument("--index_name", help="Pinecone index name (overrides .env)", default=None)
    parser.add_argument("--dimension", type=int, help="Vector dimension", default=384)
    
    args = parser.parse_args()
    
    load_dotenv()
    
    # 1. Initialize Infrastructure
    index_name = args.index_name or os.getenv('PINECONE_INDEX_NAME', 'vectors')
    print(f"Initializing connection to {os.getenv('VECTOR_DB_PROVIDER', 'chroma')} (index: {index_name})...")
    
    # We need to pass the dimension and potentially a different index name
    from app.infrastructure.vector_stores.pinecone.store import PineconeStore
    
    if os.getenv('VECTOR_DB_PROVIDER') == 'pinecone':
        vector_store = PineconeStore(
            api_key=os.getenv('PINECONE_API_KEY'),
            environment=os.getenv('PINECONE_ENVIRONMENT', 'us-east-1'),
            index_name=index_name,
            dimension=args.dimension
        )
    else:
        vector_store = get_vector_store()
    
    vector_service = VectorService(vector_store)
    
    # Using local embedding provider by default
    embedding_provider = EmbeddingFactory.create(
        provider="local",
        model_name="all-MiniLM-L6-v2"
    )
    
    ingestion_service = IngestionService(
        embedding_provider=embedding_provider,
        vector_service=vector_service
    )
    
    excel_ingestor = ExcelIngestor(ingestion_service=ingestion_service)
    
    # 2. Process File
    print(f"Reading file: {args.file_path}...")
    if not os.path.exists(args.file_path):
        print(f"Error: File not found: {args.file_path}")
        return

    try:
        with open(args.file_path, "rb") as f:
            content = f.read()
        
        # We can use FileProcessor or pandas directly here to handle the sheet
        df = pd.read_excel(args.file_path, sheet_name=args.sheet)
        # Handle NaN values for JSON compatibility
        df = df.replace({pd.NA: None}).where(pd.notnull(df), None)
        records = df.to_dict(orient="records")
        
        print(f"Found {len(records)} records in Excel.")
        
        # 3. Ingest
        text_cols = args.text_columns.split(",") if args.text_columns else None
        
        print("Starting ingestion...")
        ids = await excel_ingestor.ingest_bulk_excel(
            records=records,
            id_column=args.id_column,
            text_columns=text_cols
        )
        
        print(f"Successfully ingested {len(ids)} records into {os.getenv('VECTOR_DB_PROVIDER')}!")
        print(f"Namespace/Collection: {excel_ingestor.collection}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
