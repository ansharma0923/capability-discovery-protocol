"""FastAPI route definitions."""
from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException

from ..federation.client import get_federation_client
from ..intent.models import DiscoveryIntent
from ..registry.models import OfferingDescriptor, ProviderDescriptor
from ..registry.store import RegistryStore, get_store
from ..service.discovery import run_discovery_pipeline

router = APIRouter()


def get_registry() -> RegistryStore:
    return get_store()


@router.post("/discover", response_model=Dict[str, Any])
async def discover(
    intent: DiscoveryIntent,
    store: RegistryStore = Depends(get_registry),
) -> Dict[str, Any]:
    """Execute intent-driven discovery pipeline."""
    federated_results = None

    if intent.preferences.include_federation:
        client = get_federation_client()
        federated_results = await client.federate(intent)

    result = run_discovery_pipeline(intent, store=store, federated_results=federated_results)
    return result


@router.post("/register/provider", response_model=Dict[str, Any])
def register_provider(
    provider: ProviderDescriptor,
    store: RegistryStore = Depends(get_registry),
) -> Dict[str, Any]:
    """Register a new provider."""
    registered = store.register_provider(provider)
    return {
        "status": "registered",
        "provider_id": registered.provider_id,
        "version": registered.version,
        "registered_at": registered.registered_at.isoformat(),
    }


@router.post("/register/offering", response_model=Dict[str, Any])
def register_offering(
    offering: OfferingDescriptor,
    store: RegistryStore = Depends(get_registry),
) -> Dict[str, Any]:
    """Register a new offering."""
    provider = store.get_provider(offering.provider_id)
    if provider is None:
        raise HTTPException(
            status_code=404, detail=f"Provider '{offering.provider_id}' not found"
        )
    registered = store.register_offering(offering)
    return {
        "status": "registered",
        "offering_id": registered.offering_id,
        "provider_id": registered.provider_id,
        "version": registered.version,
        "registered_at": registered.registered_at.isoformat(),
    }


@router.patch("/update/provider/{provider_id}", response_model=Dict[str, Any])
def update_provider(
    provider_id: str,
    updates: Dict[str, Any],
    store: RegistryStore = Depends(get_registry),
) -> Dict[str, Any]:
    """Update an existing provider."""
    updated = store.update_provider(provider_id, updates)
    if updated is None:
        raise HTTPException(status_code=404, detail=f"Provider '{provider_id}' not found")
    return {
        "status": "updated",
        "provider_id": updated.provider_id,
        "updated_at": updated.updated_at.isoformat(),
    }


@router.patch("/update/offering/{offering_id}", response_model=Dict[str, Any])
def update_offering(
    offering_id: str,
    updates: Dict[str, Any],
    store: RegistryStore = Depends(get_registry),
) -> Dict[str, Any]:
    """Update an existing offering."""
    updated = store.update_offering(offering_id, updates)
    if updated is None:
        raise HTTPException(status_code=404, detail=f"Offering '{offering_id}' not found")
    return {
        "status": "updated",
        "offering_id": updated.offering_id,
        "updated_at": updated.updated_at.isoformat(),
    }


@router.get("/providers/{provider_id}", response_model=Dict[str, Any])
def get_provider(
    provider_id: str,
    store: RegistryStore = Depends(get_registry),
) -> Dict[str, Any]:
    """Get provider by ID."""
    provider = store.get_provider(provider_id)
    if provider is None:
        raise HTTPException(status_code=404, detail=f"Provider '{provider_id}' not found")
    return provider.model_dump(mode="json")


@router.get("/offerings/{offering_id}", response_model=Dict[str, Any])
def get_offering(
    offering_id: str,
    store: RegistryStore = Depends(get_registry),
) -> Dict[str, Any]:
    """Get offering by ID."""
    offering = store.get_offering(offering_id)
    if offering is None:
        raise HTTPException(status_code=404, detail=f"Offering '{offering_id}' not found")
    return offering.model_dump(mode="json")


@router.post("/federate/discover", response_model=Dict[str, Any])
async def federate_discover(
    intent: DiscoveryIntent,
    store: RegistryStore = Depends(get_registry),
) -> Dict[str, Any]:
    """Execute federated discovery across registered nodes."""
    client = get_federation_client()
    federated_results = await client.federate(intent)
    result = run_discovery_pipeline(intent, store=store, federated_results=federated_results)
    result["_federation_nodes_queried"] = len(client.nodes)
    return result


@router.get("/health", response_model=Dict[str, Any])
def health_check(store: RegistryStore = Depends(get_registry)) -> Dict[str, Any]:
    """Health check endpoint."""
    providers = store.list_providers()
    offerings = store.list_offerings()
    return {
        "status": "healthy",
        "version": "0.1.0",
        "protocol": "CDP",
        "registry": {
            "providers": len(providers),
            "offerings": len(offerings),
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
