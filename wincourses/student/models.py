from sqlalchemy import Column,Integer

from ..models import Base,DBSession

from sqlalchemy.types import String
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship

from ..institute.models import Institute

class Student(Base):
    
    __tablename__ = 'students'
    
    id = Column(Integer,primary_key=True)
    name = Column(String(256))
    email = Column(String(256),nullable = False)
    
    institute_id = Column(Integer,ForeignKey('institutes.id'),default = 1)
    institute = relationship("Institute",foreign_keys=[institute_id])
    
    institute_roll_num = Column(String(64))
    password = Column(String(256))
    
    def __init__(self,
                 name,
                 email,
                 institute_id,
                 institute_roll_num,
                 password):
        
        self.name = name
        self.email = email
        self.institute_id = institute_id
        self.institute_roll_num = institute_roll_num
        self.password = password
        
    def getJSON(self):
        
        jsonDict = {}
        jsonDict['id'] = self.id
        jsonDict['name'] = self.name
        jsonDict['institute_id'] = self.institute_id
        jsonDict['institute_roll_num'] = self.institute_roll_num
        jsonDict['email'] = self.email
        
        return jsonDict
