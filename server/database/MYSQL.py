from server.database.DBBaseClass import DBBaseClass
import pymysql

class LogDB (DBBaseClass):
    def __init__(self):
        self.conn = ''
        self.curs = ''

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
              + "VALUES ('" + winner + "'," \
              + str(win_score) + ",'" + loser + "'," + str(lose_score) + ")"
        self.curs.execute(sql)

        sql = "select * from battle_table ORDER BY num DESC  limit 1"
        self.curs.execute(sql)
        db_game = self.curs.fetchall()

        self.conn.commit()

    def del_game_log(self):
        self.conn = ''

    def search_game_log(self, name):
        self.connect()

        sql = "select * from battle_table where winner = '" + name + "'"
        self.curs.execute(sql)
        db_win = self.curs.fetchall()

        sql = "select * from battle_table where loser = '" + name + "'"
        self.curs.execute(sql)
        db_lose = self.curs.fetchall()

        print db_win
        print db_lose

        self.conn.commit()

    def search_game_log_recent(self):
        self.connect()

        sql = "select * from battle_table ORDER BY num DESC  limit 20"
        self.curs.execute(sql)
        db_recent = self.curs.fetchall()

        self.conn.commit()

    def connect(self):
        # connect
        try:
            self.conn = pymysql.connect(host='localhost', user='root', password='battle',
                                    db='tutor_db', charset='utf8')
        except Exception, e:
            print repr(e)

        # cursor
        self.curs = self.conn.cursor()

        try:
            sql = "select * from battle_table ORDER BY num DESC  limit 1"
            self.curs.execute(sql)

        except Exception, e:
            print repr(e)
            if type(e) == pymysql.ProgrammingError:
                self.create_table()
