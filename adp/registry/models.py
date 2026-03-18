from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime, timezone
import uuid


class TrustLevel(str, Enum):
    UNVERIFIED = "unverified"
    BASIC = "basic"
    VERIFIED = "verified"
    CERTIFIED = "certified"


class ProviderDescriptor(BaseModel):
    provider_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    version: str = "0.1.0"
    name: str
    description: str
    categories: List[str]
    regions: List[str]
    trust_level: TrustLevel = TrustLevel.BASIC
    contact_url: Optional[str] = None
    api_endpoint: Optional[str] = None
    compliance_certifications: List[str] = Field(default_factory=list)
    avg_latency_ms: Optional[int] = None
    availability_score: float = Field(default=0.99, ge=0, le=1)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    registered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    ttl_seconds: int = Field(default=3600)


class OfferingDescriptor(BaseModel):
    offering_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    version: str = "0.1.0"
    provider_id: str
    name: str
    description: str
    category: str
    tags: List[str] = Field(default_factory=list)
    price: Optional[float] = None
    price_unit: Optional[str] = None
    currency: str = "USD"
    region: List[str] = Field(default_factory=list)
    latency_ms: Optional[int] = None
    delivery_days: Optional[int] = None
    availability: float = Field(default=0.99, ge=0, le=1)
    compliance: List[str] = Field(default_factory=list)
    capabilities: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    registered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    ttl_seconds: int = Field(default=3600)
    active: bool = True
