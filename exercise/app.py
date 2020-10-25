 
from flask import Flask, jsonify, request, Response
from database.db import initialize_db
from database.models import Professor, ResearchGroup, Student
import json
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# database configs
app.config['MONGODB_SETTINGS'] = {
    # set the correct parameters here as required, some examples aer give below
    'host':'mongodb://mongo:27017/flask-db'
    # 'host':'mongodb://localhost/flask-db'
}
db = initialize_db(app)


@app.route('/listProfessor', methods=['post'])
def add_professor():
    print(request)
    body = request.get_json()
    professor = Professor(**body)
    professor.save()
    id = professor.id 
    output = {'message': "Professor successfully created", 'id': str(id)}
    print(type((output)))
    return (output), 201

@app.route('/listStudent', methods=['post']) 
def add_student():
    """
    This function creates a new student given student_id in the request body

    Returns:
        dict: Dictionary containing the message and id
        int : The status code
    """
    # Update the code here.      
    body = request.get_json()

    body['researchGroups'] = ObjectId(body['researchGroups'])
    student = Student(**body)
    student.save()
    id = student.id 
    for v,i in body['founder']:
        print(v)
    output = {'message': "Student successfully created", 'id': str(id)}
    return (output), 201

@app.route('/listGroup', methods=['post'])
def add_research_group():
    """
    This function creates a new student given research_group_id in the request body

    Returns:
        dict: Dictionary containing the message and id
        int : The status code
    """
    body = request.get_json()
    body['founder'] = ObjectId(body['founder'])

    research_group = ResearchGroup(**(body))
    # research_group.founder = professor
    research_group.save()
    output = {'message': "Group successfully created", 'group_id': str(research_group.id)}
    
    return jsonify(output), 201
# 5f956a68ac53930c6b3dcc9b
# Update the methods below

@app.route('/listProfessor/<prof_id>', methods=['get'])
def get_professor_by_id(prof_id):
    professors = (Professor.objects.exclude('id').get(id=prof_id)).to_json()
    return jsonify(professor), 200

@app.route('/listProfessors', methods=['get'])
def get_all_professors():
    query_param = (request.args.get('designation'))
    if (query_param is not None):
        professors = Professor.objects(designation=query_param).exclude('id','interests','designation').to_json()
        print(type(professors))
        print (professors)

        return professors, 200
    # else:
    #     query_param = (request.args.get('groupName'))
    #     group = ResearchGroup.objects(name=query_param)
    #     professors = Professor.objects(researchGroups.id=group.id)


@app.route('/listStudent/<student_id>', methods=['get'])
def get_student_by_id(student_id):
    """
    Get (read), update or delete a student

    Args:
        student_id (Object id): The student Id of the student record that nees to be modified.

    Returns:
        dict: The dictionary with output values
        int : The status code
    """
    
    if request.method == "Update here":
        student = "Get the students from database here"
        if student:
            # Update Code here
            
            output = {'name': "", 'studentNumber': "", 'researchGroups': ""}
        else:
            # Update Code here
            
            output = {'message': ''}
        status_code = 000
        return output, status_code
    elif request.method == "Update this line":
        body = request.get_json()
        keys = body.keys()
        if body and keys:
            # Update Code here
            
            output = {'message': '', 'id': ''}
        else:
            # Update Code here
            
            output = {'message': 'Message body empty'}
        status_code = 000
        return output, status_code
    elif request.method == "update here":
        # Update Code here

        # Student.objects.get_or_404(id=student_id).delete()
        output = {'message': '', 'id': ''}
        status_code = 000
        return output, status_code

@app.route('/listProfessor/<prof_id>',methods=['delete'])
def delete_professor(prof_id):
    print(prof_id)
    professor = Professor.objects.get(id=prof_id)
    output = {'message': "Professor successfully deleted", 'id': str(prof_id)}
    
    professor.delete()
    return output,200

@app.route('/listGroup/<group_id>',methods=['delete'])
def delete_group(group_id):
    print(12312)
    rg = ResearchGroup.objects.get(id=group_id)
    print(rg)
    output = {'message': "Group successfully deleted", 'id': str(group_id)}
    rg.delete()
    return output,200

@app.route('/listStudent/<student_id>',methods=['delete'])
def delete_student(student_id):
    student = Student.objects.get(id=student_id)
    output = {'message': "Student successfully deleted", 'id': str(student_id)}
    student.delete()
    return output,200


# Complete the  request methods below


# Only for local testing without docker
app.run() # FLASK_APP=app.py FLASK_ENV=development flask run