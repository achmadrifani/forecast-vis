# forecast-vis

BMKG Forecast Visualization

## Docker Deployment

`docker build -t forecast-vis .`

`docker run -d --name forecast-vis -p 8501:8501 --restart unless-stopped forecast-vis`
