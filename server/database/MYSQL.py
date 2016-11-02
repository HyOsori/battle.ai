from server.database.DBBaseClass import DBBaseClass
import pymysql


class LogDB (DBBaseClass):
    def __init__(self):
        self.conn = ''
        self.curs = ''
        self.open()

    def create_table(self):
        sql = "CREATE TABLE battle_table2(" \
              + "num int(10) not null AUTO_INCREMENT PRIMARY KEY ," \
              + "winner varchar(10)," \
              + "win_score int(5)," \
              + "loser varchar(10)," \
              + "lose_score int(5));"

        self.curs.execute(sql)

    def open(self):
        self.connect()

    def close(self):
        self.close()

    def add_game_log(self, winner, win_score, loser, lose_score):
        sql = "insert into battle_table (winner, win_score, loser, lose_score)" \
              + " VALUES ('" + winner + "'," \
              + str(win_score) + ",'" + loser + "'," + str(lose_score) + ")"
        self.curs.execute(sql)
        self.conn.commit()

    def del_game_log(self):
        self.conn = ''

    def search_game_log(self, cnt=1, name='none', win_lose='all'):
        log_dict = dict()
        if name == 'none':
            sql = "select * from battle_table ORDER BY num DESC  limit " + str(cnt)
            self.curs.execute(sql)
            db_recent = self.curs.fetchall()
            return db_recent

        else:
            if win_lose == 'all':
                sql = "select * from battle_table where winner = \"" + name + "\"" + \
                      " ORDER BY num DESC limit " + str(cnt)
                self.curs.execute(sql)
                db_win = self.curs.fetchall()

                sql = "select * from battle_table where loser = \"" + name + "\"" + \
                      " ORDER BY num DESC limit " + str(cnt)
                self.curs.execute(sql)
                db_lose = self.curs.fetchall()

                db_all = db_win + db_lose;
                db_sort = sorted(db_all, key=lambda x: (-x[0]))
                return db_sort[0:cnt]

            elif win_lose == 'win':
                sql = "select * from battle_table where winner = \"" + name + "\"" + \
                      " ORDER BY num DESC limit " + str(cnt)
                self.curs.execute(sql)
                db_win = self.curs.fetchall()
                return db_win

            elif win_lose == 'lose':
                sql = "select * from battle_table where loser = \"" + name + "\"" + \
                      " ORDER BY num DESC limit " + str(cnt)
                self.curs.execute(sql)
                db_lose = self.curs.fetchall()
                return db_lose

        self.conn.commit()

    def connect(self):
        # connect
        try:
            self.conn = pymysql.connect(
                host='localhost', user='root', password='battle',
                db='tutor_db', charset='utf8')
        except Exception, e:
            print repr(e)

        # cursor
        self.curs = self.conn.cursor()

        # check table none
        try:
            sql = "select * from battle_table ORDER BY num DESC  limit 1"
            self.curs.execute(sql)
        except Exception, e:
            print repr(e)
            if type(e) == pymysql.ProgrammingError:
                self.create_table()
