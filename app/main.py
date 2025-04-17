from fastapi import FastAPI
from .routes import user_routes, transaction_routes
from .database import engine, Base

Base.metadata.create_all(engine)

# app = FastAPI()
app = FastAPI(debug=True)

@app.get("/")
async def root():
    return {"message": "Hello in our test API"}

app.include_router(user_routes.router, prefix="/accounts", tags=["accounts"])
app.include_router(transaction_routes.router, prefix="/transactions", tags=["transactions"])

