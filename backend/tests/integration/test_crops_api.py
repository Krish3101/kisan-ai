"""
Integration tests for Crops API endpoints
"""
import pytest


@pytest.mark.integration
class TestCropsAPI:
    """Test Crops API endpoints"""
    
    def test_get_crops(self, client, auth_headers):
        """Test GET /crops endpoint"""
        response = client.get("/crops", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_add_crop(self, client, auth_headers):
        """Test POST /crops/add endpoint"""
        crop_data = {
            "name": "Wheat",
            "variety": "HD-2967",
            "sowing_date": "2025-01-01",
            "growth_stage": "Sown",
            "plot_number": "A1"
        }
        response = client.post("/crops/add", json=crop_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Wheat"
        assert data["variety"] == "HD-2967"
    
    def test_delete_crop(self, client, auth_headers):
        """Test POST /crops/delete endpoint"""
        # First add a crop
        crop_data = {
            "name": "Wheat",
            "variety": "HD-2967",
            "sowing_date": "2025-01-01",
            "growth_stage": "Sown",
            "plot_number": "A1"
        }
        add_response = client.post("/crops/add", json=crop_data, headers=auth_headers)
        crop_id = add_response.json()["id"]
        
        # Then delete it
        delete_response = client.post("/crops/delete", json={"id": crop_id}, headers=auth_headers)
        assert delete_response.status_code == 200
