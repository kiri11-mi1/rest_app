from app import app, auth, db
from flask import jsonify, abort, make_response, request, url_for
from app.models import Task

@auth.get_password
def get_password(username):
    if username == 'admin':
        return 'password'
    return None

def make_public(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
            new_task['id'] = task['id']
        else:
            new_task[field] = task[field]
    
    return new_task

@app.route('/todo/api/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    tasks = []
    for t in db.session.query(Task).all():
        tasks.append( {'id': t.id, 'title': t.title, 'description': t.description, 'done': t.done} )
    new_tasks = [make_public(t) for t in tasks]
    return jsonify({'tasks': new_tasks})

@app.route('/todo/api/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    t = db.session.query(Task).get(task_id)
    if t is None:
        abort(404)
    task = {
        'id': t.id,
        'title': t.title,
        'description': t.description,
        'done': t.done
    }
    return jsonify({'task' : make_public(task) } )

@app.route('/todo/api/tasks', methods=['POST'])
@auth.login_required
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    tasks = db.session.query(Task).all()
    task = {
        'id' : tasks[-1].id + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ''),
        'done': False
    }
    t = Task(title=task['title'], description=task['description'])
    db.session.add(t)
    db.session.commit()
    return jsonify( {'task' : make_public(task)} ), 201

@app.route('/todo/api/tasks/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    t = db.session.query(Task).get(task_id)
    if t is None:
        abort(404)
    db.session.delete(t)
    db.session.commit()
    return jsonify( {'result' : True} )

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    t = db.session.query(Task).get(task_id)
    if t is None:
        abort(404)

    if not request.json:
        abort(400)
    
    if 'title' in request.json and type(request.json['title']) is not unicode:
        abort(400)

    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)

    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)

    t.title = request.json.get('title', t.title)
    t.description = request.json.get('description', t.description)
    t.done = request.json.get('done', t.done)

    task = {
        'id': t.id,
        'title': t.title,
        'description': t.description,
        'done': t.done
    }

    return jsonify({ 'task' : make_public(task) })
