"""Alembic router for executing database migrations via API."""

import io
from contextlib import redirect_stdout

from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
from fastapi import APIRouter, HTTPException, status

from app.config import get_settings
from app.schemas.alembic import (
    AlembicCurrentResponse,
    AlembicDowngradeRequest,
    AlembicHistoryItem,
    AlembicHistoryResponse,
    AlembicResponse,
    AlembicRevisionRequest,
    AlembicUpgradeRequest,
)

router = APIRouter(prefix="/alembic", tags=["alembic"])


def get_alembic_config() -> Config:
    """Get Alembic configuration with database URL from settings."""
    settings = get_settings()
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)
    return alembic_cfg


@router.post("/upgrade", response_model=AlembicResponse)
def upgrade(request: AlembicUpgradeRequest):
    """Run alembic upgrade to the specified revision."""
    try:
        alembic_cfg = get_alembic_config()
        output = io.StringIO()
        with redirect_stdout(output):
            command.upgrade(alembic_cfg, request.revision)
        return AlembicResponse(
            success=True,
            message=f"Successfully upgraded to revision: {request.revision}",
            output=output.getvalue() or None,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Migration upgrade failed: {str(e)}",
        )


@router.post("/downgrade", response_model=AlembicResponse)
def downgrade(request: AlembicDowngradeRequest):
    """Run alembic downgrade to the specified revision."""
    try:
        alembic_cfg = get_alembic_config()
        output = io.StringIO()
        with redirect_stdout(output):
            command.downgrade(alembic_cfg, request.revision)
        return AlembicResponse(
            success=True,
            message=f"Successfully downgraded to revision: {request.revision}",
            output=output.getvalue() or None,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Migration downgrade failed: {str(e)}",
        )


@router.get("/current", response_model=AlembicCurrentResponse)
def current():
    """Get current alembic revision."""
    try:
        alembic_cfg = get_alembic_config()
        output = io.StringIO()
        with redirect_stdout(output):
            command.current(alembic_cfg)
        output_str = output.getvalue().strip()
        current_revision = output_str if output_str else None
        return AlembicCurrentResponse(
            success=True,
            current_revision=current_revision,
            message="Successfully retrieved current revision",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get current revision: {str(e)}",
        )


@router.get("/history", response_model=AlembicHistoryResponse)
def history():
    """Get alembic migration history."""
    try:
        alembic_cfg = get_alembic_config()
        script = ScriptDirectory.from_config(alembic_cfg)
        revisions = []
        for rev in script.walk_revisions():
            revisions.append(
                AlembicHistoryItem(
                    revision=rev.revision,
                    down_revision=rev.down_revision if isinstance(rev.down_revision, str) else None,
                    message=rev.doc,
                )
            )
        return AlembicHistoryResponse(
            success=True,
            revisions=revisions,
            message="Successfully retrieved migration history",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get migration history: {str(e)}",
        )


@router.post("/revision", response_model=AlembicResponse)
def revision(request: AlembicRevisionRequest):
    """Create a new alembic revision."""
    try:
        alembic_cfg = get_alembic_config()
        output = io.StringIO()
        with redirect_stdout(output):
            command.revision(
                alembic_cfg,
                message=request.message,
                autogenerate=request.autogenerate,
            )
        return AlembicResponse(
            success=True,
            message=f"Successfully created new revision: {request.message}",
            output=output.getvalue() or None,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create revision: {str(e)}",
        )
