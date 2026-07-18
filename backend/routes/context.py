"""Patient Context Model endpoints.

Read-only: the live belief state, its completeness score, and the full provenance
ledger. Writes happen only through the orchestrator and the deterministic source
adapters (pcm.record_contribution), never through the API — same
human-out-of-the-write-loop discipline as the chart.

Views:
  GET /api/visits/{id}/context      — the visit view: patient slots decorated
                                      with what THIS visit requires + why.
  GET /api/patients/{id}/context    — the patient view: the running status
                                      across all sources, full ledger.
  GET /api/patients/{id}/context.md — the same, rendered as the markdown
                                      projection (every line footnoted with the
                                      ledger entry that justifies it).
"""

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

import context_render
from db import one
from orchestrator import pcm
from routes.core import ApiError, ContractRoute

router = APIRouter(prefix="/api", route_class=ContractRoute)


@router.get("/visits/{visit_id}/context")
async def get_context(visit_id: int):
    if one("SELECT id FROM visits WHERE id=?", (visit_id,)) is None:
        raise ApiError(404, "not_found", f"unknown visit {visit_id}")
    return pcm.get_pcm(visit_id)


@router.get("/patients/{patient_id}/context")
async def get_patient_context(patient_id: int):
    if one("SELECT id FROM patients WHERE id=?", (patient_id,)) is None:
        raise ApiError(404, "not_found", f"unknown patient {patient_id}")
    return pcm.get_patient_pcm(patient_id)


@router.get("/patients/{patient_id}/context.md")
async def get_patient_context_md(patient_id: int):
    if one("SELECT id FROM patients WHERE id=?", (patient_id,)) is None:
        raise ApiError(404, "not_found", f"unknown patient {patient_id}")
    return PlainTextResponse(
        context_render.render_patient_md(patient_id), media_type="text/markdown"
    )
