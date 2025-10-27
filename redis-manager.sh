#!/bin/bash
# Redis Management Script for Backgammon Game

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker Desktop."
        exit 1
    fi
    print_success "Docker is running"
}

# Function to start Redis
start_redis() {
    print_status "Starting Redis container..."
    docker-compose up -d
    print_success "Redis container started"
    
    # Wait for Redis to be ready
    print_status "Waiting for Redis to be ready..."
    sleep 5
    
    # Test connection
    if docker-compose exec redis redis-cli ping | grep -q "PONG"; then
        print_success "Redis is ready and responding to ping"
    else
        print_error "Redis is not responding"
        exit 1
    fi
}

# Function to stop Redis
stop_redis() {
    print_status "Stopping Redis container..."
    docker-compose down
    print_success "Redis container stopped"
}

# Function to restart Redis
restart_redis() {
    print_status "Restarting Redis container..."
    docker-compose restart
    print_success "Redis container restarted"
}

# Function to show Redis status
show_status() {
    print_status "Redis container status:"
    docker-compose ps
    
    if docker-compose ps | grep -q "Up"; then
        print_status "Testing Redis connection..."
        if docker-compose exec redis redis-cli ping | grep -q "PONG"; then
            print_success "Redis is running and healthy"
        else
            print_warning "Redis container is running but not responding"
        fi
    else
        print_warning "Redis container is not running"
    fi
}

# Function to show Redis logs
show_logs() {
    print_status "Showing Redis logs (press Ctrl+C to exit):"
    docker-compose logs -f redis
}

# Function to connect to Redis CLI
connect_cli() {
    print_status "Connecting to Redis CLI..."
    docker-compose exec redis redis-cli
}

# Function to show help
show_help() {
    echo "Redis Management Script for Backgammon Game"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start     Start Redis container"
    echo "  stop      Stop Redis container"
    echo "  restart   Restart Redis container"
    echo "  status    Show Redis container status"
    echo "  logs      Show Redis logs"
    echo "  cli       Connect to Redis CLI"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start    # Start Redis"
    echo "  $0 status   # Check if Redis is running"
    echo "  $0 cli      # Open Redis command line interface"
}

# Main script logic
case "${1:-help}" in
    start)
        check_docker
        start_redis
        ;;
    stop)
        check_docker
        stop_redis
        ;;
    restart)
        check_docker
        restart_redis
        ;;
    status)
        check_docker
        show_status
        ;;
    logs)
        check_docker
        show_logs
        ;;
    cli)
        check_docker
        connect_cli
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
