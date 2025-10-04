from app.auth.model import OTP
from app.repository import BaseRepository, db

class OTPRepository(BaseRepository):
    def __init__(self):
        super().__init__(OTP.table_name)
        
    def get_by_user_and_code(self, user_id: int, code: str):
        """Get activation by user ID and code (valid if not expired)."""
        query = f"""
        SELECT * FROM {self.table_name}
        WHERE user_id=%s AND code=%s AND expires_at > NOW()
        """
        results = db.execute(query, (user_id, code), fetch=True)
        return results[0] if results else None
    
    def get_by_email_and_purpose(self, email: int, purpose: str):
        query = f"""
        SELECT * FROM {self.table_name}
        WHERE email = %s AND purpose = %s
        ORDER BY created_at DESC
        LIMIT 1
        """
        results = db.execute(query, (email, purpose), fetch=True)
        return results[0] if results else None
    
    def delete_by_email_and_purpose(self, email: str, purpose: str):
        query = f"""
            DELETE FROM {self.table_name}
            WHERE email = %s AND purpose = %s
        """
        return db.execute(query, (email, purpose))

