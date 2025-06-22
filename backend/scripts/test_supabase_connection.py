#!/usr/bin/env python3
"""
Test Supabase connection and environment variables
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

def test_connection():
    """Test database connection"""
    print("🔍 Testing Supabase Connection")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    # Get database URL
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        print("   Make sure your .env file exists and contains DATABASE_URL")
        return False
    
    print(f"📡 Database URL: {database_url[:50]}...")
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Connection successful!")
            print(f"📊 Database version: {version}")
            
            # Test if tables exist
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = [row[0] for row in result.fetchall()]
            
            if tables:
                print(f"📋 Existing tables: {', '.join(tables)}")
            else:
                print("📋 No tables found - ready for migrations")
                
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check your .env file has the correct DATABASE_URL")
        print("2. Verify your Supabase credentials")
        print("3. Ensure your IP is whitelisted in Supabase")
        print("4. Check if the database exists")
        return False

if __name__ == "__main__":
    test_connection() 