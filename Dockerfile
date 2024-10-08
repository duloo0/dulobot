# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the necessary dependencies
RUN pip install --no-cache-dir discord.py requests

# Set environment variables
ENV INFERMATIC_API_KEY=${INFERMATIC_API_KEY}
ENV DISCORD_TOKEN=${DISCORD_TOKEN}

# Run the bot
CMD ["python", "chatbot.py"]
