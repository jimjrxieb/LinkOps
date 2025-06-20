#!/usr/bin/env python3
"""
Password generator script for LinkOps Core
Generates secure passwords for database and pgAdmin
"""

import secrets
import string
import os

def generate_secure_password(length=16):
    """Generate a secure random password"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)
                and any(c in "!@#$%^&*" for c in password)):
            return password

def generate_secret_key(length=32):
    """Generate a secure secret key"""
    return secrets.token_urlsafe(length)

if __name__ == "__main__":
    print("🔐 LinkOps Core - Secure Password Generator")
    print("=" * 50)
    
    # Generate passwords
    db_password = generate_secure_password(20)
    pgadmin_password = generate_secure_password(16)
    secret_key = generate_secret_key(32)
    
    print("\n📋 Generated Secure Credentials:")
    print("-" * 30)
    print(f"Database Password: {db_password}")
    print(f"pgAdmin Password: {pgadmin_password}")
    print(f"Secret Key: {secret_key}")
    
    print("\n📝 Add these to your .env file:")
    print("-" * 30)
    print(f"POSTGRES_PASSWORD={db_password}")
    print(f"PGADMIN_DEFAULT_PASSWORD={pgadmin_password}")
    print(f"SECRET_KEY={secret_key}")
    print(f"DATABASE_URL=postgresql://linkops:{db_password}@localhost:5432/linkops")
    
    print("\n⚠️  Security Notes:")
    print("- Keep your .env file secure and never commit it to version control")
    print("- Use different passwords for production environments")
    print("- Regularly rotate passwords in production")
    print("- Consider using a secrets management service for production") 