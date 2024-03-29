from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
"""
This creates an instance of the declarative base which cleans up the creation
of the classes.
"""
Base = declarative_base()


"""
The classes below each create tables on the database.  The School and Spell
classes have JSON serialize functions.
"""
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class School(Base):
    __tablename__ = 'school'

    id = Column(Integer)
    name = Column(String(250), primary_key=True, unique=True)
    description = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    spells = relationship("Spell", backref="School")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
                'name': self.name,
                'id': self.id,
                'description': self.description,
                'user_id': self.user_id,
                  }


class Spell(Base):
    __tablename__ = 'spell'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    school_id = Column(String(250), ForeignKey('school.name'), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'school_id': self.school_id
        }
"""
This creates an engine attached to the database.
"""
engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
"""
Adds the create_all mapper to the Base class.
"""
Base.metadata.create_all(engine)
