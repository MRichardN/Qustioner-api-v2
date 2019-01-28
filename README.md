# Questioner-api
[![Build Status](https://travis-ci.com/MRichardN/Questioner-api.svg?branch=develop)](https://travis-ci.com/MRichardN/Questioner-api)
[![Coverage Status](https://coveralls.io/repos/github/MRichardN/Questioner-api/badge.svg?branch=develop)](https://coveralls.io/github/MRichardN/Questioner-api?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/c72f85d70a879602dc6c/maintainability)](https://codeclimate.com/github/MRichardN/Questioner-api/maintainability)

A questioner is a platform for crowd-sourcing questions for a meetup. It helps the meetup organizer prioritize  questions to be answered. Other users can vote on asked questions and they bubble to the top  or bottom of the log.

## Prerequisites
- Python 3.7.0 
- Postman


## Installation
1. Clone this repository :

	```
    $ git clone https://github.com/MRichardN/Questioner-api.git
    ```

2. CD into the project folder on your machine

	```
    $ cd Questioner-api
    ```

3. Create a virtual environment

    ```
    $ python3 -m venv venv
    ```

4. Activate the virtual environment

	```
    $ . venv/bin/activate
    ```

5. Install the dependencies from the requirements file

	```
    $ pip install -r requirements.txt
    $ pip install python-dotenv
    ```

6. Run the application

    ```
    python3 run.py
    ```

## Testing API endpoint

| Endpoint                             | HTTP Verb   | Functionality           |
| ------------------------------------ | ----------- | ----------------------- |    
| /api/v1/add_meetup/                  | POST        | Create a meetup record       |
| /api/v1/meetups/meetup_id/           | GET         | Fetch a specific meetup record |
| /api/v1/meeetups/upcoming/           | GET         | Fetch all upcoming meetup records       |
| /api/v1/add_question/                | POST        | Create a question for a specific meetup   |
| /api/v1/questions/<question_id>/upvote/| PATCH       | Up-vote a specific question       |
| /api/v1/questions/<question_id>/downvote/| PATCH       | Down-vote a specific question       |
| /api/v1/add_meetups/<meetup_id>/rsvps/   | POST        | Create a question for a specific meetup   |

## Authors
Mathenge Richard - [MRichardN](https://github.com/MRichardN)

## License
This project is licensed under [MIT](https://github.com/MRichardN/Questioner-api/blob/master/LICENSE) license.

## Acknowledgement
-Andela Workshops
-Team members