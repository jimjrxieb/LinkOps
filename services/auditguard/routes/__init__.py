from .audit import router as audit_router
from .compliance import router as compliance_router
from .security import router as security_router

all_routes = [audit_router, compliance_router, security_router]
