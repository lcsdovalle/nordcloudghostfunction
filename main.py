from helpers.authApi import authService
import json
import sqlalchemy
from sqlalchemy.sql import select
import os

#------------------------------------------------------------------#
# Key for running the routine
#------------------------------------------------------------------#
key = "fa47c14adc939ee35190cec22d429263"


#------------------------------------------------------------------#
# Get instance information
#------------------------------------------------------------------#
escopo = [
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/sqlservice.admin'
    ]
service = authService(escopo,"dbadmin.json").getService('sqladmin','v1beta4')
try:
    req = service.instances().list(project=os.environ.get('GCP_PROJECT'))
    resp = req.execute()
    r = resp.get('items')[0]
    connName = r.get('connectionName')
    instanceName = r.get('name')
    region = r.get('region')
    project = r.get('project')
except Exception as e:
    print(e)



def cleanUpDB(request):
    #------------------------------------------------------------------#
    # Verify the key
    #------------------------------------------------------------------#
    content_type = request.headers['content-type']
    if content_type == 'application/json':
        request_json = request.get_json(silent=True)
        if request_json and 'key' in request_json:
            req_key = request_json['key'] or None
            if not req_key or req_key != key:
                return {"Forbidden":"Access denied!"}, 403
        else:
           return {"Error":"You gotta send a json!"}, 400
    #------------------------------------------------------------------#
    # Connect to the instance
    #------------------------------------------------------------------#
    db_name = "ghost"
    db_user = "root"
    db_password = "zxzx1212"
    connection_name = connName
    try:
        driver_name = 'mysql+pymysql'
        query_string = dict({"unix_socket": "/cloudsql/{}".format(connection_name)})        
        db = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername=driver_name,
            username=db_user,
            password=db_password,
            database=db_name,
            query=query_string,
        ),
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800
        )

        try:
            #------------------------------------------------------------------#
            # Delete all the posts from the database
            #------------------------------------------------------------------#
            with db.connect() as conn:         
                q = sqlalchemy.text('SET FOREIGN_KEY_CHECKS = 0')
                result = conn.execute(q)
                q = sqlalchemy.text('truncate table posts_authors')
                result = conn.execute(q)
                q = sqlalchemy.text('truncate table posts')
                result = conn.execute(q)
                q = sqlalchemy.text('truncate table posts')
                result = conn.execute(q)
                q = sqlalchemy.text('SET FOREIGN_KEY_CHECKS = 1')
                return {"result":"All the posts has been deleted"},201
        except Exception as e:
            return {"error":str(e)},400

    except Exception as e:
        print(e)
