import queue
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from orm import Thing, Color

SQL_USER = 'test'
SQL_PASS = 'Test Database User 2025'
ADDRESS = 'localhost'
DATABASE = 'test'

connection_string = (
    f"mssql+pymssql://{SQL_USER}:{SQL_PASS}"
    f"@{ADDRESS}/{DATABASE}"
)
engine = create_engine(connection_string)
Session = scoped_session(sessionmaker(bind=engine))

# create a queue which will handle database actions
action_queue = queue.Queue()

def send_command_to_db(command, *args):
    action_queue.put((command, args))    

def example_command(session, data):
    return session.query(Thing).all()



# a function which will run in its own thread to constantly pop items from the action queue
def db_handler():
    sql = Session()
    while True:
        subject, action, target, arg = action_queue.get()
        if action == 'STOP':
            break
        do(subject, action, target, arg)
        sql.commit()

 

class Actions():
    def color(subject, target, arg):
        target.color=arg
        pass

def do(subject, action, target, arg):
    do_action=getattr(Actions, action, None)
    if do_action: do_action(subject=subject, target=target, arg=arg)
    else:
        print(f"* BUG *: action '{action}' not implemented.")
        raise NotImplementedError
