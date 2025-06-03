from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import List, Optional

app = FastAPI(
    title="My API",
    description="A simple FastAPI app deployed on Railway",
    version="1.0.0",
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory storage (replace with database in production)
items_db = [
    {"id": 1, "name": "Item 1", "description": "First item"},
    {"id": 2, "name": "Item 2", "description": "Second item"},
]


# Pydantic models
class Item(BaseModel):
    name: str
    description: Optional[str] = None


class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


# Routes
@app.get("/")
async def root():
    return {
        "message": "Welcome to my FastAPI app!",
        "status": "running",
        "endpoints": [
            "/docs - API documentation",
            "/items - Get all items",
            "/items/{id} - Get specific item",
            "/items (POST) - Create new item",
        ],
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": os.getenv("RAILWAY_ENVIRONMENT", "local"),
    }


@app.get("/items", response_model=List[ItemResponse])
async def get_items():
    return items_db


@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    item = next((item for item in items_db if item["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/items", response_model=ItemResponse)
async def create_item(item: Item):
    new_id = max(item["id"] for item in items_db) + 1 if items_db else 1
    new_item = {"id": new_id, "name": item.name, "description": item.description}
    items_db.append(new_item)
    return new_item


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    global items_db
    original_length = len(items_db)
    items_db = [item for item in items_db if item["id"] != item_id]

    if len(items_db) == original_length:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"message": f"Item {item_id} deleted successfully"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
