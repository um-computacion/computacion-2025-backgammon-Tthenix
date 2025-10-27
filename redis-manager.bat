@echo off
REM Redis Management Script for Backgammon Game (Windows)

setlocal enabledelayedexpansion

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running. Please start Docker Desktop.
    exit /b 1
)
echo [SUCCESS] Docker is running

REM Parse command line argument
set COMMAND=%1
if "%COMMAND%"=="" set COMMAND=help

if "%COMMAND%"=="start" goto start_redis
if "%COMMAND%"=="stop" goto stop_redis
if "%COMMAND%"=="restart" goto restart_redis
if "%COMMAND%"=="status" goto show_status
if "%COMMAND%"=="logs" goto show_logs
if "%COMMAND%"=="cli" goto connect_cli
if "%COMMAND%"=="help" goto show_help
goto unknown_command

:start_redis
echo [INFO] Starting Redis container...
docker-compose -f docker-compose-simple.yml up -d
if %errorlevel% neq 0 (
    echo [ERROR] Failed to start Redis container
    exit /b 1
)
echo [SUCCESS] Redis container started

echo [INFO] Waiting for Redis to be ready...
timeout /t 5 /nobreak >nul

echo [INFO] Testing Redis connection...
docker-compose -f docker-compose-simple.yml exec redis redis-cli ping | findstr "PONG" >nul
if %errorlevel% equ 0 (
    echo [SUCCESS] Redis is ready and responding to ping
) else (
    echo [ERROR] Redis is not responding
    exit /b 1
)
goto end

:stop_redis
echo [INFO] Stopping Redis container...
docker-compose -f docker-compose-simple.yml down
if %errorlevel% neq 0 (
    echo [ERROR] Failed to stop Redis container
    exit /b 1
)
echo [SUCCESS] Redis container stopped
goto end

:restart_redis
echo [INFO] Restarting Redis container...
docker-compose -f docker-compose-simple.yml restart
if %errorlevel% neq 0 (
    echo [ERROR] Failed to restart Redis container
    exit /b 1
)
echo [SUCCESS] Redis container restarted
goto end

:show_status
echo [INFO] Redis container status:
docker-compose -f docker-compose-simple.yml ps

docker-compose -f docker-compose-simple.yml ps | findstr "Up" >nul
if %errorlevel% equ 0 (
    echo [INFO] Testing Redis connection...
    docker-compose -f docker-compose-simple.yml exec redis redis-cli ping | findstr "PONG" >nul
    if %errorlevel% equ 0 (
        echo [SUCCESS] Redis is running and healthy
    ) else (
        echo [WARNING] Redis container is running but not responding
    )
) else (
    echo [WARNING] Redis container is not running
)
goto end

:show_logs
echo [INFO] Showing Redis logs (press Ctrl+C to exit):
docker-compose -f docker-compose-simple.yml logs -f redis
goto end

:connect_cli
echo [INFO] Connecting to Redis CLI...
docker-compose -f docker-compose-simple.yml exec redis redis-cli
goto end

:show_help
echo Redis Management Script for Backgammon Game
echo.
echo Usage: %0 [COMMAND]
echo.
echo Commands:
echo   start     Start Redis container
echo   stop      Stop Redis container
echo   restart   Restart Redis container
echo   status    Show Redis container status
echo   logs      Show Redis logs
echo   cli       Connect to Redis CLI
echo   help      Show this help message
echo.
echo Examples:
echo   %0 start    # Start Redis
echo   %0 status   # Check if Redis is running
echo   %0 cli      # Open Redis command line interface
goto end

:unknown_command
echo [ERROR] Unknown command: %COMMAND%
goto show_help

:end
