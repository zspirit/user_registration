from typing import List, Optional, TypeVar, Generic, Dict, Any
from pydantic import BaseModel
from datetime import datetime, timezone
from app.config import logger

T = TypeVar("T")

# Database
class Database:
    def __init__(self):
        self.conn = None

    def connect(self):
        if self.conn is None:
            try:
                import psycopg2
                from psycopg2.extras import RealDictCursor
                from app.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

                self.conn = psycopg2.connect(
                    host=DB_HOST,
                    port=DB_PORT,
                    database=DB_NAME,
                    user=DB_USER,
                    password=DB_PASSWORD
                )
                self.conn.autocommit = True
                logger.info("Database connection established.")
            except Exception as e:
                logger.error(f"Failed to connect to DB: {e}")
                raise
        return self.conn

    def execute(self, query: str):
        conn = self.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(query)
                logger.debug(f"Executed query: {query}")
        except Exception as e:
            logger.error(f"DB Error executing query: {query} | Error: {e}")
            raise

    def fetchAll(self, query: str) -> List[Dict]:
        conn = self.connect()
        try:
            from psycopg2.extras import RealDictCursor
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                results = cur.fetchall()
                logger.debug(f"Executed query: {query} | Fetched all: {results}")
                return results
        except Exception as e:
            logger.error(f"DB Error executing query: {query} | Error: {e}")
            raise

    def fetchOne(self, query: str) -> Optional[Dict]:
        conn = self.connect()
        try:
            from psycopg2.extras import RealDictCursor
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                result = cur.fetchone()
                logger.debug(f"Executed query: {query} | Fetched one: {result}")
                return result
        except Exception as e:
            logger.error(f"DB Error executing query: {query} | Error: {e}")
            raise

db = Database()

# Base Repository
class BaseRepository(Generic[T]):
    def __init__(self, table_name: str):
        self.table_name = table_name

    def get_all(self) -> List[T]:
        query = f"SELECT * FROM {self.table_name}"
        logger.info(f"Fetching all rows from {self.table_name}")
        results = db.fetchAll(query)
        return results if results else []

    def get_by_id(self, entity_id) -> Optional[T]:
        query = f"SELECT * FROM {self.table_name} WHERE id={entity_id}"
        logger.info(f"Fetching from {self.table_name} where id={entity_id}")
        return db.fetchOne(query)

    def insert(self, data: BaseModel) -> int:
        data_dict = data.model_dump(exclude_unset=True, exclude_none=True)
        data_dict.setdefault("created_at", datetime.now(timezone.utc))

        keys = ", ".join(data_dict.keys())
        values = ", ".join([f"'{v}'" if not isinstance(v, (int, float)) else str(v) for v in data_dict.values()])

        query = f"INSERT INTO {self.table_name} ({keys}) VALUES ({values}) RETURNING id"
        logger.info(f"Inserting into {self.table_name}")
        result = db.fetchOne(query)
        new_id = result["id"]
        logger.info(f"Inserted new row with id={new_id}")
        return new_id

    def update(self, entity_id, data: Dict[str, Any]):
        set_clause = ", ".join([f"{k}='{v}'" if not isinstance(v, (int, float)) else f"{k}={v}" for k, v in data.items()])
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE id={entity_id}"
        logger.info(f"Updating {self.table_name} id={entity_id}")
        db.execute(query)

    def delete_by_id(self, entity_id):
        query = f"DELETE FROM {self.table_name} WHERE id={entity_id}"
        logger.info(f"Deleting from {self.table_name} id={entity_id}")
        db.execute(query)

    def delete(self, conditions: Dict[str, Any]):
        where_clause = " AND ".join([f"{k}='{v}'" if not isinstance(v, (int, float)) else f"{k}={v}" for k, v in conditions.items()])
        query = f"DELETE FROM {self.table_name} WHERE {where_clause}"
        logger.info(f"Deleting from {self.table_name} where {conditions}")
        db.execute(query)
