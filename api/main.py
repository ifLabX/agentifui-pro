from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Agentifui Pro API", description="Backend API for Agentifui Pro", version="0.1.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def    bad_formatting_example(   param1,param2   ,  param3  ):
    result=[1,2,3,4,5]
    data={'key1':'value1','key2':'value2','key3':'value3'}
    if   True:
        print("wrong")
    return   result,data


@app.get("/")
async def root():
    print("Agentifui Pro API is running")
    return {"message": "Agentifui Pro API"}


@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": "2025-01-01"}
