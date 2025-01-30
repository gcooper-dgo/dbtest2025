from db import action_queue, db_handler
import threading



def user_thread_function(data):
    # how to attach this to the end connection?
    while True:
        command = input(" >> ")

def main():

    # attach a thread to the db handler and start it
    db_thread = threading.Thread(target=db_handler)
    db_thread.start()

    # Start a user-connected thread
    # (how to attach to the end connection? socket or whatever)
    user_thread = threading.Thread(target=user_thread_function, args=('some_data',))
    user_thread.start()


if __name__=='__main__':
    main()



