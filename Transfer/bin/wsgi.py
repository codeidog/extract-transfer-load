from transfer import app, engine
from database import create_tables
import argparse
import logging

create_tables(engine=engine)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Server that accepts list of files, and upload their name to a datbase if they are not corrupted')
    parser.add_argument("--log", const=True, default='INFO', nargs='?', help="Log level")    
    args = parser.parse_args()        
    logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=getattr(logging, str(args.log).upper())
    )

    #Create the tables if are not present in the database
    
    app.run()