from pyramid.response import Response
from pyramid.view import view_config, forbidden_view_config
from pyramid.security import remember,authenticated_userid, forget, Authenticated

from pyramid.httpexceptions import HTTPFound

import json,hashlib

from .models import DBSession
from .models import Student
from ..course.models import Course, CourseStudent

from sqlalchemy import and_

@view_config(
	route_name='registerStudent',
	renderer='json',
	request_method='POST',
	permission='__no_permission_required__'
)
def registerStudent(request):

	name = request.POST['name']

	email = request.POST['email']
	password = hashlib.sha256(request.POST['password']).hexdigest()

	institute_id = request.POST['institute_id']
	institute_roll_num = request.POST['institute_roll_num']

	dbFoundUser = DBSession.query(Student).filter(Student.email == email).first()
	if dbFoundUser:
		return {'status' : 'false'}

	dbFoundUser = Student(name, email, institute_id, institute_roll_num, password)
	DBSession.add(dbFoundUser)
	DBSession.flush()

	request.session['user'] = dbFoundUser.getJSON()
	headers = remember(request,dbFoundUser.id)
	request.response.headerlist.extend(headers)

	return {'status' : 'true'}

@view_config(
	route_name='login',
	renderer='json',
	request_method='POST',
	permission='__no_permission_required__'
)
def login(request):

	email = request.POST['email']
	password = hashlib.sha256(request.POST['password']).hexdigest()

	print email, password

	dbFoundUser = DBSession.query(Student).\
	filter(and_(Student.email == email, Student.password == password)).\
	first()

	if dbFoundUser is None:
		return {'status' : 'false'}

	request.session['user'] = dbFoundUser.getJSON()
	headers = remember(request,dbFoundUser.id)
	request.response.headerlist.extend(headers)

	return {'status' : 'true'}

@view_config(
	route_name='logout',
	renderer='json'
)
def logout(request):
    
    currentUser = int(authenticated_userid(request))
    headers = forget(request)
    request.session.invalidate()
    request.response.headerlist.extend(headers)

    return {'status' : 'true'}


@view_config(
	route_name='studentCourses',
	renderer='json',
	request_method='GET'
)
def studentCourses(request):

	studentId = int(authenticated_userid(request))

	courseQuery = DBSession.query(CourseStudent).filter(CourseStudent.student_id == studentId)
	courses = []
	for courseStudent in courseQuery.all():
		courseId = courseStudent.course_id
		course = DBSession.query(Course).filter(Course.id == courseId).first()
		courses.append(course.getJSON())

	return {'courses' : courses}

@view_config(
	route_name='courseRegister',
	renderer='json',
	request_method='POST'
)
def courseRegister(request):

	studentId = int(authenticated_userid(request))
	courseId = request.POST['course_id']

	courseStudent = DBSession.query(CourseStudent).\
	filter(and_(CourseStudent.student_id == studentId, CourseStudent.course_id == courseId)).\
	first()

	if courseStudent:
		return {'status' : 'false'}

	courseStudent = CourseStudent(courseId, studentId)
	DBSession.add(courseStudent)
	DBSession.flush()

	return {'status' : 'true'}