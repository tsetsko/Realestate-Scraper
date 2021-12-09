from sqlalchemy import Column, Integer, Unicode, UnicodeText, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlite3

engine = create_engine('real_estate_data.db', echo=True)
Base = declarative_base(bind=engine)


class Property:
	# def get_db(self):
	# 	connection = sqlite3.connect('real_estate_data.db')
	# 	cursor = connection.cursor()
	# 	cursor.execute("CREATE TABLE IF NOT EXISTS real_data (item TEXT, quantity INTEGER, price REAL)")

	__tablename__ = 'realestate_data'
	id = Column(Integer, primary_key=True)
	id_property = Column(Integer)
	date = Column(String)
	type_of_property = Column(String)
	area = Column(String)
	city_or_provice = Column(String)
	location = Column(String)
	price_per_m2 = Column(String)
	total_price = Column(String)
	published_by = Column(String)
	description = Column(String)
	link = Column(String)
	name = Column(Unicode())

	def __init__(self, id, date, type_of_property, area, city_or_provice, location, price_per_m2, total_price, published_by, description, link):
		self.id = id
		self.date = date
		self.type_of_property = type_of_property
		self.area = area
		self.city_or_provice = city_or_provice
		self.location = location
		self.price_per_m2 = price_per_m2
		self.total_price = total_price
		self.published_by = published_by
		self.description = description
		self.link = link

	# def db_commit(self):
	# 	connection = sqlite3.connect('real_estate_data.db')
	# 	connection.commit()
	# 	connection.close()


Base.metadata.create_all()

Session = sessionmaker(bind=engine)
s = Session()


