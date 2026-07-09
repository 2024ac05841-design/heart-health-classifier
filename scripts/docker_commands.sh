# Build the Docker image
docker build -t heart-disease-api:latest .

# Run the container
docker run -d -p 8000:8000 --name heart-api heart-disease-api:latest

# Check logs
docker logs heart-api

# Stop and remove container
docker stop heart-api
docker rm heart-api
