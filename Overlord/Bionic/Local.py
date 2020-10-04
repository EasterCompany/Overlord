from flask import Flask, request, redirect
from platform import uname
from Overlord.Bionic.Basics import local_db, randint, root


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
        self.db.commit()
        self.db.close()

    def test(self, *args):
        return "pass"

    def make_user_tables(self, *args):
        self.sql.execute("CREATE TABLE IF NOT EXISTS user_public('uid' TEXT, 'pid' TEXT, 'pkey' TEXT);")
        self.sql.execute("CREATE TABLE IF NOT EXISTS user_private('uid' TEXT, 'ukey' TEXT);")
        self.sql.execute(
            """
            CREATE TABLE IF NOT EXISTS user_data(
                'uid' TEXT, 'email' TEXT, 'mobile_number' TEXT,
                'dob' TEXT, 'region' TEXT, 'icon' TEXT, 
                'fname' TEXT, 'mname' TEXT, 'lname' TEXT, 
                'alias' TEXT
            );
            """
        )

    def uid_exists(self, uid):
        if self.sql.execute("SELECT * FROM user_private WHERE uid='" + uid + "'").fetchone() is None and \
            self.sql.execute("SELECT * FROM user_public WHERE uid='" + uid + "'").fetchone() is None:
            return False
        else:
            return True

    def connect_db(self):
        self.db = local_db()
        self.sql = self.db.cursor()

    def commit_db(self):
        self.db.commit()
        self.db.close()

    def log_user(self, user):
        self.connect_db()
        log = self.sql.execute("SELECT * FROM user_private WHERE uid='" + str(user['uid']) + "' AND ukey='" + str(user['ukey']) + "'").fetchone()
        self.db.close()
        if log is not None:
            return True
        else:
            return False

    def make_new_user(self, user):
        if isinstance(user['fname'], str) and \
          user['lname'] is not None and \
          user['passw'] is not None:
            
            def make_uid(user):
                return user['fname'][0] + user['lname'][0] + \
                    user['fname'][-1] + user['lname'][-1] + \
                    str(randint(1111, 9999))
            
            self.connect_db()
            uid = make_uid(user)
        
            while self.uid_exists(uid):
                uid = make_uid(user)
        
            self.sql.execute("INSERT INTO user_private VALUES('" + uid + "', '" + user['passw'] + "');")
            self.commit_db()
            return uid        
        else:
            return redirect('/')

    def remove_user(self, uid):
        self.connect_db()
        self.sql.execute("DELETE FROM user_private WHERE uid='" + uid + "'")
        self.sql.execute("DELETE FROM user_public WHERE uid='" + uid + "'")
        self.sql.execute("DELETE FROM user_data WHERE uid='" + uid + "'")
        self.commit_db()

    def _fetch_user_public(self, uid):
        return self.sql.execute("SELECT * FROM user_public WHERE uid='" + uid + "'").fetchone()

    def _fetch_user_private(self, uid):
        return self.sql.execute("SELECT * FROM user_private WHERE uid='" + uid + "'").fetchone()

    def fetch_user(self, uid):
        self.connect_db()
        r = {
            uid: self._fetch_user_data(uid)
        }
        self.commit_db()
        return r


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
