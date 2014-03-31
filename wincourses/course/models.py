from sqlalchemy import Column,Integer

from ..models import Base,DBSession

from sqlalchemy.types import String, Boolean
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship

from ..institute.models import Institute
from ..student.models import Student
from ..faculty.models import Faculty

class Course(Base):

	__tablename__ = 'courses'

	id = Column(Integer,primary_key=True)
	name = Column(String(256))
	code = Column(String(64))
	year = Column(String(64))
	description = Column(String(4096))

	institute_id = Column(Integer,ForeignKey('institutes.id'),default = 1)
	# institute = relationship("Institute",foreign_keys=[institute_id])

	def __init__(self, name, code, year, description, institute_id):

		self.name = name
		self.code = code
		self.year = year
		self.description = description
		self.institute_id = institute_id

	def getJSON(self):

		jsonDict = {}
		jsonDict['id'] = self.id
		jsonDict['name'] = self.name
		jsonDict['code'] = self.code
		jsonDict['year'] = self.year
		jsonDict['description'] = self.description
		jsonDict['institute_id'] = self.institute_id

		return jsonDict

class CourseStudent(Base):

	__tablename__ = 'course_students'

	id = Column(Integer,primary_key=True)

	course_id = Column(Integer,ForeignKey('courses.id'),default = 1)
	# course = relationship("Course",foreign_keys=[course_id])

	student_id = Column(Integer,ForeignKey('students.id'),default = 1)
	# student = relationship("Student",foreign_keys=[student_id])

	def __init__(self, course_id, student_id):

		self.student_id = student_id
		self.course_id = course_id

class CourseFaculty(Base):

	__tablename__ = 'course_faculty'

	id = Column(Integer,primary_key=True)

	course_id = Column(Integer,ForeignKey('courses.id'),default = 1)
	# course = relationship("Course",foreign_keys=[course_id])

	faculty_id = Column(Integer,ForeignKey('faculty.id'),default = 1)
	# faculty = relationship("Faculty",foreign_keys=[faculty_id])

	def __init__(self, course_id, faculty_id):

		self.faculty_id = faculty_id
		self.course_id = course_id

class Attachment(Base):

	__tablename__ = 'attachments'

	id = Column(Integer,primary_key=True)
	type = Column(String(256))
	location = Column(String(2048))

	def __init__(self, type, location):

		self.type = type
		self.location = location

	def getJSON(self):

		jsonDict = {}
		jsonDict['type'] = self.type
		jsonDict['location'] = self.location

		return jsonDict

class CourseResource(Base):

	__tablename__ = 'course_resources'

	id = Column(Integer,primary_key=True)

	course_id = Column(Integer,ForeignKey('courses.id'),default = 1)
	# course = relationship("Course",foreign_keys=[course_id])

	attachment_id = Column(Integer,ForeignKey('attachments.id'),default = 1)
	attachment = relationship("Attachment",foreign_keys=[attachment_id])
	
	description = Column(String(4096))

	def __init__(self, course_id, attachment_id, description):

		self.course_id = course_id
		self.attachment_id = attachment_id
		self.description = description

	def getJSON(self):

		jsonDict = {}
		jsonDict['id'] = self.id
		jsonDict['description'] = self.description
		jsonDict['attachment'] = self.attachment.getJSON()

		return jsonDict

class CourseAssignment(Base):

	__tablename__ = 'course_assignments'

	id = Column(Integer,primary_key=True)

	course_id = Column(Integer,ForeignKey('courses.id'),default = 1)
	# course = relationship("Course",foreign_keys=[course_id])

	attachment_id = Column(Integer,ForeignKey('attachments.id'),default = 1)
	attachment = relationship("Attachment",foreign_keys=[attachment_id])
	
	description = Column(String(4096))
	uploaded = Column(String(256))
	due_date = Column(String(256))
	is_active = Column(Boolean, default = True)

	def __init__(self, course_id, attachment_id, description,
		uploaded, due_date, is_active = True):

		self.course_id = course_id
		self.attachment_id = attachment_id
		self.description = description
		self.uploaded = uploaded
		self.due_date = due_date
		self.is_active = is_active

	def getJSON(self):

		jsonDict = {}
		jsonDict['id'] = self.id
		jsonDict['description'] = self.description
		jsonDict['uploaded'] = self.uploaded
		jsonDict['due_date'] = self.due_date
		jsonDict['is_active'] = self.is_active
		jsonDict['attachment'] = self.attachment.getJSON()

		return jsonDict
		
