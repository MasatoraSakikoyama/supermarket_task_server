"""Alembic router for executing database migrations via API."""

import io
from contextlib import redirect_stdout
from pathlib import Path

from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.util.exc import CommandError
from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import get_current_user
from app.config import get_settings
from app.models.user import User
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

# Get the project root directory (where alembic.ini is located)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ALEMBIC_INI_PATH = PROJECT_ROOT / "alembic.ini"


def get_alembic_config() -> Config:
    """Get Alembic configuration with database URL from settings."""
    settings = get_settings()
    alembic_cfg = Config(str(ALEMBIC_INI_PATH))
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)
    return alembic_cfg


@router.post("/upgrade", response_model=AlembicResponse)
def upgrade(
    request: AlembicUpgradeRequest,
    current_user: User = Depends(get_current_user),
):
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
    except CommandError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Migration upgrade failed: {str(e)}",
        )


@router.post("/downgrade", response_model=AlembicResponse)
def downgrade(
    request: AlembicDowngradeRequest,
    current_user: User = Depends(get_current_user),
):
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
    except CommandError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Migration downgrade failed: {str(e)}",
        )


@router.get("/current", response_model=AlembicCurrentResponse)
def current(current_user: User = Depends(get_current_user)):
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
    except CommandError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get current revision: {str(e)}",
        )


@router.get("/history", response_model=AlembicHistoryResponse)
def history(current_user: User = Depends(get_current_user)):
    """Get alembic migration history."""
    try:
        alembic_cfg = get_alembic_config()
        script = ScriptDirectory.from_config(alembic_cfg)
        revisions = []
        for rev in script.walk_revisions():
            # down_revision can be None, a string, or a tuple for branch merges
            down_rev = rev.down_revision
            down_revision_str = down_rev if isinstance(down_rev, str) else None
            revisions.append(
                AlembicHistoryItem(
                    revision=rev.revision,
                    down_revision=down_revision_str,
                    message=rev.doc,
                )
            )
        return AlembicHistoryResponse(
            success=True,
            revisions=revisions,
            message="Successfully retrieved migration history",
        )
    except CommandError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get migration history: {str(e)}",
        )


@router.post("/revision", response_model=AlembicResponse)
def revision(
    request: AlembicRevisionRequest,
    current_user: User = Depends(get_current_user),
):
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
    except CommandError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create revision: {str(e)}",
        )
