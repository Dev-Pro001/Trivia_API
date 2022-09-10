# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Setting up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia_db
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia_db < trivia.psql
```


### Starting the Server

Navigate to the backend directory first ensure you are working using your created virtual environment.

To run the server, execute:

```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
# API Documentation 

**Endpoints**

``` GET '/categories'  ```

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category

- Request Arguments: None

- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.

Example: ```curl http://localhost:5000/categories```

```
{
    'categories': { 

    '1' : 'Science',
    '2' : 'Art',
    '3' : 'Geography',
    '4' : 'History',
    '5' : 'Entertainment',
    '6' : 'Sports' 
   }
}

```


``` GET '/questions' ```

- Fetches a paginated set of questions, a total number of questions, all categories and current category string.

- Returns: An object with a list of questions, total questions, all categories, and current category string

Example: ```curl http://localhost:5000/questions```

**NOTE:** The questions list is truncated 
```
{
    'questions': [
	{   
	    'id': 2,
	    'question':  'What movie earned Tom Hanks his third straight Oscar nomination, in 1996?',
    	    'answer':  'Apollo 13',
    	    'difficulty': 4,
    	    'category': 5,
	},

	{   
	    'id': 4,
	    'question':  'What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?',
    	    'answer':  'Tom Cruise',
    	    'difficulty': 4,
    	    'category': 5,
	},

	{   
	    'id': 5,
	    'question':  'Who discovered penicillin?',
    	    'answer':  'Alexander Fleming',
    	    'difficulty': 3,
    	    'category': 1,
	},

	{   
	    'id': 9,
	    'question':  'What boxer's original name is Cassius Clay?',
    	    'answer':  'Muhammad Ali',
    	    'difficulty': 1,
    	    'category': 4,
	},
	
	{
            'id': 10,
            'question': 'Which is the only team to play in every soccer World Cup tournament?',
            'answer': 'Brazil',
            'difficulty': 3,
            'category': 6
        }
    ],
    'total_questions': 19,
    'categories': { 

    '1' : 'Science',
    '2' : 'Art',
    '3' : 'Geography',
    '4' : 'History',
    '5' : 'Entertainment',
    '6' : 'Sports' 
    },
    'current_category': null
}
```

``` GET '/categories/<category_id>/questions' ```

- Fetches questions from a given category specified in the request argument 

- Request Arguments: category_id 

- Returns: An object with the list of questions for the specified category, total questions, and current category string


Example: ```curl http://localhost:5000/categories/5/questions```

```
{
    'questions': [
	{   
	    'id': 2,
	    'question':  'What movie earned Tom Hanks his third straight Oscar nomination, in 1996?',
    	    'answer':  'Apollo 13',
    	    'difficulty': 4,
    	    'category': 5,
	},
	
	{   
	    'id': 4,
	    'question':  'What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?',
    	    'answer':  'Tom Cruise',
    	    'difficulty': 4,
    	    'category': 5,
	}
    ],
    'total_questions': 2,
    'current_category': 5
}

```


``` DELETE '/questions/<question_id> ```

- Deletes a specified question from the given list based on the id of the question

- Request Arguments: question_id 

- Returns: An id of the deleted question.

Example: ```curl -X DELETE http://localhost:5000/questions/5```

```
{ 
    'deleted': 5
}

```

`` POST '/questions' ```

- Takes in request body arguments and adds a new question to the existing list.

- Request Body: 

```
{
    'question':  'Who discovered penicillin?',
    'answer':  'Alexander Fleming',
    'difficulty': 3,
    'category': 1,
}

```

- Returns: An id of the newly created question

Example:  ```curl -X POST http://localhost:5000/api/questions -H 'Content-Type: application/json' -d '{'question': 'Who discovered penicillin?', 'answer': 'Alexander Fleming', 'difficulty': 3, 'category': 1}'```

```
{
    'created': 21
}

```


``` POST '/questions/search' ```

- It performs partial text match and returns the list of questions matching.

- Request Body:

```
{
    'searchTerm': 'play'
}

```

- Returns: An object of list of questions that met the search criteria, total questions

Example: ```curl -X POST http://localhost:5000/api/questions -H 'Content-Type: application/json' -d '{'searchTerm': 'play'}'```

```
{
	'questions': [
       	 {
            'id': 10,
            'question': 'Which is the only team to play in every soccer World Cup tournament?',
            'answer': 'Brazil',
            'difficulty': 3,
            'category': 6
        },
    ],
    	'total_questions': 1,
}

```

``` POST '/quizzes' ```

- Allows a user to play the quiz 

- Request Arguments: 
	- quiz_category: the category which we want questions from
	- previous_questions: contains the list of questions which we already played
- Returns : A random question from a given category or across all categories which is not in the previous asked questions. 

Example: ```curl -X POST http://localhost:5000/quizzes -H 'Content-Type: application/json' -d '{ 'quiz_category': { 'id':'1'}, 'previous_questions': []}'```

```
{
    'question': {
	'id': 22,
	'question': Hematology is a branch of medicine involving the study of what?,
        'answer': 'Blood',
        'category_id': 1,
        'difficulty': 4,
    }
}

```







