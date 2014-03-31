from pyramid.response import Response
from pyramid.view import view_config, forbidden_view_config
from pyramid.security import remember,authenticated_userid, forget, Authenticated

from pyramid.httpexceptions import HTTPFound

from .models import DBSession
from .models import Course, CourseStudent, CourseFaculty, CourseResource, CourseAssignment, CourseMark, CourseQuiz, Question, QuizQuestion

from ..faculty.models import Faculty
import json

from sqlalchemy import and_

@view_config(
	route_name='courseGetAll',
	renderer='json',
	request_method='GET',
	permission='__no_permission_required__'
)
def courseGetAll(request):

	courseQuery = DBSession.query(Course)

	courses = []
	for course in courseQuery.all():
		courses.append(course.getJSON())

	return {'courses' : courses}

@view_config(
	route_name='courseInstituteGetAll',
	renderer='json',
	request_method='GET',
)
def courseInstituteGetAll(request):

	studentId = int(authenticated_userid(request))
	studentInstituteId = request.session['user']['institute_id']
	courseQuery = DBSession.query(Course).filter(Course.institute_id == studentInstituteId)

	courses = []
	for course in courseQuery.all():
		_course = course.getJSON()
		courseStudentQuery = DBSession.query(CourseStudent).\
		filter(and_(CourseStudent.student_id == studentId, CourseStudent.course_id == course.id)).first()
		registered = 'false'
		if courseStudentQuery is not None:
			registered = 'true'
		_course.update({'registered' : registered})
		courses.append(_course)

	return {'courses' : courses}

@view_config(
	route_name='courseFaculty',
	renderer='json',
	request_method='GET'
)
def courseFaculty(request):

	studentId = int(authenticated_userid(request))
	courseId = request.matchdict['course_id']

	courseFaculty = DBSession.query(CourseFaculty).\
	filter(CourseFaculty.course_id == courseId).all()

	facultys = []
	for faculty in courseFaculty:
		_faculty = DBSession.query(Faculty).\
		filter(Faculty.id == faculty.faculty_id).first()

		facultys.append(_faculty.getJSON())

	return {'faculty' : facultys}

@view_config(
	route_name='courseResource',
	renderer='json',
	request_method='GET'
)
def courseResource(request):

	studentId = int(authenticated_userid(request))
	courseId = request.matchdict['course_id']

	courseResource = DBSession.query(CourseResource).\
	filter(CourseResource.course_id == courseId).all()

	resources = []
	for resource in courseResource:
		_resource = resource.getJSON()
		_resource['attachment']['location'] = '<a href = %s>%s</a>'%(_resource['attachment']['location'],_resource['attachment']['location'])
		resources.append(_resource)

	return {'resources' : resources}

@view_config(
	route_name='courseAssignment',
	renderer='json',
	request_method='GET'
)
def courseAssignment(request):

	studentId = int(authenticated_userid(request))
	courseId = request.matchdict['course_id']

	courseAssignment = DBSession.query(CourseAssignment).\
	filter(CourseAssignment.course_id == courseId).all()

	assignments = []
	for assignment in courseAssignment:
		_assignment = assignment.getJSON()
		_assignment['attachment']['location'] = '<a href = %s>%s</a>'%(_assignment['attachment']['location'],_assignment['attachment']['location'])
		assignments.append(_assignment)

	return {'assignments' : assignments}

@view_config(
	route_name='courseMarks',
	renderer='json',
	request_method='GET'
)
def courseMarks(request):

	studentId = int(authenticated_userid(request))
	courseId = request.matchdict['course_id']

	courseMark = DBSession.query(CourseMark).\
	filter(and_(CourseMark.course_id == courseId, CourseMark.student_id == studentId)).\
	all()

	marks = []
	for mark in courseMark:
		_mark = mark.getJSON()
		marks.append(_mark)

	return {'marks' : marks}

@view_config(
	route_name='courseQuiz',
	renderer='json',
	request_method='GET'
)
def courseQuiz(request):

	studentId = int(authenticated_userid(request))
	courseId = request.matchdict['course_id']

	courseQuiz = DBSession.query(CourseQuiz).\
	filter(and_(CourseQuiz.course_id == courseId, CourseQuiz.is_active == True)).\
	first()

	quiz = courseQuiz.getJSON()
	quiz['questions'] = []
	
	quizQuestions = DBSession.query(QuizQuestion).\
	filter(QuizQuestion.course_quiz_id == courseQuiz.id).all()

	for question in quizQuestions:
		quiz['questions'].append(question.getJSON())

	quizHTML = '<form method="post">'
	quizHTML += '<ol>'
	for question in quizQuestions:
		_question = question.getJSON()['question']
		quizHTML += '<li>'
		quizHTML += _question['question'] + "<br />"
		quizHTML += '<input type="radio" value="option_a" name="answer-%s" > %s <br />'%(_question['id'], _question['option_a'])
		quizHTML += '<input type="radio" value="option_b" name="answer-%s" > %s <br />'%(_question['id'], _question['option_b'])
		quizHTML += '<input type="radio" value="option_c" name="answer-%s" > %s <br />'%(_question['id'], _question['option_c'])
		quizHTML += '<input type="radio" value="option_d" name="answer-%s" > %s <br />'%(_question['id'], _question['option_d'])
		quizHTML += '</li>'

	quizHTML += '</ol>'
	quizHTML += '<input type="submit" value="Submit" id="quiz-submit">'
	quizHTML += '</form>'

	quiz['quizHTML'] = quizHTML

	return {'quiz' : quiz}
