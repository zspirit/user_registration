from typing import List, Optional, TypeVar, Generic, Dict, Any
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from app.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from datetime import datetime, timezone

T = TypeVar("T")

class Database:
    def __init__(self):
        self.conn = None  # don't connect yet

    def connect(self):
        if self.conn is None:
            self.conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            self.conn.autocommit = True
        return self.conn

    def execute(self, query: str, params=None, fetch=False):
        conn = self.connect() 
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            if fetch:
                return cur.fetchall()
            return None

db = Database()


class BaseRepository(Generic[T]):
    def __init__(self, table_name: str):
        self.table_name = table_name

    def get_all(self) -> List[T]:
        """Get all entities."""
        query = f"SELECT * FROM {self.table_name}"
        return db.execute(query, fetch=True)

    def get_by_id(self, entity_id) -> Optional[T]:
        """Get entity by ID."""
        query = f"SELECT * FROM {self.table_name} WHERE id=%s"
        results = db.execute(query, (entity_id,), fetch=True)
        return results[0] if results else None

    def add(self, data: BaseModel) -> int:
        """Insert a new entity. Returns new id (Postgres)."""
        # Safely dump model → dict
        data = data.model_dump(exclude_unset=True, exclude_none=True)

        # Ensure created_at exists
        data.setdefault("created_at", datetime.now(timezone.utc))

        keys = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        values = tuple(data.values())

        query = f"INSERT INTO {self.table_name} ({keys}) VALUES ({placeholders}) RETURNING id"
        result = db.execute(query, values, fetch=True)
        return result[0]["id"]


    def update(self, entity_id, data: Dict[str, Any]):
        """Update an entity by ID."""
        set_clause = ", ".join([f"{k}=%s" for k in data.keys()])
        values = tuple(data.values()) + (entity_id,)
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE id=%s"
        db.execute(query, values)

    def delete_by_id(self, entity_id):
        """Delete an entity by ID."""
        query = f"DELETE FROM {self.table_name} WHERE id=%s"
        db.execute(query, (entity_id,))

    def delete(self, conditions: Dict[str, Any]):
        """Delete entities matching conditions."""
        where_clause = " AND ".join([f"{k}=%s" for k in conditions.keys()])
        values = tuple(conditions.values())
        query = f"DELETE FROM {self.table_name} WHERE {where_clause}"
        db.execute(query, values)