class CourseMark(Base):

	__tablename__ = 'course_marks'

	id = Column(Integer,primary_key=True)

	course_id = Column(Integer,ForeignKey('courses.id'),default = 1)
	# course = relationship("Course",foreign_keys=[course_id])
	student_id = Column(Integer,ForeignKey('students.id'),default = 1)

	exam = Column(String(256))
	marks = Column(Integer)
	total_marks = Column(Integer)

	def __init__(self, course_id, student_id, exam,
		marks, total_marks):

		self.course_id = course_id
		self.student_id = student_id
		self.exam = exam
		self.marks = marks
		self.total_marks = total_marks

	def getJSON(self):

		jsonDict = {}
		jsonDict['id'] = self.id
		jsonDict['exam'] = self.exam
		jsonDict['marks'] = self.marks
		jsonDict['total_marks'] = self.total_marks
		jsonDict['student_id'] = self.student_id
		jsonDict['course_id'] = self.course_id

		return jsonDict

class CourseQuiz(Base):

	__tablename__ = 'course_quiz'

	id = Column(Integer,primary_key=True)

	course_id = Column(Integer,ForeignKey('courses.id'),default = 1)
	# course = relationship("Course",foreign_keys=[course_id])

	title = Column(String(256))
	duration = Column(Integer)
	is_active = Column(Boolean,default = True)

	def __init__(self, course_id, title, duration,is_active = True):

		self.course_id = course_id
		self.title = title
		self.duration = duration
		self.is_active = is_active

	def getJSON(self):

		jsonDict = {}
		jsonDict['id'] = self.id
		jsonDict['title'] = self.title
		jsonDict['duration'] = self.duration
		jsonDict['is_active'] = self.is_active
		jsonDict['course_id'] = self.course_id

		return jsonDict

class Question(Base):
	
	__tablename__ = 'questions'

	id = Column(Integer,primary_key=True)
	question = Column(String(4096))
	option_a = Column(String(256))
	option_b = Column(String(256))
	option_c = Column(String(256))
	option_d = Column(String(256))
	correct_option = Column(Integer)

	def __init__(self, question, option_a, option_b, option_c, option_d, correct_option):

		self.question = question
		self.option_a = option_a
		self.option_b = option_b
		self.option_c = option_c
		self.option_d = option_d
		self.correct_option = correct_option

	def getJSON(self):

		jsonDict = {}
		jsonDict['id'] = self.id
		jsonDict['question'] = self.question
		jsonDict['option_a'] = self.option_a
		jsonDict['option_b'] = self.option_b
		jsonDict['option_c'] = self.option_c
		jsonDict['option_d'] = self.option_d
		jsonDict['correct_option'] = self.correct_option

		return jsonDict

class QuizQuestion(Base):
	
	__tablename__ = 'quiz_questions'

	id = Column(Integer,primary_key=True)

	course_quiz_id = Column(Integer,ForeignKey('course_quiz.id'),default = 1)
	# course_quiz = relationship("CourseQuiz",foreign_keys=[course_quiz_id])

	question_id = Column(Integer,ForeignKey('questions.id'),default = 1)
	question = relationship("Question",foreign_keys=[question_id])

	def __init__(self, course_quiz_id, question_id):

		self.course_quiz_id = course_quiz_id
		self.question_id = question_id

	def getJSON(self):

		jsonDict = {}
		jsonDict['id'] = self.id
		jsonDict['question'] = self.question.getJSON()

		return jsonDict
