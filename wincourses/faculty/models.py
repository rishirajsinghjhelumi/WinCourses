from sqlalchemy import Column,Integer

from ..models import Base,DBSession

from sqlalchemy.types import String
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship

from ..institute.models import Institute

class Faculty(Base):

	__tablename__ = 'faculty'

	id = Column(Integer,primary_key=True)
	name = Column(String(256))
	email = Column(String(256),nullable = False)
    
	institute_id = Column(Integer,ForeignKey('institutes.id'),default = 1)
	institute = relationship("Institute",foreign_keys=[institute_id])
    
	title = Column(String(64))

	def __init__(self,
				name,
				email,
				title,
				institute_id):
        
		self.name = name
		self.email = email
		self.title = title
		self.institute_id = institute_id

	def getJSON(self):

		jsonDict = {}
		jsonDict['id'] = self.id
		jsonDict['name'] = self.name
		jsonDict['title'] = self.title
		jsonDict['institute_id'] = self.institute_id
		jsonDict['email'] = self.email

		return jsonDict