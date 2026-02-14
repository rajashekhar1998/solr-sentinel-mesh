import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "sentinel_active"}

def main():
    """Entry point for the console script"""
    # this is what runs when solr-sentinel command is run from the dockerfile
    uvicorn.run("solr_sentinel.main:app", host="0.0.0.0", port=8984, reload=False)

if __name__ == "__main__":
    main()