from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import asyncpg
from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

async def lifespan(app: FastAPI):
    """Connect to the PostgreSQL database on startup."""
    app.state.db = await asyncpg.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    print("Connected to PostgreSQL")
    
    yield  # Control is handed to the app

    # Shutdown: close the connection
    await app.state.db.close()
    print("PostgreSQL connection closed")


app = FastAPI(
    title="User registration API",
    description="User registration Management System with Authentication",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(users_router)

# Serve static pytest report
app.mount("/report", StaticFiles(directory=".", html=True), name="report")

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "User registration CMS API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.get("/test-db")
async def test_db_connection():
    """
    Test PostgreSQL connection by fetching the current timestamp.
    Returns a simple success message if the connection works.
    """
    try:
        row = await app.state.db.fetchrow("SELECT NOW() AS current_time;")
        return {
            "status": "success",
            "message": "Connection to PostgreSQL is working",
            "current_time": str(row["current_time"])
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to connect to PostgreSQL: {e}"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
