# 🔧 KisanAI - Backend Best Practices Guide

> **Purpose:** Standardize backend code patterns, error handling, type hints, and database practices.

---

## 📋 Table of Contents

1. [Code Quality & Formatting](#-code-quality--formatting)
2. [Type Hints & Annotations](#type-hints--annotations)
3. [Error Handling Patterns](#error-handling-patterns)
4. [Database Best Practices](#database-best-practices)
5. [Service Layer Patterns](#service-layer-patterns)
6. [Route Patterns](#route-patterns)
7. [Caching Strategies](#caching-strategies)
8. [Security Best Practices](#security-best-practices)

---

##  Linting & Formatting (Ruff)

This project uses **Ruff** for linting and formatting to ensure code quality and consistency.

### How to Use

-   **Check for issues:**
    ```bash
    # Run from the project root
    .venv\Scripts\ruff.exe check backend
    ```
-   **Automatically fix issues:**
    ```bash
    # Run from the project root
    .venv\Scripts\ruff.exe check backend --fix
    ```
-   **Format all files:**
    ```bash
    # Run from the project root
    .venv\Scripts\ruff.exe format backend
    ```
The configuration for `ruff` can be found in `backend/ruff.toml`.

---

## 🏷️ Type Hints & Annotations

### ✅ Always Add Type Hints

```python
from datetime import datetime
from sqlalchemy.orm import Session
from models.database import Crop
from models.schemas import CropCreate

# Bad - no type hints
def get_crop(db, crop_id):
    return db.query(Crop).filter(Crop.id == crop_id).first()

# Good - complete type hints
def get_crop(db: Session, crop_id: int) -> Crop | None:
    """
    Retrieve a crop by ID.
    
    Args:
        db: Database session
        crop_id: ID of the crop to retrieve
        
    Returns:
        Crop object if found, None otherwise
    """
    return db.query(Crop).filter(Crop.id == crop_id).first()
```

### Function Return Types

```python
# Simple return
def get_all_crops(db: Session) -> list[Crop]:
    return db.query(Crop).all()

# Dictionary return
def get_summary(db: Session) -> dict[str, Any]:
    return {
        "total_crops": db.query(Crop).count(),
        "active_crops": db.query(Crop).filter(Crop.stage != "Harvested").count()
    }

# Optional return (might be None)
def find_crop_by_name(db: Session, name: str) -> Crop | None:
    return db.query(Crop).filter(Crop.name == name).first()

# Boolean return
def delete_crop(db: Session, crop_id: int) -> bool:
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if crop:
        db.delete(crop)
        db.commit()
        return True
    return False
```

### Pydantic Schema Type Hints

```python
from pydantic import BaseModel, Field
from datetime import date

class CropCreate(BaseModel):
    """Schema for creating a new crop"""
    name: str = Field(..., min_length=1, max_length=100, description="Crop name")
    type: str = Field(..., min_length=1, description="Crop type")
    plot: str = Field(..., min_length=1, description="Plot/field identifier")
    sowing_date: date = Field(..., description="Date when crop was sown")
    stage: str = Field(default="Sown", description="Current growth stage")
    
class CropResponse(BaseModel):
    """Schema for crop response"""
    id: int
    name: str
    type: str
    plot: str
    sowing_date: date
    stage: str
    created_at: datetime
    
    class Config:
        from_attributes = True  # Replaces orm_mode in Pydantic v2
```

---

## ⚠️ Error Handling Patterns

### Standardized Error Responses

```python
from fastapi import HTTPException, status

# This custom exception can be defined in a helpers module
class StorageError(Exception):
    """Custom exception for database-related errors."""
    pass

# Common errors
def not_found_error(resource: str, id: int):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{resource} with id {id} not found"
    )

def validation_error(message: str):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message
    )

def unauthorized_error():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
```

### Service Layer Error Handling

```python
import logging

logger = logging.getLogger(__name__)

def get_crop_safe(db: Session, crop_id: int) -> Crop | None:
    """
    Safely retrieve a crop with error logging.
    
    Args:
        db: Database session
        crop_id: Crop ID to retrieve
        
    Returns:
        Crop object if found, None if not found or error occurred
    """
    try:
        crop = db.query(Crop).filter(Crop.id == crop_id).first()
        if not crop:
            logger.warning(f"Crop with id {crop_id} not found")
        return crop
    except Exception as e:
        logger.error(f"Error retrieving crop {crop_id}: {e}")
        return None

def add_crop_safe(db: Session, crop_data: CropCreate) -> Crop | None:
    """
    Safely add a crop with rollback on error.
    
    Args:
        db: Database session
        crop_data: Crop creation data
        
    Returns:
        Created Crop object or raises StorageError on failure.
    """
    try:
        crop = Crop(**crop_data.model_dump())
        db.add(crop)
        db.commit()
        db.refresh(crop)
        logger.info(f"Created crop: {crop.name} (id: {crop.id})")
        return crop
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating crop: {e}")
        raise StorageError(f"Failed to save crop: {e}") from e
```

### Route Layer Error Handling

```python
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

@router.get("/crops/{crop_id}", response_model=CropResponse)
async def get_crop(crop_id: int, db: Session = Depends(get_db)):
    """Get crop by ID with proper error handling"""
    crop = get_crop_safe(db, crop_id)
    if not crop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Crop with id {crop_id} not found"
        )
    return crop

@router.post("/crops/add", response_model=CropResponse, status_code=status.HTTP_201_CREATED)
async def add_crop(crop_data: CropCreate, db: Session = Depends(get_db)):
    """Add new crop with error handling"""
    crop = add_crop_safe(db, crop_data)
    if not crop:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create crop"
        )
    return crop
```

---

## 🗄️ Database Best Practices

### Model Definitions

```python
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.database import Base

class Crop(Base):
    __tablename__ = "crops"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Required fields
    name = Column(String(100), nullable=False, index=True)
    type = Column(String(50), nullable=False)
    plot = Column(String(50), nullable=False)
    
    # Dates
    sowing_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Optional fields
    stage = Column(String(50), default="Sown")
    
    # Foreign keys and relationships
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="crops")
    expenses = relationship("Expense", back_populates="crop", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Crop(id={self.id}, name='{self.name}', type='{self.type}')>"
```

### Query Patterns

```python
from sqlalchemy import desc, func

# Simple query
def get_all_crops(db: Session) -> list[Crop]:
    return db.query(Crop).all()

# Filtered query with ordering
def get_active_crops(db: Session) -> list[Crop]:
    return db.query(Crop)\
        .filter(Crop.stage != "Harvested")\
        .order_by(desc(Crop.created_at))\
        .all()

# Query with limit
def get_recent_crops(db: Session, limit: int = 10) -> list[Crop]:
    return db.query(Crop)\
        .order_by(desc(Crop.created_at))\
        .limit(limit)\
        .all()

# Query with join
def get_crops_with_expenses(db: Session) -> list[Crop]:
    return db.query(Crop)\
        .join(Expense, Crop.id == Expense.crop_id)\
        .distinct()\
        .all()

# Aggregation query
def get_crop_count_by_type(db: Session) -> dict[str, int]:
    results = db.query(Crop.type, func.count(Crop.id))\
        .group_by(Crop.type)\
        .all()
    return {crop_type: count for crop_type, count in results}
```

### Transaction Patterns

```python
def transfer_crop_to_plot(db: Session, crop_id: int, new_plot: str) -> bool:
    """
    Safely transfer crop to new plot with transaction.
    
    Args:
        db: Database session
        crop_id: ID of crop to transfer
        new_plot: New plot identifier
        
    Returns:
        True if successful, False otherwise
    """
    try:
        crop = db.query(Crop).filter(Crop.id == crop_id).first()
        if not crop:
            return False
        
        old_plot = crop.plot
        crop.plot = new_plot
        
        db.commit()
        logger.info(f"Transferred crop {crop_id} from {old_plot} to {new_plot}")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error transferring crop: {str(e)}")
        return False

def bulk_update_crop_stages(db: Session, crop_ids: list[int], new_stage: str) -> int:
    """
    Update multiple crop stages in a single transaction.
    
    Returns:
        Number of crops updated
    """
    try:
        updated = db.query(Crop)\
            .filter(Crop.id.in_(crop_ids))\
            .update({"stage": new_stage}, synchronize_session=False)
        
        db.commit()
        logger.info(f"Updated {updated} crops to stage: {new_stage}")
        return updated
    except Exception as e:
        db.rollback()
        logger.error(f"Error bulk updating crops: {str(e)}")
        return 0
```

---

## 🏢 Service Layer Patterns

### Service Structure

```python
# services/crop_service.py
from sqlalchemy.orm import Session
from models.database import Crop
from models.schemas import CropCreate
import logging

logger = logging.getLogger(__name__)

class CropService:
    """Service layer for crop operations"""
    
    @staticmethod
    def get_all(db: Session) -> list[Crop]:
        """Get all crops"""
        return db.query(Crop).order_by(desc(Crop.created_at)).all()
    
    @staticmethod
    def get_by_id(db: Session, crop_id: int) -> Crop | None:
        """Get crop by ID"""
        return db.query(Crop).filter(Crop.id == crop_id).first()
    
    @staticmethod
    def create(db: Session, crop_data: CropCreate) -> Crop | None:
        """Create new crop"""
        try:
            crop = Crop(**crop_data.model_dump())
            db.add(crop)
            db.commit()
            db.refresh(crop)
            return crop
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating crop: {e}")
            return None
    
    @staticmethod
    def delete(db: Session, crop_id: int) -> bool:
        """Delete crop"""
        try:
            crop = db.query(Crop).filter(Crop.id == crop_id).first()
            if crop:
                db.delete(crop)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting crop: {e}")
            return False
    
    @staticmethod
    def get_summary(db: Session) -> dict[str, Any]:
        """Get crop summary statistics"""
        total = db.query(Crop).count()
        active = db.query(Crop).filter(Crop.stage != "Harvested").count()
        harvested = total - active
        
        return {
            "total_crops": total,
            "active_crops": active,
            "harvested_crops": harvested
        }

# Usage in routes
from services.crop_service import CropService

@router.get("/crops")
async def get_crops(db: Session = Depends(get_db)):
    return CropService.get_all(db)
```

---

## 🛣️ Route Patterns

### RESTful Endpoints

```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

router = APIRouter(prefix="/crops", tags=["crops"])

# GET all
@router.get("/", response_model=list[CropResponse])
async def list_crops(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get list of crops with pagination"""
    crops = CropService.get_all(db)
    return crops[skip : skip + limit]

# GET by ID
@router.get("/{crop_id}", response_model=CropResponse)
async def get_crop(crop_id: int, db: Session = Depends(get_db)):
    """Get crop by ID"""
    crop = CropService.get_by_id(db, crop_id)
    if not crop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Crop with id {crop_id} not found"
        )
    return crop

# POST (create)
@router.post("/", response_model=CropResponse, status_code=status.HTTP_201_CREATED)
async def create_crop(crop_data: CropCreate, db: Session = Depends(get_db)):
    """Create new crop"""
    crop = CropService.create(db, crop_data)
    if not crop:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create crop"
        )
    return crop

# PATCH (partial update)
@router.patch("/{crop_id}/stage", response_model=CropResponse)
async def update_crop_stage(
    crop_id: int,
    stage: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """Update crop growth stage"""
    crop = CropService.get_by_id(db, crop_id)
    if not crop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Crop with id {crop_id} not found"
        )
    
    crop.stage = stage
    db.commit()
    db.refresh(crop)
    return crop

# DELETE
@router.delete("/{crop_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_crop(crop_id: int, db: Session = Depends(get_db)):
    """Delete crop"""
    success = CropService.delete(db, crop_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Crop with id {crop_id} not found"
        )
    return None
```

---

## 💾 Caching Strategies

### Database Cache Pattern

```python
from datetime import datetime, timedelta
from typing import Optional
import json

class WeatherCache(Base):
    __tablename__ = "weather_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), nullable=False, index=True)
    data = Column(String, nullable=False)  # JSON string
    cached_at = Column(DateTime(timezone=True), server_default=func.now())
    
    @property
    def is_stale(self, ttl_minutes: int = 10) -> bool:
        """Check if cache is stale"""
        age = datetime.now() - self.cached_at
        return age > timedelta(minutes=ttl_minutes)
    
    def get_data(self) -> dict:
        """Parse JSON data"""
        return json.loads(self.data)

def get_cached_weather(db: Session, city: str, ttl_minutes: int = 10) -> dict | None:
    """
    Get cached weather data if valid.
    
    Args:
        db: Database session
        city: City name
        ttl_minutes: Cache time-to-live in minutes
        
    Returns:
        Cached data dict or None if stale/missing
    """
    cache = db.query(WeatherCache)\
        .filter(WeatherCache.city == city.lower())\
        .order_by(desc(WeatherCache.cached_at))\
        .first()
    
    if cache and not cache.is_stale(ttl_minutes):
        return cache.get_data()
    
    return None

def set_cached_weather(db: Session, city: str, data: dict) -> None:
    """
    Cache weather data.
    
    Args:
        db: Database session
        city: City name
        data: Weather data dictionary
    """
    try:
        cache = WeatherCache(
            city=city.lower(),
            data=json.dumps(data)
        )
        db.add(cache)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Error caching weather data: {str(e)}")
```

---

## 🔒 Security Best Practices

### Password Hashing

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)
```

### JWT Tokens

```python
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"  # From environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create JWT access token.
    
    Args:
        data: Data to encode in token
        expires_delta: Token expiration time
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict | None:
    """
    Decode and verify JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token data or None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

### Input Validation

```python
from pydantic import BaseModel, Field, validator
import re

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=5, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)
    
    @validator('email')
    def validate_email(cls, v):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid email format')
        return v.lower()
    
    @validator('password')
    def validate_password(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        return v
```

---

## ✅ Code Quality Checklist

### Before Committing:

- [ ] All functions have type hints
- [ ] All functions have docstrings
- [ ] Error handling with try/except
- [ ] Logging for important operations
- [ ] Database operations have rollback on error
- [ ] Pydantic schemas for validation
- [ ] HTTPException with proper status codes
- [ ] Query filters use indexed columns
- [ ] Relationships properly configured
- [ ] Passwords hashed, never stored plain text

---

## 📊 Performance Tips

1. **Use indexes on frequently queried columns**
   ```python
   name = Column(String(100), nullable=False, index=True)
   ```

2. **Limit query results**
   ```python
   crops = db.query(Crop).limit(100).all()
   ```

3. **Use select_related / joinedload for relationships**
   ```python
   from sqlalchemy.orm import joinedload
   crops = db.query(Crop).options(joinedload(Crop.expenses)).all()
   ```

4. **Cache expensive operations**
   ```python
   @lru_cache(maxsize=128)
   def get_crop_types() -> List[str]:
       return ["Wheat", "Rice", "Corn"]
   ```

5. **Use bulk operations for multiple updates**
   ```python
   db.bulk_update_mappings(Crop, [
       {"id": 1, "stage": "Harvested"},
       {"id": 2, "stage": "Harvested"}
   ])
   ```

---

**Guide Version:** 1.0  
**Last Updated:** November 20, 2025
