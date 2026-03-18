from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime, timezone
import uuid


class Category(str, Enum):
    PRODUCT = "product"
    SERVICE = "service"
    AGENT = "agent"
    DATA = "data"
    COMPUTE = "compute"
    API = "api"


class RankingProfile(str, Enum):
    DEFAULT = "default"
    COST_OPTIMIZED = "cost_optimized"
    LATENCY_OPTIMIZED = "latency_optimized"
    TRUST_OPTIMIZED = "trust_optimized"


class Constraints(BaseModel):
    max_price: Optional[float] = None
    currency: Optional[str] = "USD"
    region: Optional[List[str]] = None
    max_latency_ms: Optional[int] = None
    delivery_days: Optional[int] = None
    compliance: Optional[List[str]] = None
    availability_min: Optional[float] = None


class Preferences(BaseModel):
    ranking_profile: RankingProfile = RankingProfile.DEFAULT
    max_results: int = Field(default=10, ge=1, le=100)
    include_federation: bool = False


class DiscoveryIntent(BaseModel):
    intent_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    version: str = "0.1.0"
    intent_text: str = Field(..., min_length=1, max_length=2000)
    category: Category
    constraints: Constraints = Field(default_factory=Constraints)
    preferences: Preferences = Field(default_factory=Preferences)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
