from fastapi import FastAPI
# from app.api.v1.endpoints import query

app = FastAPI(title="Med RAG Drug Assistant")

# app.include_router(query.router, prefix="/api/v1", tags=["query"])
