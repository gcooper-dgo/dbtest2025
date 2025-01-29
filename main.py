from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column
from sqlalchemy import create_engine, ForeignKey

SQL_USER = 'test'
SQL_PASS = 'Test Database User 2025'
ADDRESS = 'localhost'
DATABASE = 'test'

connection_string = (
    f"mssql+pymssql://{SQL_USER}:{SQL_PASS}"
    f"@{ADDRESS}/{DATABASE}"
)
engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)
sql = Session()


class Base(DeclarativeBase):
    def __repr__(self):
        return f"<{self.__class__.__name__}({self.id})>"

class Thing(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    color_id:Mapped[int] = mapped_column(ForeignKey('colors.id'))

class Color(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    red: Mapped[int]
    green: Mapped[int]
    blue: Mapped[int]

    @property
    def rgb(self):
        return (self.red, self.green, self.blue)



