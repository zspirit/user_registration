from typing import Optional
from app.repository import BaseRepository, db
from app.users.model import User

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User.table_name)
        
    def get_all(self):
        """Get all users."""
        query = f"""
        SELECT * FROM {self.table_name}
        """
        results = db.execute(query, fetch=True)
        return results if results else None
    
    def get_by_email(self, email: str):
        """Get user by email."""
        query = f"""
        SELECT * FROM {self.table_name}
        WHERE email=%s
        """
        
        results = db.execute(query, (email,), fetch=True)
        return results[0] if results else None
    
    def update_user(self, user_id: str, update_data: dict) -> Optional[User]:
        """Update user information in the database."""
        # Get the current user
        user = self.get_by_id(user_id)
        if not user:
            return None

        # Prepare the fields and values to update
        fields = []
        values = []
        for key, value in update_data.items():
            if hasattr(user, key) and value is not None:
                fields.append(f"{key} = %s")
                values.append(value)
                # Also update the Pydantic model instance
                setattr(user, key, value)

        if not fields:
            # Nothing to update
            return user

        # Build the UPDATE SQL query
        query = f"""
            UPDATE {self.table_name}
            SET {', '.join(fields)}
            WHERE id = %s
            RETURNING *
        """
        values.append(user_id)  # add user_id for WHERE clause

        # Execute the query and fetch the updated user
        updated_rows = db.execute(query, tuple(values), fetch=True)
        if updated_rows:
            updated_user_data = updated_rows[0]
            # Return a new User instance from the updated data
            return User(**updated_user_data)
        
        return None
