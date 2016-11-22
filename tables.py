from sqlalchemy import Column, Integer, String, ForeignKey

class Crops(Base):
	__tablename__ = 'crops'

	id = Column(Integer, primary_key=True)
	farmerID = Column(Integer, ForeignKey('far.id'))
	cropID = Column(Integer, ForeignKey('masterCropList.id'))
	dateCreated = Column(date)
	dateHarvested = Column(date)
	cropYield = Column(Integer)
	deleteFlage = Column(boolean)


class MasterCropList(Base):
	__tablename__ = 'masterCropList'

	id = Column(Integer, primary_key=true)
	crop = Column(String)
	cropDescription = Column(String)

class Aret(Base):
    __tablename__ = "aretUsers"

    id = Column(Integer, primary_key=True)
    POBox = Column(Integer)
    locality_name = Column(Integer)
    deliver_indicator = Column(Integer)
    user_type = Column(Integer)
    username = Column(String)
    lname = Column(String)
    fname = Column(String)
    password = Column(String)
    phoneNum = Column(Integer)
    age = Column(Integer)

class Farmer(Base):
    __tablename__ = "farmerUsers"

    id = Column(Integer, primary_key=True)
    region_id = Column(Integer)
    username = Column(String)
    lname = Column(String)
    fname = Column(String)
    password = Column(String)
    phoneNum = Column(Integer)
    age = Column(Integer)

class Files(Base):
	__tablename__ = "files"
    id = Column(Integer, primary_key=True)
    aret_id = Column(Integer, ForeignKey('aretUsers.id'))
    url = Column(String)
    size = Column(Integer)
    tag = Column(String)
