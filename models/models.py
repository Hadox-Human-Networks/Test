from werkzeug.security import check_password_hash
from flask_login import UserMixin
from ..helper.load_data import connection_to_postgres

class User(UserMixin):
    def __init__(self, id=None, email=None, password=None, username=None, creation_date=None, role_id=None):
        self.id=id
        self.email = email
        self.password = password
        self.username = username
        self.creation_date = creation_date
        self.role_id= role_id

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)

class ModelUser():
    
    @classmethod
    def login(self, user):
        cur = connection_to_postgres()
        try:
            query_SQL = """SELECT id, email, password_hash, username, creation_date, role_id 
                FROM emo_users.users WHERE email = '{}'""".format(user.email)
            cur.execute(query_SQL) 
            row = cur.fetchone()
            if row != None:
                user = User(row[0], row[1], User.check_password(row[2], user.password), row[3], row[4], row[5])
                return user
            else: 
                return None
        except Exception as ex:
            raise Exception(ex)       

    @classmethod
    def get_by_id(self, id):
        cur = connection_to_postgres()
        try: 
            query = """SELECT id, email, username FROM emo_users.users WHERE id = {}""".format(id)
            cur.execute(query)
            row = cur.fetchone()
            if row != None:
                user = User(row[0], row[1], row[2])
                return user
            else: 
                return None
        except Exception as ex:
            raise Exception(ex)


