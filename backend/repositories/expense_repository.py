"""
Expense Repository
Data access layer for Expense operations
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from backend.models.database import Expense
from backend.repositories.base import BaseRepository


class ExpenseRepository(BaseRepository[Expense]):
    """Repository for Expense data access"""
    
    def __init__(self):
        super().__init__(Expense)
    
    def get_by_user(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Expense]:
        """Get all expenses for a specific user"""
        return db.query(Expense)\
            .filter(Expense.user_id == user_id)\
            .order_by(Expense.date.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    def get_by_id_and_user(self, db: Session, expense_id: int, user_id: int) -> Optional[Expense]:
        """Get expense by ID and user_id"""
        return db.query(Expense)\
            .filter(Expense.id == expense_id, Expense.user_id == user_id)\
            .first()
    
    def get_by_type(self, db: Session, user_id: int, expense_type: str) -> List[Expense]:
        """Get expenses by type (income/expense)"""
        return db.query(Expense)\
            .filter(Expense.user_id == user_id, Expense.type == expense_type)\
            .order_by(Expense.date.desc())\
            .all()
    
    def get_by_category(self, db: Session, user_id: int, category: str) -> List[Expense]:
        """Get expenses by category"""
        return db.query(Expense)\
            .filter(Expense.user_id == user_id, Expense.category == category)\
            .order_by(Expense.date.desc())\
            .all()
    
    def get_summary(self, db: Session, user_id: int) -> dict:
        """Get expense summary for a user"""
        total_income = db.query(func.sum(Expense.amount))\
            .filter(Expense.user_id == user_id, Expense.type == 'income')\
            .scalar() or 0
        
        total_expense = db.query(func.sum(Expense.amount))\
            .filter(Expense.user_id == user_id, Expense.type == 'expense')\
            .scalar() or 0
        
        return {
            'total_income': float(total_income),
            'total_expense': float(total_expense),
            'net': float(total_income - total_expense)
        }
    
    def get_monthly_summary(self, db: Session, user_id: int, year: int, month: int) -> dict:
        """Get monthly expense summary"""
        total_income = db.query(func.sum(Expense.amount))\
            .filter(
                Expense.user_id == user_id,
                Expense.type == 'income',
                extract('year', Expense.date) == year,
                extract('month', Expense.date) == month
            ).scalar() or 0
        
        total_expense = db.query(func.sum(Expense.amount))\
            .filter(
                Expense.user_id == user_id,
                Expense.type == 'expense',
                extract('year', Expense.date) == year,
                extract('month', Expense.date) == month
            ).scalar() or 0
        
        return {
            'month': month,
            'year': year,
            'total_income': float(total_income),
            'total_expense': float(total_expense),
            'net': float(total_income - total_expense)
        }


# Global instance
expense_repository = ExpenseRepository()
