FROM python:3.12-slim

#set working directory 
WORKDIR /api

# Copy the requirements to install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the application port 
EXPOSE 8000

# Command to start FastAPI application
CMD ["uvicorn", "api.app", "--host", "0.0.0.0", "--port", "8000"]