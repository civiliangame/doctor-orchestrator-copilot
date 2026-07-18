"""Patient Context Model endpoint (Phase 1 of the agentic harness).

Read-only: the live belief state, its completeness score, and the full provenance
ledger for a visit. Writes happen only through the orchestrator (pcm.record_contribution),
never through the API — same human-out-of-the-write-loop discipline as the chart.
"""

from fastapi import APIRouter

from db import one
from orchestrator import pcm
from routes.core import ApiError, ContractRoute

router = APIRouter(prefix="/api", route_class=ContractRoute)


@router.get("/visits/{visit_id}/context")
async def get_context(visit_id: int):
    if one("SELECT id FROM visits WHERE id=?", (visit_id,)) is None:
        raise ApiError(404, "not_found", f"unknown visit {visit_id}")
    return pcm.get_pcm(visit_id)
