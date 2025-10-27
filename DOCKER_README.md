# Redis Docker Setup for Backgammon Game

This directory contains Docker configuration files to run Redis for the Backgammon game persistence functionality.

## Files Overview

- `Dockerfile` - Custom Redis Docker image configuration
- `docker-compose.yml` - Docker Compose configuration for easy management
- `redis.conf` - Redis server configuration file
- `redis-manager.sh` - Linux/Mac management script
- `redis-manager.bat` - Windows management script

## Quick Start

### Prerequisites

1. **Docker Desktop** must be installed and running
2. **Docker Compose** (usually included with Docker Desktop)

### Starting Redis

#### Option 1: Using Simple Docker Compose (Recommended)

```bash
# Start Redis (uses official Redis image)
docker-compose -f docker-compose-simple.yml up -d

# Check status
docker-compose -f docker-compose-simple.yml ps

# Stop Redis
docker-compose -f docker-compose-simple.yml down
```

#### Option 2: Using Custom Docker Compose

```bash
# Start Redis (builds custom image)
docker-compose up -d

# Check status
docker-compose ps

# Stop Redis
docker-compose down
```

#### Option 3: Using Management Scripts

**On Windows:**

```cmd
# Start Redis
redis-manager.bat start

# Check status
redis-manager.bat status

# Stop Redis
redis-manager.bat stop
```

**On Linux/Mac:**

```bash
# Make script executable
chmod +x redis-manager.sh

# Start Redis
./redis-manager.sh start

# Check status
./redis-manager.sh status

# Stop Redis
./redis-manager.sh stop
```

## Management Commands

### Using Docker Compose

```bash
# Start Redis in background
docker-compose up -d

# View logs
docker-compose logs -f redis

# Stop Redis
docker-compose down

# Restart Redis
docker-compose restart

# Check status
docker-compose ps

# Connect to Redis CLI
docker-compose exec redis redis-cli
```

### Using Management Scripts

```bash
# Available commands:
redis-manager.bat start     # Start Redis
redis-manager.bat stop      # Stop Redis
redis-manager.bat restart   # Restart Redis
redis-manager.bat status    # Show status
redis-manager.bat logs      # Show logs
redis-manager.bat cli       # Connect to CLI
redis-manager.bat help      # Show help
```

## Redis Configuration

The Redis server is configured with the following settings:

- **Port**: 6379 (default Redis port)
- **Memory Limit**: 256MB
- **Persistence**: RDB snapshots + AOF logging
- **Security**: No password (development mode)
- **Data Directory**: `/data` (persisted via Docker volume)

## Testing Redis Connection

### From Command Line

```bash
# Test connection
docker-compose exec redis redis-cli ping
# Should return: PONG

# Set a test value
docker-compose exec redis redis-cli set test "Hello Redis"

# Get the test value
docker-compose exec redis redis-cli get test
# Should return: Hello Redis
```

### From Python Application

The Backgammon game will automatically detect Redis availability:

```python
# If Redis is running, you'll see:
# "Redis connection successful"

# If Redis is not running, you'll see:
# "Redis not available: [error]"
# "Using file-based persistence instead"
```

## Data Persistence

Redis data is persisted using Docker volumes:

- **Volume Name**: `redis_data`
- **Location**: Docker managed volume
- **Backup**: Data survives container restarts
- **Cleanup**: Run `docker-compose down -v` to remove data

## Troubleshooting

### Redis Not Starting

1. **Check Docker is running:**

   ```bash
   docker info
   ```

2. **Check port availability:**

   ```bash
   netstat -an | findstr 6379
   ```

3. **View Redis logs:**
   ```bash
   docker-compose logs redis
   ```

### Connection Issues

1. **Test Redis connectivity:**

   ```bash
   docker-compose exec redis redis-cli ping
   ```

2. **Check container status:**

   ```bash
   docker-compose ps
   ```

3. **Restart Redis:**
   ```bash
   docker-compose restart
   ```

### Performance Issues

1. **Monitor Redis memory:**

   ```bash
   docker-compose exec redis redis-cli info memory
   ```

2. **Check Redis stats:**
   ```bash
   docker-compose exec redis redis-cli info stats
   ```

## Development Notes

- Redis runs in development mode (no authentication)
- Data is persisted to disk for durability
- Memory usage is limited to 256MB
- Logs are available via `docker-compose logs`

## Production Considerations

For production deployment, consider:

1. **Security**: Enable Redis authentication
2. **Memory**: Increase memory limits based on usage
3. **Monitoring**: Add Redis monitoring tools
4. **Backup**: Implement regular backup strategy
5. **Networking**: Use proper network security

## Fallback Behavior

If Redis is not available, the Backgammon game will automatically fall back to file-based persistence, saving games as JSON files in the `saved_games/` directory.
