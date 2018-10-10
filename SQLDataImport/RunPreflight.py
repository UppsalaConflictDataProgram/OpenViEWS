from __future__ import print_function
from __future__ import division
from sqlalchemy import create_engine
from sqlalchemy.sql import text as alchemy_text
import os

def preflightRUN (db_engine_name, level='pgm'):

    """
    :param db_engine_name: the Views DB URI
    :param level: the Views level to which you want to denormalize. CM and PGM are implemented
    :return: 0 on success, error code on failure.

    Runs a normal preflight run for Views, i.e. denormalizes the Views Staging tables to a flat format
    suitable for model running.
    Current implemented levels are cm and pgm.
    """

    script_path = os.path.join(os.path.dirname(os.path.realpath('__file__')), '../SQLFuelingPlans/flight_'+level.lower()+'.sql')
    try:
        preflight_file = open(script_path,'r')
    except:
        return 1

    preflight_query = alchemy_text(preflight_file.read())

    if db_engine_name is None:
        print (preflight_query)
        return 2
    else:
        engine = create_engine(db_engine_name)
        with engine.connect() as con:
            trans = con.begin()
            con.execute("DROP TABLE IF EXISTS preflight.flight_"+level.lower())
            trans.commit()
            trans = con.begin()
            print (preflight_query)
            con.execute(preflight_query)
            trans.commit()
        return 0

if __name__ == "__main__":
    err_code = preflightRUN (None,'cm')
    exit(err_code)