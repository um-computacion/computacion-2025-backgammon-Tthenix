# Dockerfile for Redis Backgammon Game
FROM redis:7-alpine

# Set working directory
WORKDIR /data

# Create a custom Redis configuration
COPY redis.conf /usr/local/etc/redis/redis.conf

# Expose Redis port
EXPOSE 6379

# Set default command
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]

# Add labels for documentation
LABEL maintainer="Backgammon Game Team"
LABEL description="Redis server for Backgammon game persistence"
LABEL version="1.0"
