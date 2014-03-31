from sqlalchemy import Column,Integer

from ..models import Base,DBSession

from sqlalchemy.types import String
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship

class Institute(Base):

	__tablename__ = 'institutes'

	id = Column(Integer,primary_key=True)
	name = Column(String(256))

	def __init__(self,name):

		self.name = name

	def getJSON(self):

		jsonDict = {}
		jsonDict['id'] = self.id
		jsonDict['name'] = self.name

		return jsonDict