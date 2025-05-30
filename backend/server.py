from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

class ClickTracking(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    click_type: str  # 'beacons_link', 'share', 'view'
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ClickTrackingCreate(BaseModel):
    click_type: str
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None

class PromoContent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    subtitle: str
    description: str
    call_to_action: str
    target_url: str
    view_count: int = 0
    click_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "TikTok Style Promo API Ready!"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

@api_router.get("/promo-content")
async def get_promo_content():
    """Get the main promotional content"""
    content = {
        "id": str(uuid.uuid4()),
        "title": "💰 Make Money From Your PC! 💰",
        "subtitle": "Discover the Secret to Earning $100+ Daily",
        "description": "Transform your computer into a money-making machine! Join thousands who are already earning from home.",
        "call_to_action": "Start Making Money Now!",
        "target_url": "https://beacons.ai/junior47620",
        "benefits": [
            "🏠 Work from anywhere",
            "⏰ Flexible hours",
            "💻 Only need a PC/laptop",
            "🚀 Start earning today",
            "📈 Unlimited earning potential"
        ],
        "testimonials": [
            {
                "name": "Sarah M.",
                "amount": "$250/day",
                "quote": "I couldn't believe how easy it was to start earning!"
            },
            {
                "name": "Mike R.", 
                "amount": "$180/day",
                "quote": "Finally found something that actually works!"
            },
            {
                "name": "Jessica L.",
                "amount": "$320/day", 
                "quote": "My PC is now my personal ATM!"
            }
        ]
    }
    
    # Increment view count
    await db.analytics.update_one(
        {"type": "promo_views"}, 
        {"$inc": {"count": 1}}, 
        upsert=True
    )
    
    return content

@api_router.post("/track-click")
async def track_click(click_data: ClickTrackingCreate):
    """Track user interactions for analytics"""
    click_obj = ClickTracking(**click_data.dict())
    await db.click_tracking.insert_one(click_obj.dict())
    
    # Update analytics counters
    await db.analytics.update_one(
        {"type": f"clicks_{click_data.click_type}"}, 
        {"$inc": {"count": 1}}, 
        upsert=True
    )
    
    return {"status": "tracked", "click_type": click_data.click_type}

@api_router.get("/analytics")
async def get_analytics():
    """Get basic analytics data"""
    analytics = await db.analytics.find().to_list(100)
    
    result = {
        "total_views": 0,
        "total_clicks": 0,
        "beacons_clicks": 0,
        "share_clicks": 0
    }
    
    for item in analytics:
        if item["type"] == "promo_views":
            result["total_views"] = item.get("count", 0)
        elif item["type"] == "clicks_beacons_link":
            result["beacons_clicks"] = item.get("count", 0)
            result["total_clicks"] += item.get("count", 0)
        elif item["type"] == "clicks_share":
            result["share_clicks"] = item.get("count", 0)
            result["total_clicks"] += item.get("count", 0)
    
    return result

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
