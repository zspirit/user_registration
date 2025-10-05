from typing import Optional
from app.repository import BaseRepository, db
from app.users.model import User
from app.config import logger

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User.table_name)

    def get_all(self):
        """Get all users."""
        query = f"SELECT * FROM {self.table_name}"
        logger.info(f"Fetching all users from {self.table_name}")
        try:
            results = db.fetchAll(query)
            logger.debug(f"Fetched users: {results}")
            return results if results else []
        except Exception as e:
            logger.error(f"Error fetching all users: {e}")
            return []

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        query = f"SELECT * FROM {self.table_name} WHERE email='{email}'"
        logger.info(f"Fetching user by email: {email}")
        try:
            result = db.fetchOne(query)
            logger.debug(f"Fetched user: {result}")
            return User(**result) if result else None
        except Exception as e:
            logger.error(f"Error fetching user by email {email}: {e}")
            return None

    def update_user(self, user_id: str, update_data: dict, allow_is_active=False) -> Optional[User]:
        """
        Update user information.
        Only allows certain fields to be updated. If allow_is_active=True, can update is_active.
        """
        ALLOWED_UPDATE_FIELDS = {"firstname", "lastname", "email", "password_hash"}
        if allow_is_active:
            ALLOWED_UPDATE_FIELDS.add("is_active")

        # Get current user data
        user_data = self.get_by_id(user_id)
        if not user_data:
            return None

        # Build SET clause safely
        set_clause_parts = []
        for k, v in update_data.items():
            if k in ALLOWED_UPDATE_FIELDS and v is not None:
                # If string, wrap with single quotes
                if isinstance(v, str):
                    safe_value = v.replace("'", "''")  # escape single quotes
                    set_clause_parts.append(f"{k}='{safe_value}'")
                elif isinstance(v, bool):
                    set_clause_parts.append(f"{k}={'TRUE' if v else 'FALSE'}")
                else:
                    set_clause_parts.append(f"{k}={v}")

        if not set_clause_parts:
            # Nothing to update
            return User(**user_data)

        set_clause = ", ".join(set_clause_parts)
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE id={user_id} RETURNING *"

        try:
            updated_user_data = db.fetchOne(query)  # no params
            if updated_user_data:
                return User(**updated_user_data)
            return None
        except Exception as e:
            logger.error(f"Error updating user id={user_id}: {e}")
            return None



