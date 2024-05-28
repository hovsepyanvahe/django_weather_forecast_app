# Weather App
This is a Django application for fetching weather forecasts using Docker Compose.

## Prerequisites

Before you begin, ensure you have Docker and Docker Compose installed on your system.

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
```

## Running the Application

1. Clone this repository:

```bash
git clone https://github.com/your-username/weather-app.git
cd weather-app
```

2. Set up environment variables:

Create a `.env` file in the `docker` directory and configure the following variables:

```plaintext
# docker/.env
APP_NAME=weather_app
```

3. Build and run Docker containers:

```bash
docker-compose up --build
```

4. Access the application:

Once the containers are up and running, you can access the application at `http://localhost:8000`.

## Stopping the Application

To stop the application and remove the containers, press `Ctrl + C` in the terminal where Docker Compose is running, and then run:

```bash
docker-compose down
```

## Configuration

### Database Configuration

The PostgreSQL database is configured to use the following settings:

- Database Name: postgres
- Username: postgres
- Password: supersecretpassword

You can modify these settings in the `docker-compose.yml` file if needed.

### Environment Variables

You can customize environment variables for the Django application in the `.env` file located in the `docker` directory.
