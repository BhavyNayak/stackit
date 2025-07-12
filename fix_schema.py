#!/usr/bin/env python3
"""
Fix Database Schema Script
This script adds the missing role column to the users table
"""

import asyncio
from sqlalchemy import text
from utils.database_helper import async_engine

async def fix_schema():
    """Add the missing role column to users table"""
    
    async with async_engine.begin() as conn:
        # Check if role column exists
        result = await conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name = 'role'
        """))
        
        if result.fetchone():
            print("✅ Role column already exists")
        else:
            print("🔧 Adding role column to users table...")
            # Add the role column with default value
            await conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN role user_role NOT NULL DEFAULT 'user'
            """))
            print("✅ Role column added successfully")
        
        # Verify the column was added
        result = await conn.execute(text("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name = 'role'
        """))
        
        column_info = result.fetchone()
        if column_info:
            print(f"✅ Role column verified: {column_info[0]} ({column_info[1]}) - default: {column_info[3]}")

if __name__ == "__main__":
    print("🔧 Fixing database schema...")
    asyncio.run(fix_schema())
    print("✅ Schema fix completed!") 