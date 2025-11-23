"""Price API Routes"""

from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from config import get_logger, settings
from models.database import get_db
from services.price_service import get_market_price as get_price_service

logger = get_logger(__name__)
router = APIRouter()


@router.get("/price", response_model=None)
def get_price(
    crop: str = Query(..., description="Crop name"),
    state: str = Query(None, description="State name"),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Get market price for a crop in a specific state."""
    # Use config default if not provided
    state = state or settings.DEFAULT_STATE

    logger.info(f"Price endpoint called for {crop} in {state}")
    return get_price_service(db, crop, state)
