from sqlalchemy import Column, Integer, Float, ARRAY, Index
from app.db.base import Base


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, autoincrement=True)
    depth = Column(Float)
    pixels = Column(ARRAY(Integer))

    __table_args__ = (
        Index('ix_images_depth', 'depth'),  # Create an index on the depth column
    )
