import logging
from sqlalchemy.orm import session
from sqlalchemy import create_engine
from database import Heartbeat, create_engine, create_session, File, _get_date, create_tables
from flask import Flask, request
import argparse
import socket
import os

#Connect to the databse engine
db_server = os.environ['DB_SERVER']
db_name = os.environ['DB_NAME']
db_user = os.environ['DB_USER']
db_pwd = os.environ['DB_PWD']
db_string = f'postgresql://{db_user}:{db_pwd}@{db_server}/{db_name}'
engine = create_engine(db_string)
create_tables(engine=engine)
app = Flask(__name__)
req_count = 0

@app.route("/sendfiles", methods=['post'])
def sendfiles():
    #Check that request has not exceeded 4
    global req_count
    if(req_count >= 4):
        return {'Messge':'Max number of allowed request exceeded please wait a while'}, 401
    req_count+=1
    app.logger.debug('Parsing list of files')
    body = request.get_json(force=True) 
    corrupted_files = []    
    messgae = ''
    status_code = 200
    #Iterate over the files and load only valid ones
    session = create_session(engine=engine) #Connect to the database
    try:
        for key,value in body["files"].items():
            if(value is False):                
                app.logger.warn(f'File {key} is corrupted and will not be loaded to the database')
                corrupted_files.append(key)
            elif(value is True):
                app.logger.debug(f'File {key}. Adding it to the database')
                file = File(name=key)            
                session.add(file)
                session.commit()
        message = f'The following corrupted files were not loaded {corrupted_files}'
    except Exception as e:
        app.logger.error(e)
        message = e
        status_code=500
    session.close()
    req_count-= 1
    return {'Message':message}, status_code

@app.route("/heartbeat", methods=['get'])
def heartbeat():
    try:
        session = create_session(engine=engine)
        hostname = socket.gethostname()    
        heartbeat_server = session.query(Heartbeat).filter_by(hostname=hostname)
        if(heartbeat_server.count() > 0):
            date = _get_date()
            heartbeat_server.update({'time':date})
        else:
            heartbeat = Heartbeat(hostname=hostname)
            session.add(heartbeat)        
        session.commit()
        session.close()
        return {
            'Messge:':'I am alive',
            'Description': ' value update in the database'
        }
    except Exception as e:
        app.logger.error(f'Exception while writing heartbeat to the datbase: {e}')
        return {
            'Message':'I am alive',
            'Description': 'An error occurred while writing to the datbase'
        }

    
    

#For local debugging
if __name__ == '__main__':
    #Parse commandline args
    app.logger.setLevel(logging.DEBUG)
    app.run()    

#Production use from Gunicorn
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)    