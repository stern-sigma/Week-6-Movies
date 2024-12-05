[![Test and Deploy](https://github.com/stern-sigma/Week-6-Movies/actions/workflows/test_and_deploy.yml/badge.svg)](https://github.com/stern-sigma/Week-6-Movies/actions/workflows/test_and_deploy.yml)

# Stern's Movies API Documentation

Welcome to Stern's Movies API! Follow these steps to get the API up and running:

1. Configure your **secrets** to map to a remote host.
2. Separately send a `.env` file with your remote database server details to the same location.

Once the above is set up, **automated actions will take care of loading and initializing the server.**

> **Note:** This repository only ships the server. For database initialization functionality, refer to [this repository](https://github.com/stern-sigma/Coursework-Backend-Week-2/tree/main/movie_api).

The server runs on port `5000` by default. However, this can be reconfigured in the environment settings.

---

## Endpoints

### `/`
**Method:** `GET`  
**Description:** Returns a greeting message.

---

### `/movies`
**Methods:** `GET`, `POST`

#### `GET`:
Returns a list of all movies in the database (⚠️ **Warning:** this can be slow).  
Optionally, the following query parameters are supported:  
- `sort_by`: Determines which field the list should be sorted by. Acceptable values:  
  - `movie_id`, `title`, `score`, `budget`, `revenue`.  
- `sort_order`: Determines the sort direction. Acceptable values:  
  - `asc`, `desc`.  
- `search`: Filters results to only include movies with the provided substring in their title.

#### `POST`:
Accepts a JSON payload with the following fields to add a movie to the database:  
- `title`: string  
- `release_date`: string, formatted as `'MM/DD/YYYY'`  
- `genre`: string  
- `overview`: string  
- `budget`: float  
- `revenue`: float  
- `country`: string  
- `language`: string  
- `orig_title`: string  

---

### `/movies/<movie_id>`
**Methods:** `GET`, `DELETE`

#### `GET`:
Returns the movie with the specified `movie_id`.

#### `DELETE`:
Deletes the movie with the specified `movie_id`.

---

### `/countries/<country_code>`
**Method:** `GET`  
**Description:** Returns a list of movies made in the specified country.  

#### Query Parameters:
- `sort_by` and `sort_order` are supported as described in the `/movies` endpoint.

---
