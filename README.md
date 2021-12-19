# Backend Assignment -Extern

API to fetch latest videos sorted in reverse chronological order of their publishing
date-time from YouTube for a given tag/search query in a paginated response.

- When django server starts, the management commands automatically start syncing the API with database.
- Dashboard `http://127.0.0.1:8000/admin/` to access the sync data.
- Implement a GET API which returns the stored video data in a paginated response sorted in decending
  order of published datetime.
- The API will give 50 results on every query.  To view next ones, use `http://127.0.0.1:8000/videos/?page=2`


## Getting started

- Used Django for Backend
- Used Docker to Containerize the project
- Admin dashboard to view the stored videos with filters and sorting options
- Asynchronously sync the database with API


## Run Locally

### Using Docker

- Add `YOUTUBE_API_KEY` in `.env`.
- Run `docker-compose up`

### Building from source

- Fork the repo `https://github.com/edith007/Youtube-API-Backend-Assignment` 
- Clone the repo and type the following command in terminal
    `git clone git@github.com:edith007/Youtube-API-Backend-Assignment.git`
- Create a virtual environment using the python command
    `python3 -m venv env`
- Install the dependencies
    `pip install -r requirements.txt`
- Add `YOUTUBE_API_KEY` in `.env`.
- After the dependencies are install run the migration using command
    `python3 manage.py makemigrations && python3 manage.py migrate`
- Start the server through the following command
    `python3 manage.py lookup` -> To fetch API
    `python3 manage.py runserver` -> To run Django Server
- You can run the server and fetch the API with single management command
    `python3 manage.py lookup_runserver`