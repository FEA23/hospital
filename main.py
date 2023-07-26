from hospital import Hospital
from session import Session


if __name__ == '__main__':
    hospital = Hospital()
    session = Session(hospital)
    session.start()
