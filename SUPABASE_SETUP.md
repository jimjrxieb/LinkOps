# 🔗 LinkOps Core - Supabase Setup Guide

This guide will help you configure LinkOps Core to work with Supabase instead of a local PostgreSQL database.

## 📋 Prerequisites

1. **Supabase Account**: Sign up at [supabase.com](https://supabase.com)
2. **Python Dependencies**: Ensure you have the required packages installed
3. **Environment Variables**: Set up your `.env` file

## 🚀 Step-by-Step Setup

### 1. Create Your `.env` File

Create a `.env` file in your project root with the following content:

```bash
# Application Settings
APP_NAME=LinkOps Core
DEBUG=true
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO

# CORS Settings
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:8080"]
ALLOWED_HOSTS=["localhost","127.0.0.1"]

# Supabase Database Settings
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# Security Settings
SECRET_KEY=your-super-secret-key-change-this-in-production-2024
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Storage Settings
SCREENSHOTS_DIR=./screenshots
LOGS_DIR=./logs

# Monitoring and Logging
ENABLE_METRICS=true
METRICS_PORT=9090
LOG_FORMAT=json
```

### 2. Get Your Supabase Database URL

1. Go to your Supabase project dashboard
2. Navigate to **Settings** → **Database**
3. Copy the **Connection string** (URI format)
4. Replace `[YOUR-PASSWORD]` and `[YOUR-PROJECT-REF]` in your `.env` file

### 3. Test Your Connection

Run the connection test script:

```bash
python scripts/test_supabase_connection.py
```

This will verify that:
- Your `.env` file is loaded correctly
- The DATABASE_URL is valid
- You can connect to Supabase
- No tables exist yet (ready for migrations)

### 4. Run Database Migrations

Create and apply the database schema:

```bash
# Generate a new migration (if needed)
alembic revision --autogenerate -m "Initial schema"

# Apply migrations to Supabase
alembic upgrade head
```

### 5. Verify Tables Created

Check your Supabase dashboard:
1. Go to **Table Editor**
2. You should see tables: `orbs`, `runes`, `logs`, etc.

## 🔧 Configuration Files Updated

The following files have been updated to support Supabase:

- ✅ `migrations/env.py` - Now loads `.env` and uses DATABASE_URL
- ✅ `main.py` - Added `.env` loading
- ✅ `core/db/database.py` - Already had `.env` loading
- ✅ `docker-compose.yml` - Uses environment variables
- ✅ `config/settings.py` - Updated with better descriptions

## 🛠️ Troubleshooting

### Connection Issues

If you get connection errors:

1. **Check your DATABASE_URL format**:
   ```
   postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
   ```

2. **Verify IP whitelist**: Add your IP to Supabase's allowed list

3. **Check credentials**: Ensure password is correct

4. **Test with psql**:
   ```bash
   psql "postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres"
   ```

### Migration Issues

If migrations fail:

1. **Check table permissions**: Ensure your user has CREATE TABLE permissions
2. **Verify schema**: Make sure you're using the `public` schema
3. **Check for conflicts**: Drop existing tables if they conflict

## 🔒 Security Best Practices

1. **Never commit `.env` files** to version control
2. **Use strong passwords** for database access
3. **Rotate credentials** regularly
4. **Use environment-specific** configurations
5. **Enable Row Level Security** in Supabase for production

## 📊 Monitoring

After setup, you can monitor your database:

1. **Supabase Dashboard**: Real-time metrics and logs
2. **Table Editor**: View and edit data directly
3. **SQL Editor**: Run custom queries
4. **Logs**: Monitor application logs

## 🎉 Next Steps

Once your Supabase connection is working:

1. **Start your application**: `python main.py`
2. **Test the API**: Visit `http://localhost:8000/docs`
3. **Create some data**: Use the GUI or API endpoints
4. **Monitor performance**: Check Supabase dashboard

---

**Need help?** Check the logs or run the test script again! 