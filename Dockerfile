# Use the slim image as the base
FROM python:3.12-slim-bullseye

# Set the working directory
WORKDIR /app

# Install necessary Python tools
RUN pip install setuptools

# Copy the requirements.txt to the working directory
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the working directory
COPY . /app

# Expose the port
EXPOSE 8080

# Set environment variables 
ENV OPENAI_API_KEY = "OPENAI_API_KEY"
ENV VERIFY_TOKEN = "VERIFY_TOKEN"
ENV ACCESS_TOKEN = "ACCESS_TOKEN"
ENV PAGE_ID = "PAGE_ID"
ENV ASSISTANT_ID = "ASSISTANT_ID"
ENV INSTAGRAM_GRAPH_API_URL = "https://graph.facebook.com/v20.0"
ENV PORT=8080

# Command to run the application (correct path to main.py)
CMD ["python", "app/main.py"]