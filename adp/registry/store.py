"""In-memory registry store with TTL support."""
import time
from typing import Dict, Optional, List, Any
from datetime import datetime
from .models import ProviderDescriptor, OfferingDescriptor


class RegistryStore:
    def __init__(self):
        self._providers: Dict[str, Dict[str, Any]] = {}
        self._offerings: Dict[str, Dict[str, Any]] = {}
        self._audit_log: List[Dict[str, Any]] = []

    def register_provider(self, provider: ProviderDescriptor) -> ProviderDescriptor:
        self._providers[provider.provider_id] = {
            "data": provider,
            "expires_at": time.time() + provider.ttl_seconds,
        }
        return provider

    def get_provider(self, provider_id: str) -> Optional[ProviderDescriptor]:
        entry = self._providers.get(provider_id)
        if entry is None:
            return None
        if time.time() > entry["expires_at"]:
            del self._providers[provider_id]
            return None
        return entry["data"]

    def update_provider(self, provider_id: str, updates: Dict[str, Any]) -> Optional[ProviderDescriptor]:
        provider = self.get_provider(provider_id)
        if provider is None:
            return None
        updated = provider.model_copy(update={**updates, "updated_at": datetime.utcnow()})
        self._providers[provider_id]["data"] = updated
        self._providers[provider_id]["expires_at"] = time.time() + updated.ttl_seconds
        return updated

    def list_providers(self) -> List[ProviderDescriptor]:
        now = time.time()
        expired = [pid for pid, e in self._providers.items() if now > e["expires_at"]]
        for pid in expired:
            del self._providers[pid]
        return [e["data"] for e in self._providers.values()]

    def register_offering(self, offering: OfferingDescriptor) -> OfferingDescriptor:
        self._offerings[offering.offering_id] = {
            "data": offering,
            "expires_at": time.time() + offering.ttl_seconds,
        }
        return offering

    def get_offering(self, offering_id: str) -> Optional[OfferingDescriptor]:
        entry = self._offerings.get(offering_id)
        if entry is None:
            return None
        if time.time() > entry["expires_at"]:
            del self._offerings[offering_id]
            return None
        return entry["data"]

    def update_offering(self, offering_id: str, updates: Dict[str, Any]) -> Optional[OfferingDescriptor]:
        offering = self.get_offering(offering_id)
        if offering is None:
            return None
        updated = offering.model_copy(update={**updates, "updated_at": datetime.utcnow()})
        self._offerings[offering_id]["data"] = updated
        self._offerings[offering_id]["expires_at"] = time.time() + updated.ttl_seconds
        return updated

    def list_offerings(self, provider_id: Optional[str] = None) -> List[OfferingDescriptor]:
        now = time.time()
        expired = [oid for oid, e in self._offerings.items() if now > e["expires_at"]]
        for oid in expired:
            del self._offerings[oid]
        offerings = [e["data"] for e in self._offerings.values()]
        if provider_id:
            offerings = [o for o in offerings if o.provider_id == provider_id]
        return offerings

    def add_audit_log(self, record: Dict[str, Any]) -> None:
        self._audit_log.append(record)

    def get_audit_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        return self._audit_log[-limit:]


# Global singleton
_store = RegistryStore()


def get_store() -> RegistryStore:
    return _store
