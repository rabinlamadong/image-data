## Introduction
This service loads image data from the provided csv file located in `data-source/data.csv`
applies the required transformation and dumps it into the application's database.
And, it has an API to get the data from the DB.

## Setup instructions
1. Clone the repo to your local machine
2. Copy the .env file `cp .env.sample .env`
3. Run the service in docker `docker compose up --build -d`
4. Visit the API doc page `http://localhost:8000/docs`