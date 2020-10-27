from time import time
from platform import uname
from hashlib import sha256
from random import randint
from urllib import parse as urlparse
from flask import Flask, request, redirect
from .Crypt import spice
from .Basics import local_db, root


class __Server__:
    app = Flask(
        __name__,
        static_url_path='/',
        static_folder='./Static',
        root_path=root
    )

    def __init__(self):
        self.os = uname().system
        self.db = local_db()
        self.name = uname().node
        self.request = request
        self.goto = redirect
        self.sql = self.db.cursor()
        self.make_user_tables()
        self.purge_old_tokens()
        self.db.commit()
        self.db.close()

    @staticmethod
    def test():
        return "pass"

    def purge_old_tokens(self):
        self.sql.execute(
            "DELETE FROM user_tokens WHERE expires<={current_time}".format(
                current_time=int(time())
            )
        )

    def make_user_tables(self):
        self.sql.execute("CREATE TABLE IF NOT EXISTS user_private('uid' TEXT, 'email' TEXT, 'passw' TEXT);")
        self.sql.execute("CREATE TABLE IF NOT EXISTS user_tokens('uid' TEXT, 'token' TEXT, 'expires' INT);")
        self.sql.execute(
            """
            CREATE TABLE IF NOT EXISTS user_data(
                'uid' TEXT, 'mobile_number' TEXT,
                'dob' TEXT, 'region' TEXT, 'icon' TEXT, 
                'fname' TEXT, 'mname' TEXT, 'lname' TEXT, 
                'alias' TEXT
            );
            """
        )

    def uid_exists(self, uid):
        if self.sql.execute("SELECT * FROM user_private WHERE uid='" + uid + "'").fetchone() is None:
            return False
        else:
            return True

    def email_exists(self, email):
        self.connect_db()
        r = self.sql.execute("SELECT * FROM user_private WHERE email='" + email + "'").fetchone()
        self.db.close()
        if r is None:
            return False
        else:
            return True

    def connect_db(self):
        self.db = local_db()
        self.sql = self.db.cursor()

    def commit_db(self):
        self.db.commit()
        self.db.close()

    @staticmethod
    def parse_user(user):
        return {
            'email': urlparse.unquote(user['email']),
            'passw': urlparse.unquote(user['passw'])
        }

    def log_user(self, user):
        self.connect_db()

        pas = sha256(
                user['passw'].encode()
            ).hexdigest()
        
        log = self.sql.execute(
            "SELECT * FROM user_private WHERE email='{email}' AND passw='{pas}'".format(
                email=user['email'],
                pas=pas
            )
        ).fetchone()

        if log is not None:
            new_token = spice(log[0])
            self.sql.execute(
                "INSERT INTO user_tokens VALUES('{uid}', '{token}', {expires})".format(
                    uid=log[0],
                    token=new_token,
                    expires=int(time() + (60 * 60 * 24 * 30))
                )
            )
            self.commit_db()
            return new_token
        else:
            self.db.close()
            return None

    def make_new_user(self, user):
        if user['email'] is not None and \
           user['passw'] is not None and \
           len(user['email']) >= 5 and \
           len(user['passw']) >= 8 and \
           '@' in user['email'] and '.' in user['email']:
            
            if self.email_exists(user['email']):
                return "Email already in use."

            def make_uid():
                return str(
                    randint(111111111111, 
                            999999999999
                    )
                )
            
            self.connect_db()
            uid = make_uid()
            pas = sha256(
                user['passw'].encode()
            ).hexdigest()

            while self.uid_exists(uid):
                uid = make_uid(user)
        
            self.sql.execute("INSERT INTO user_private VALUES('{uid}', '{email}', '{passw}');".\
                format(
                    uid=uid, email=user['email'], passw=pas
                )
            )
            self.commit_db()
            return 'success!'
        else:
            return redirect('/')

    def remove_user(self, uid):
        self.connect_db()
        self.sql.execute("DELETE FROM user_private WHERE uid='" + uid + "'")
        self.sql.execute("DELETE FROM user_public WHERE uid='" + uid + "'")
        self.sql.execute("DELETE FROM user_data WHERE uid='" + uid + "'")
        self.commit_db()

    def _fetch_user_private(self, uid):
        return self.sql.execute("SELECT * FROM user_private WHERE uid='" + uid + "'").fetchone()


Server = __Server__()


class __Index__:

    def __init__(self):
        self.add = Server.app.route

    @staticmethod
    def __request_arg__(arg):
        try:
            return request.args.get(arg)
        except Exception as arg_error:
            return arg_error

    def urp(self, *args):
        results = {}
        for arg in args:
            results[arg] = self.__request_arg__(arg)
        return results
    
    @staticmethod
    def goto(path):
        return redirect(path)


Index = __Index__()
