# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division
from sqlalchemy import create_engine
from sqlalchemy.sql import text as alchemy_text
from time import time
import sys



def monthid_to_ymd(month_id, db_engine_name='postgresql://VIEWSADMIN@VIEWSHOST:5432/views'):
    '''given month_id, return Y-M-01 in ISO format'''
    engine = create_engine(db_engine_name)
    with engine.connect() as con:
        query = alchemy_text("SELECT month, year_id FROM staging.month WHERE id=:id")
        try:
            result = con.execute(query,id=int(month_id)).fetchone()
            result = '{1:04d}-{0:02d}-01'.format(*result)
        except: result = None
        return result




def date_to_monthid(*args,**kwargs):
    '''if called with date parse ISO string to Y-M-D and return month_id.
       if called with year,month,day obtain return month_id
       and if called with only an actual month_id, guess what, pass through!'''
    db_engine_name = 'postgresql://VIEWSADMIN@VIEWSHOST:5432/views'
    if 'db_engine_name' in kwargs:
        db_engine_name = kwargs['db_engine_name']

    if len(args) not in (1,3): return None

    if len(args)==1:
        if '-' not in args[0]:
            try: passthrough = int(args[0])
            except: passthrough = None
            return passthrough
        ymd=args[0].split('-')
        if len(ymd) != 3: return None
        try:
            y=int(ymd[0])
            m=int(ymd[1])
        except ValueError:
            return None
    if len(args)==3:
        try:
            y=int(args[0])
            m=int(args[1])
        except ValueError:
            return None

    engine = create_engine(db_engine_name)
    with engine.connect() as con:
        query = alchemy_text("SELECT id FROM staging.month WHERE year_id=:y and month=:m")
        try:
            result = con.execute(query,y=y, m=m).fetchone()
            return result[0]
        except: return None


    #print (len(args),db_engine_name)


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, bar_length = 100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()


def backupOldTable (db_engine_name='postgresql://VIEWSADMIN@VIEWSHOST:5432/views',
               schema_name='dataprep',
               table_name='ged'):
    '''
    creates a backup copy of a table with the name TABLEnnnnnnn where n is unix timestamp
    :param db_engine_name engine URI
    :param schema_name schema
    :param table_name
    '''

    ot = schema_name+'.'+table_name
    nt= schema_name+'.'+table_name+'_'+str(int(time()))
    query = alchemy_text('CREATE TABLE '+nt+' AS SELECT * FROM '+ot)

    engine = create_engine(db_engine_name)

    with engine.connect() as con:
        con.execute(query)

if __name__ == "__main__":
    exit('This should not be called directly')