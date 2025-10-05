from typing import Optional
from app.repository import BaseRepository, db
from app.auth.model import OTP
from app.config import logger

class OTPRepository(BaseRepository):
    def __init__(self):
        super().__init__(OTP.table_name)

    def get_by_user_and_code(self, user_id: int, code: str):
        """Get activation by user ID and code (valid if not expired)."""
        query = f"""
        SELECT * FROM {self.table_name}
        WHERE user_id={int(user_id)} AND code='{str(code)}' AND expires_at > NOW()
        """
        try:
            result = db.fetchOne(query)
            return result if result else None
        except Exception as e:
            logger.error(f"DB error in get_by_user_and_code: {e}")
            return None

    def get_by_email_and_purpose(self, email: str, purpose: str):
        query = f"""
        SELECT * FROM {self.table_name}
        WHERE email='{email}' AND purpose='{purpose}'
        ORDER BY created_at DESC
        LIMIT 1
        """
        try:
            result = db.fetchOne(query)
            return result if result else None
        except Exception as e:
            logger.error(f"DB error in get_by_email_and_purpose: {e}")
            return None

    def delete_by_email_and_purpose(self, email: str, purpose: str):
        query = f"""
        DELETE FROM {self.table_name}
        WHERE email='{email}' AND purpose='{purpose}'
        """
        try:
            return db.execute(query)
        except Exception as e:
            logger.error(f"DB error in delete_by_email_and_purpose: {e}")
            return None
