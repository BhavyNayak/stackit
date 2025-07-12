from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
from sqlalchemy import text

from routes import user_routes, question_routes, answer_routes
from utils.database_helper import engine, async_engine
from models import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        async with async_engine.begin() as conn:
            # Drop existing enum types to avoid conflicts
            await conn.execute(text("DROP TYPE IF EXISTS usertypeenum CASCADE"))
            await conn.execute(text("DROP TYPE IF EXISTS user_role CASCADE"))
            # Create tables
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"⚠️ Database initialization warning: {e}")
        # Try to create tables anyway
        try:
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            print("✅ Tables created successfully")
        except Exception as e2:
            print(f"❌ Database initialization failed: {e2}")
    
    yield
    # Shutdown
    await async_engine.dispose()

app = FastAPI(
    title="StackIt - Q&A Platform API",
    description="A comprehensive Q&A platform with JWT authentication and CRUD operations",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "message": exc.detail,
            "data": None
        }
    )

# Include routers
app.include_router(user_routes.router, prefix="/api/users", tags=["Users"])
app.include_router(question_routes.router, prefix="/api/questions", tags=["Questions"])
app.include_router(answer_routes.router, prefix="/api/answers", tags=["Answers"])

@app.get("/")
def root():
    return {
        "status": 200,
        "message": "Welcome to StackIt API",
        "data": {
            "version": "1.0.0",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": 200,
        "message": "API is healthy",
        "data": {
            "status": "running"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )