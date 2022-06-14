import json
from flask import (
    Flask,
    abort,
    jsonify,
    request
)

from flask_cors import CORS, cross_origin

from models import setup_db, Todo, TodoList


TODOS_PER_PAGE=5

def paginate_todos(request, selection, isDescendent):
    if isDescendent:
        start = len(selection) - TODOS_PER_PAGE
        end = len(selection)
    else:
        page = request.args.get('page', 1, type=int)
        start = (page - 1)*TODOS_PER_PAGE
        end = start + TODOS_PER_PAGE
    todos = [todo.format() for todo in selection]
    current_todos = todos[start:end]
    return current_todos
    


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, origins=['https://utec.edu.pe', 'http://127.0.0.1:5001'], max_age=10)
    
    @app.after_request
    def after_resquest(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorizations, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/todos', methods=['GET'])
    def get_todos():
        selection = Todo.query.order_by('id').all()
        todos = paginate_todos(request, selection, False)
        
        if len(todos) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'todos': todos,
            'total_todos': len(selection)
        })

    @app.route('/todos', methods=['POST'])
    def create_todo():
        body = request.get_json()

        description = body.get('description', None)
        completed = body.get('completed', None)
        list_id = body.get('list_id', None)
        search = body.get('search', None)

        if search:
            selection = Todo.query.order_by('id').filter(Todo.description.like('%{}%'.format(search))).all()
            todos = paginate_todos(request, selection, False)
            return jsonify({
                'success': True,
                'todos': todos,
                'total_todos': len(selection)
            })

        if description is None or list_id is None:
            abort(422)

        todo = Todo(description=description, completed=completed, list_id=list_id)
        new_todo_id = todo.insert()
        
        selection = Todo.query.order_by('id').all()
        current_todos = paginate_todos(request, selection, True)

        return jsonify({
            'success': True,
            'created': new_todo_id,
            'todos': current_todos,
            'total_todos': len(selection)
        })


    @app.route('/todos/<todo_id>', methods=['PATCH'])
    def update_todo(todo_id):
        error_404 = False
        try:
            todo = Todo.query.filter(Todo.id==todo_id).one_or_none()

            if todo is None:
                error_404 = True
                abort(404)

            body = request.get_json()
            if 'description' in body:
                todo.description = body.get('description')

            todo.update()

            return jsonify({
                'success': True,
                'id': todo_id
            })
        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)



    @app.route('/todos/<todo_id>', methods=['DELETE'])
    def delete_todo(todo_id):
        error_404 = False
        try:
            todo = Todo.query.filter(Todo.id == todo_id).one_or_none()
            if todo is None:
                error_404 = True
                abort(404)

            todo.delete()

            selection = Todo.query.order_by('id').all()
            todos = paginate_todos(request, selection, True)

            return jsonify({
                'success': True,
                'deleted': todo_id,
                'todos': todos,
                'total_todos': len(selection)
            })
        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)


    @app.route('/lists', methods=['GET'])
    def get_lists():
        error_404 = False
        try:
            lists = {list.id: {'id': list.id, 'name': list.name} for list in TodoList.query.order_by('id').all()}

            if len(lists) == 0:
                error_404 = True
                abort(404)

            return jsonify({
                'success': True,
                'lists': lists,
                'total_lists': len(lists)
            })
        except Exception as e:
            print(e)
            if error_404:
                abort(404)


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'code': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'code': 500,
            'message': 'Internal Server Error'
        }), 500


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'code': 422,
            'message': 'Unprocessable'
        }), 422

    return app
