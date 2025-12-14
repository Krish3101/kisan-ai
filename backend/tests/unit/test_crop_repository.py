"""
Unit tests for Crop Repository
"""
import pytest
from backend.repositories.crop_repository import crop_repository
from backend.models.database import Crop


@pytest.mark.unit
class TestCropRepository:
    """Test Crop Repository methods"""
    
    def test_get_by_user(self, db, test_user):
        """Test getting crops by user"""
        # Create test crops
        crop1 = Crop(
            name="Wheat",
            variety="HD-2967",
            sowing_date="2025-01-01",
            growth_stage="Sown",
            plot_number="A1",
            user_id=test_user.id
        )
        crop2 = Crop(
            name="Rice",
            variety="Basmati",
            sowing_date="2025-01-02",
            growth_stage="Germination",
            plot_number="A2",
            user_id=test_user.id
        )
        db.add_all([crop1, crop2])
        db.commit()
        
        # Test retrieval
        crops = crop_repository.get_by_user(db, test_user.id)
        assert len(crops) == 2
        assert crops[0].name in ["Wheat", "Rice"]
    
    def test_get_by_stage(self, db, test_user):
        """Test getting crops by growth stage"""
        crop = Crop(
            name="Wheat",
            variety="HD-2967",
            sowing_date="2025-01-01",
            growth_stage="Sown",
            plot_number="A1",
            user_id=test_user.id
        )
        db.add(crop)
        db.commit()
        
        crops = crop_repository.get_by_stage(db, test_user.id, "Sown")
        assert len(crops) == 1
        assert crops[0].growth_stage == "Sown"
    
    def test_update_stage(self, db, test_user):
        """Test updating crop growth stage"""
        crop = Crop(
            name="Wheat",
            variety="HD-2967",
            sowing_date="2025-01-01",
            growth_stage="Sown",
            plot_number="A1",
            user_id=test_user.id
        )
        db.add(crop)
        db.commit()
        
        updated_crop = crop_repository.update_stage(db, crop.id, test_user.id, "Germination")
        assert updated_crop.growth_stage == "Germination"
    
    def test_count_by_user(self, db, test_user):
        """Test counting crops for a user"""
        crop = Crop(
            name="Wheat",
            variety="HD-2967",
            sowing_date="2025-01-01",
            growth_stage="Sown",
            plot_number="A1",
            user_id=test_user.id
        )
        db.add(crop)
        db.commit()
        
        count = crop_repository.count_by_user(db, test_user.id)
        assert count == 1
