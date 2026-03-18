"""ADP FastAPI application entry point."""
import logging
import json
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.middleware import RequestLoggingMiddleware
from .api.routes import router
from .registry.store import get_store
from .registry.models import ProviderDescriptor, OfferingDescriptor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)

_log = logging.getLogger("adp")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load sample data on startup."""
    store = get_store()
    data_dir = Path(__file__).parent.parent / "data"

    providers_file = data_dir / "providers.json"
    if providers_file.exists():
        with open(providers_file) as f:
            providers_data = json.load(f)
        for pd in providers_data:
            store.register_provider(ProviderDescriptor(**pd))
        _log.info(f"Loaded {len(providers_data)} providers from data/")

    offerings_file = data_dir / "offerings.json"
    if offerings_file.exists():
        with open(offerings_file) as f:
            offerings_data = json.load(f)
        for od in offerings_data:
            store.register_offering(OfferingDescriptor(**od))
        _log.info(f"Loaded {len(offerings_data)} offerings from data/")

    yield


app = FastAPI(
    title="Agent Discovery Protocol",
    description="A protocol for intent-driven discovery of agents, services, and products.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
