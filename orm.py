from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from typing import Tuple

# database objects (ORM)
class Base(DeclarativeBase):
    def __repr__(self):
        return f"<{self.__class__.__name__}({self.id})>"

class Thing(Base):
    __tablename__ = "things"
    id: Mapped[int] = mapped_column(primary_key=True)
    color_id:Mapped[int] = mapped_column(ForeignKey('colors.id'))
    shape:Mapped[str]
    state:Mapped[bool]
    color:Mapped['Color'] = relationship()

    def __init__(self, color_id, shape="circle"):
        self.color_id = color_id
        self.shape = shape
        self.state = False

    @property
    def rgb(self):
        return self.color.rgb
    
class Color(Base):
    __tablename__ = "colors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    red: Mapped[int]
    green: Mapped[int]
    blue: Mapped[int]

    def __init__(self, rgb: Tuple[int, int, int], name:str="color") -> None:
        if len(rgb) == 3:
            r,g,b = rgb
        else:
            r,g,b = 0,0,0
        self.red = max(0, min(r,255))
        self.green = max(0, min(g,255))
        self.blue = max(0, min(b,255))
        self.name = name

    @property
    def rgb(self):
        return self.red, self.green, self.blue