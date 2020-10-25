 
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
    if (request.args.get('researchGroups')):
        rg = (body['researchGroups'])
        rg = [ObjectId(rg_id) for rg_id in rg]
        body['researchGroups'] = rg
    professor = Professor(**body)
    professor.save()
    id = professor.id 
    output = {'message': "Professor successfully created", 'id': str(id)}
    print(type((output)))
    return (output), 201


@app.route('/listProfessor/<prof_id>', methods=['get'])
def get_professor_by_id(prof_id):
    professor = (Professor.objects.get(id=prof_id))
    output = {'name':professor.name, 'email':professor.email,'designation':professor.designation,'interests':professor.interests}

    return jsonify(output), 200


@app.route('/listProfessors', methods=['get'])
def get_professor_by_property():
    designation = request.args.get('designation')
    if designation:
        professors = Professor.objects(designation=designation)
        output = [
            {'name': professor.name, 'email': professor.email} for professor in professors
        ]
    else:
        groupName = request.args.get('groupName')
        research_group = ResearchGroup.objects.get(name=groupName)
        print(research_group.name)

        professors = Professor.objects(researchGroups=research_group)
        output = [
            {'name': professor.name, 'email': professor.email} for professor in professors
        ]
    return jsonify(output), 200

@app.route('/listProfessor/<prof_id>', methods=['put'])
def update_professor(prof_id):
    professor = Professor.objects(id= prof_id)
    body = request.get_json()
    try:
        rg =  body["researchGroups"]
        rg = [ObjectId(rg_id) for rg_id in rg]
        print(rg)

        body['researchGroups'] = rg
    except KeyError:
        pass
    finally:
        professor.update(**body)
        output = {'message': "Professor successfully updated", 'id': str(prof_id)}
        return output, 200

@app.route('/listProfessor/<prof_id>',methods=['delete'])
def delete_professor(prof_id):
    print(prof_id)
    professor = Professor.objects(id=prof_id)
    output = {'message': "Professor successfully deleted", 'id': str(prof_id)}
    
    professor.delete()
    return output,200

@app.route('/listGroup', methods=['post'])
def add_research_group():
    body = request.get_json()
    body['founder'] = ObjectId(body['founder'])

    research_group = ResearchGroup(**(body))
    # research_group.founder = professor
    research_group.save()
    output = {'message': "Group successfully created", 'id': str(research_group.id)}
    
    return jsonify(output), 201
# 5f956a68ac53930c6b3dcc9b
# Update the methods below

@app.route('/listGroup/<group_id>',methods=['get'])
def get_group_by_id(group_id):
    print(group_id)
    group = ResearchGroup.objects.get(id=group_id)
    print(group)
    output = {'id':group_id, 'name':group.name, 'founder':group.founder.id}
    return output,200

@app.route('/listGroup/<group_id>', methods=['put'])
def update_group(group_id):
    group = ResearchGroup.objects(id=group_id)
    body = request.get_json()
    try:
        
        rg = body['founder']
        print(body['founder'])
        rg = ObjectId(rg) 
        body['founder'] = rg
    except KeyError:
        pass
    finally:
        print(body)
        output = {'message': "Group successfully updated", 'id': str(group_id)}
        group.update(**body)
        return output, 200

@app.route('/listGroup/<group_id>',methods=['delete'])
def delete_group(group_id):
    rg = ResearchGroup.objects.get(id=group_id)
    rg.delete()
    output = {'message': "Group successfully deleted", 'id': str(group_id)}
    return output,200

@app.route('/listStudent', methods=['post'])
def add_student():

    body = request.get_json()
    if (request.args.get('researchGroups')):
        rg = (body['researchGroups'])
        rg = [ObjectId(rg_id) for rg_id in rg]
        body['researchGroups'] = rg
    student = Student(**body)
    print(body)
    # print(body['researchGroups'])
    student.save()
    id = student.id 
    output = {'message': "Student successfully created", 'id': str(id)}
    return (output), 201

@app.route('/listStudent/<student_id>',methods=['get'])
def get_student_by_id(student_id):
    student = Student.objects.get(id=student_id)
    body = {'name':student.name,'studentNumber':student.studentNumber,'researchGroups':student.researchGroups}
    return jsonify(body),200

@app.route('/listStudents', methods=['get'])
def get_students_by_property():
    groupName = request.args.get('groupName')
    research_group = ResearchGroup.objects.get(name=groupName)
    students = Student.objects(researchGroups=research_group)
    output = [
        {'name': student.name, 'studentNumber': student.studentNumber} for student in students
    ]
    return jsonify(output), 200

@app.route('/listStudent/<student_id>', methods=['put'])
def update_students(student_id):

    body = request.get_json()
    student = Student.objects(id=student_id)
    try:
        rg =  body["researchGroups"]
        rg = [ObjectId(rg_id) for rg_id in rg]
        print(rg)

        body['researchGroups'] = rg
    except KeyError:
        pass
    finally:
        student.update(**body)
        output = {'message': "Student successfully updated", 'id': str(student_id)}
        return output, 200

@app.route('/listStudent/<student_id>',methods=['delete'])
def delete_student(student_id):
    student = Student.objects.get(id=student_id)
    output = {'message': "Student successfully deleted", 'id': str(student_id)}
    student.delete()
    return output,200

app.run() # FLASK_APP=app.py FLASK_ENV=development flask run