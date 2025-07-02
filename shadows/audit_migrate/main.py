from fastapi import FastAPI
from routers import migrate_router, remote_link_router, cursor_patch_router

app = FastAPI(
    title="Audit Migrate Service",
    description=(
        "Generate real folder structures and microservices from scaffold plans. "
        "Linked to audit_assess, audit_logic, whis_logic, igris_logic."
    ),
    version="1.0.0",
)

app.include_router(migrate_router.router)
app.include_router(remote_link_router.router)
app.include_router(cursor_patch_router.router)
