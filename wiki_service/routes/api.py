from fastapi import APIRouter

from wiki_service.routes import kubernetes, wiki

router = APIRouter()
router.include_router(kubernetes.router)
router.include_router(wiki.router, prefix='/wiki')
router.include_router(wiki.adminRouter, prefix='/admin/wiki')
