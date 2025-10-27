# Redis Installation Guide for Windows

## Option 1: Using Chocolatey (Recommended)

1. Install Chocolatey if you don't have it:

   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

2. Install Redis:

   ```powershell
   choco install redis-64
   ```

3. Start Redis server:
   ```powershell
   redis-server
   ```

## Option 2: Using Docker (Alternative)

1. Install Docker Desktop
2. Run Redis in a container:
   ```bash
   docker run -d -p 6379:6379 --name redis redis:latest
   ```

## Option 3: Manual Installation

1. Download Redis for Windows from: https://github.com/microsoftarchive/redis/releases
2. Extract and run `redis-server.exe`

## Fallback Solution

If Redis installation is not possible, the application will automatically use file-based persistence instead. Games will be saved as JSON files in the `saved_games` directory.

## Testing Redis Connection

To test if Redis is working:

```bash
redis-cli ping
```

Should return: `PONG`
