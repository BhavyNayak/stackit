#!/usr/bin/env python3
"""
Check Database Schema Script
This script checks the actual database schema to see what columns exist
"""

import asyncio
from sqlalchemy import text
from utils.database_helper import async_engine

async def check_schema():
    """Check the actual database schema"""
    
    async with async_engine.begin() as conn:
        # Check if users table exists and what columns it has
        result = await conn.execute(text("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'users' 
            ORDER BY ordinal_position
        """))
        
        columns = result.fetchall()
        print("📋 Users table columns:")
        for column in columns:
            print(f"  - {column[0]}: {column[1]} (nullable: {column[2]})")
        
        # Check if user_role enum exists
        result = await conn.execute(text("""
            SELECT typname, typarray 
            FROM pg_type 
            WHERE typname = 'user_role'
        """))
        
        enum_result = result.fetchone()
        if enum_result:
            print(f"✅ user_role enum exists: {enum_result[0]}")
        else:
            print("❌ user_role enum does not exist")
        
        # Check enum values
        result = await conn.execute(text("""
            SELECT enumlabel 
            FROM pg_enum 
            WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname = 'user_role')
            ORDER BY enumsortorder
        """))
        
        enum_values = result.fetchall()
        print("📋 user_role enum values:")
        for value in enum_values:
            print(f"  - {value[0]}")

if __name__ == "__main__":
    print("🔍 Checking database schema...")
    asyncio.run(check_schema())
    print("✅ Schema check completed!") 