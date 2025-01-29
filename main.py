import queue
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column, relationship
from sqlalchemy import create_engine, ForeignKey
import threading
from typing import Tuple


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

# create a queue which will handle database actions
action_queue = queue.Queue()

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

# a function which will run in its own thread to constantly pop items from the action queue
def db_handler():
    sql = Session()
    while True:
        command, args, result_queue = action_queue.get()
        if command == 'STOP':
            break
        try:
            # try to run the command on the session with the specified args
            result = command(sql, *args)
            # put the result to the result queue
            result_queue.put(result)
        except Exception as e:
            # if something went weird, put the error to the result queue
            result_queue.put(e)


def send_command_to_db(command, *args):
    result_queue = queue.Queue()
    action_queue.put((command, args, result_queue))
    return result_queue.get()

def example_command(session, data):
    return session.query(Thing).all()

def user_thread_function(data):
    # how to attach this to the end connection?
    result = send_command_to_db(example_command, data)
    print(result)

def main():

    # attach a thread to the db handler and start it
    db_thread = threading.Thread(target=db_handler)
    db_thread.start()

    # Start a user-connected thread
    # (how to attach to the end connection? socket or whatever)
    user_thread = threading.Thread(target=user_thread_function, args=('some_data',))
    user_thread.start()

    # Stop the DBThread when done
    action_queue.put(('STOP', None, None))
    db_thread.join()

if __name__=='__main__':
    main()


