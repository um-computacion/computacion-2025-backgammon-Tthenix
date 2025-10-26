# Use Ubuntu base image and install Python
FROM ubuntu:22.04

# Set working directory
WORKDIR /app

# Install Python and system dependencies required for Pygame
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libfreetype6-dev \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*

# Create symlink for python command
RUN ln -s /usr/bin/python3 /usr/bin/python

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Set environment variables for Pygame
ENV SDL_VIDEODRIVER=dummy
ENV DISPLAY=:99
ENV SDL_AUDIODRIVER=dummy
ENV PULSE_SERVER=unix:/tmp/pulse-socket

# Make main.py executable
RUN chmod +x main.py

# Expose port (if needed for web interface in future)
EXPOSE 8000

# Default command to keep the container running
CMD ["sh", "-c", "echo 'Container is running. echo Container is running. Create a new terminal and execute the game with 'docker exec -it backgammon-game python main.py'.' && tail -f /dev/null"]

