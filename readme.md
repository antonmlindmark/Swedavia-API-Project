**OpenSky Flight Tracker Dashboard**

This is a terminal-based dashboard that tracks live arrivals, departures, and aircraft histories using the free OpenSky Network API. It is designed to be hosted on an AWS EC2 instance.

**Prerequisites**
Docker installed on your local machine or server.

**How to Run**
Build the Docker image:
docker build -t flight-tracker .

Run the container interactively:
docker run -it flight-tracker