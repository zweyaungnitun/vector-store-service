import asyncio
import httpx
import pandas as pd
import io

async def test_large_ingestion():
    url = "http://localhost:8000/api/v1/ingest/file?target=excel"
    
    # Create a large dummy dataframe (e.g., 6000 rows to trigger chunking)
    df = pd.DataFrame({
        "Reference": [f"REF_{i}" for i in range(6000)],
        "Value": [i * 1.5 for i in range(6000)],
        "Status": ["Active" if i % 2 == 0 else "Inactive" for i in range(6000)]
    })
    
    # Save to Excel in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    content = output.getvalue()
    
    files = {'file': ('large_test.xlsx', content, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
    
    print("Sending large excel file for ingestion...")
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, files=files)
        
    if response.status_code == 200:
        result = response.json()
        print(f"Success! Ingested {result['count']} records.")
        print(f"IDs: {result['ids'][:5]}... ({len(result['ids'])} total)")
    else:
        print(f"Failed! Status code: {response.status_code}")
        print(f"Error: {response.text}")

if __name__ == "__main__":
    asyncio.run(test_large_ingestion())
