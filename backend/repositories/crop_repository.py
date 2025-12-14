"""
Crop Repository
Data access layer for Crop operations
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from backend.models.database import Crop
from backend.repositories.base import BaseRepository


class CropRepository(BaseRepository[Crop]):
    """Repository for Crop data access"""
    
    def __init__(self):
        super().__init__(Crop)
    
    def get_by_user(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Crop]:
        """Get all crops for a specific user"""
        return db.query(Crop)\
            .filter(Crop.user_id == user_id)\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    def get_by_id_and_user(self, db: Session, crop_id: int, user_id: int) -> Optional[Crop]:
        """Get crop by ID and user_id"""
        return db.query(Crop)\
            .filter(Crop.id == crop_id, Crop.user_id == user_id)\
            .first()
    
    def get_by_stage(self, db: Session, user_id: int, stage: str) -> List[Crop]:
        """Get crops by growth stage"""
        return db.query(Crop)\
            .filter(Crop.user_id == user_id, Crop.growth_stage == stage)\
            .all()
    
    def update_stage(self, db: Session, crop_id: int, user_id: int, stage: str) -> Optional[Crop]:
        """Update crop growth stage"""
        crop = self.get_by_id_and_user(db, crop_id, user_id)
        if crop:
            crop.growth_stage = stage
            db.commit()
            db.refresh(crop)
        return crop
    
    def count_by_user(self, db: Session, user_id: int) -> int:
        """Count crops for a user"""
        return db.query(Crop).filter(Crop.user_id == user_id).count()


# Global instance
crop_repository = CropRepository()
