#!/usr/bin/env python3
"""
Database Migration Script for StackIt
This script handles the enum type mismatch and creates tables properly
"""

import asyncio
from sqlalchemy import text
from utils.database_helper import async_engine
from models import Base

async def migrate_database():
    """Migrate the database to handle enum types properly"""
    
    async with async_engine.begin() as conn:
        # Drop existing tables if they exist
        await conn.execute(text("DROP TABLE IF EXISTS answers CASCADE"))
        await conn.execute(text("DROP TABLE IF EXISTS questions CASCADE"))
        await conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
        
        # Drop existing enum types if they exist
        await conn.execute(text("DROP TYPE IF EXISTS usertypeenum CASCADE"))
        await conn.execute(text("DROP TYPE IF EXISTS user_role CASCADE"))
        
        print("✅ Dropped existing tables and enum types")
    
    # Create tables with proper enum types
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Created all tables with proper enum types")

if __name__ == "__main__":
    print("🔄 Starting database migration...")
    asyncio.run(migrate_database())
    print("✅ Database migration completed successfully!") 