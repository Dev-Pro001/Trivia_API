from errno import ESTALE
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import func

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)    # 
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    paginated_questions = questions[start:end]
    return paginated_questions




def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response


    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def retrieve_categories():
        #Retrieving and formatting the categories
        categories = Category.query.all()
        if len(categories)==0:
            abort(404)
        else:
            formatted_categories = {}
            for category in categories:
                formatted_categories[category.id] = category.type
            #Returning the result
            return jsonify({
                'success': True,
                'categories': formatted_categories
            })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions')
    def retrieve_questions():
        #Retrieving all questions and getting the count
        all_questions = Question.query.all()
        questions_count = len(all_questions)
        #Paginating the questions using the method for pagination defined above
        paginated_questions = paginate_questions(request, all_questions)
        #Retrieve and formatting the categories
        categories = Category.query.all()
        formatted_categories = {}

        for category in categories:
            formatted_categories[category.id] = category.type
        #Checking if questions are available
        if len(paginated_questions) == 0:
            abort(404)

        else:
        #Returning the result
            return jsonify({
                'success': True,
                'questions': paginated_questions,
                'total_questions': questions_count,
                'categories': formatted_categories,
                'current_category': None
            })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        #Get the question with the given id 
        question = Question.query.filter(Question.id == question_id).one_or_none()
        #Check if the question is not available
        if question is None:
            abort(404)
        #Otherwise   
        else:
            question.delete()
    
        return jsonify({
            'success': True,
            'deleted': question_id
        })

       
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions', methods=['POST'])
    def create_question():
        data = request.get_json()
        #Getting the values from the form fields
        question = data.get('question')
        answer = data.get('answer')
        difficulty = data.get('difficulty')
        category_id = data.get('category')
        #Checking if the question or answer is empty
        if (question is None) or (answer is None):
            abort (400)
        #Otherwise
        try:
            new_question = Question(
                question=question, 
                answer=answer,
                difficulty=difficulty, 
                category=category_id
                )
            new_question.insert()

            return jsonify({
            'success': True,
            'created': new_question.id,
           
            })

        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        data = request.get_json()
        #Checking if the search field is empty
        if data['searchTerm'] is None:
            abort(400)
        #Otherwise grab the searchTerm  and perfome a query on the database
        searchTerm = data.get('searchTerm')
        matched_results = Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).all()
        #Checking if questions with the searcTerm is found
        if len(matched_results) == 0:
            abort(404)
        #Paginating the questions 
        matched_questions = paginate_questions(request, matched_results)

        return jsonify({
        'success': True,
        'questions': matched_questions,
        'total_results': len(matched_results)
        })
    

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def retrieve_categorised_questions(category_id):
        #Grabbing the category whose id is passed from the url
        category = Category.query.get(category_id)
        #Checking if there's category with the given id
        if category is None:
            abort(404)
        else:
            categorised_questions = Question.query.filter(Question.category==category_id).all()
            paginated_categorised_questions = paginate_questions(request, categorised_questions)

        if len(categorised_questions) == 0:
            abort(404)

        else:
            return jsonify({
            'success': True,
            'questions': paginated_categorised_questions,
            'total_questions': len(categorised_questions),
            'current_category': category_id
            })

    
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    
    @app.route('/quizzes', methods=['POST'])
    def play():

        data =  request.get_json()
        previous_questions = data['previous_questions']   
        category_id  = data['quiz_category']['id']  

        if category_id==0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(category=category_id).all()

        questions = [question.format() for question in questions]
        #Getting the questions not in the previous asked questions
        filtered_questions = []
        for question in questions:
            if question['id'] not in previous_questions:
                filtered_questions.append(question)

        if len(filtered_questions) == 0:
            return jsonify({
                'success': True
            })

        else:
            #Getting a random question the filtered question
            question = random.choice(filtered_questions)

            return jsonify({
                'success': True,
                'question': question
            })

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
                'success': False, 
                'error': 404, 
                'message': 'Resource not found'
                }),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({
                'success': False, 
                'error': 422, 
                'message': 'Unprocessable'
                }),
            422,
        )
    
    @app.errorhandler(400)
    def bad_request(error):
        return (
                jsonify({
                'success': False, 
                'error': 400, 
                'message': 'Bad request'
                }),
            400
         )

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({
                'success': False, 
                'error': 405, 
                'message': 'Method not allowed'
                }),
            405,
        )

    
    @app.errorhandler(500)
    def internal_error(error):
        return (
            jsonify({
                'success': False,
                'error': 500,
                'message': 'Internal server error'
        }),
        500
        
        )
       



    return app

