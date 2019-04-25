from sqlalchemy import (Table, Column, select, insert, update, create_engine,
                        Integer, String, Sequence, MetaData, func, literal)
import uuid

metadata = MetaData()


class DBManager():
    def __init__(self):
        self.connect("postgres","pass123","commons")

    def get_move_num(self, player_id):
        move_table = self.meta.tables['move']
        moves = move_table.select().where(
            move_table.c.player_id == player_id).execute().fetchall()

    def store_move(self, player_id, summit_id, move):
        move_table = self.meta.tables['move']
        move_table.insert().values(
            player_id=player_id,
            summit_id=summit_id,
            harvest=move).execute()

    def get_summit_index(self, summit_id, game_id):
        summit_table = self.meta.tables['summit']
        index = select([func.count(summit_table.c.id)]).where(
            summit_table.c.game_id == game_id).where(
            summit_table.c.id <= summit_id).execute().fetchone()[0]
        return index

    def get_summit_id(self, summit_index, game_id):
        summit_table = self.meta.tables['summit']
        summits = select([summit_table.c.id]).where(
            summit_table.c.game_id == game_id).order_by(
            summit_table.c.id).execute().fetchall()

        i = 0
        for s in summits:
            if i == summit_index:
                return s[0]
            else:
                i += 1

    def new_summit(self, game_id, commons_index):
        summit_table = self.meta.tables['summit']
        summit_table.insert().values(
            game_id = game_id,
            commons_index = 0).execute()



    def get_chats(self, game_id):
        chat_table = self.meta.tables['chat']
        player_table = self.meta.tables['player']
        summit_table = self.meta.tables['summit']
        summits = summit_table.select().where(
            summit_table.c.game_id == game_id).execute().fetchall()
        chat_log = []
        for r in summits:
            chat_log.append(chat_table.join(player_table, 
                chat_table.c.player_id == player_table.c.id).select(
                chat_table.c.summit_id == r[2]).execute().fetchall())
        return chat_log


    def store_chat(self, obj):
        chat_table = self.meta.tables['chat']
        chat_table.insert().values(
            player_id=obj['player_id'],
            text=obj['text'],
            summit_id=obj['summit_id']).execute()


    def set_name(self, player_id, name_string):
        player_table = self.meta.tables['player']
        player_table.update().values(name=name_string).where(
            player_table.c.id==player_id).execute()

    def get_pass_list(self):
        player_table = self.meta.tables['player']
        pass_list = select([player_table.c.password]).execute().fetchall()
        # pass_list is actually a list of tuples with empty [1]s
        return [p[0] for p in pass_list] # returns a regular list instead

    def check_pass(self, pass_string):
        player_table = self.meta.tables['player']
        player = player_table.select().where(
            player_table.c.password==pass_string).execute().fetchone()
        if(player!=None):
            return player[0]
        return False

    def get_player_details(self, player_id):
        player_table = self.meta.tables['player']
        summit_table = self.meta.tables['summit']
        move_table = self.meta.tables['move']

        player_details = player_table.select().where(
            player_table.c.id == player_id).execute().fetchone()
        summit_details = summit_table.select().where(
            summit_table.c.id==player_details[1]).execute().fetchone()
        summit_num = select([func.count(summit_table.c.id)]).where(
            summit_table.c.game_id == summit_details[2]).where(
            summit_table.c.id <= player_details[1]).execute().fetchone()
        move_details = move_table.select().where(
            move_table.c.player_id == player_id).execute().fetchall()
        players_dump = select([player_table.c.id,player_table.c.name]).where(
            player_table.c.summit_id.in_(select([summit_table.c.id]).where(
                summit_table.c.game_id == summit_details[2]))).order_by(
            player_table.c.id).execute().fetchall()

        players = []
        for p in players_dump:
            player = [p[0],None]
            if p[1]:
                player[1] = str(p[1])

            players.append(player)

        player_index = 0
        for p in players:
            if p[0] < player_id:
                player_index += 1

        return {"player_id":player_details[0],
                "player_index":player_index,
                "game_id":summit_details[2],
                "move_num":len(move_details),
                "summit_id":player_details[1],
                "summit_num": summit_num[0],
                "name":player_details[2],
                "worth":player_details[3],
                "players":players,
                "type":"connection"}

    def load_games(self):
        game_table = self.meta.tables['game']
        summit_table = self.meta.tables['summit']
        player_table = self.meta.tables['player']
        move_table = self.meta.tables['move']
        games_list = {}

        for g in select([game_table.c.id]).execute().fetchall():
            summits = select([summit_table.c.id]).where(
                summit_table.c.game_id == g[0]).execute().fetchall()
            games_list[g[0]] = {"players":[], "moves":[]}
            r_list = []
            for r in summits:
                p_ids = select([player_table.c.id]).where(
                    player_table.c.summit_id == r[0]).order_by(
                    player_table.c.id).execute().fetchall()
                players = [player[0] for player in p_ids]
                player_indexes = {}
                i = 1
                for p in players:
                    player_indexes[p] = i
                    i += 1
                for p in players:
                    games_list[g[0]]["players"].append(p)
                    moves_dump = move_table.select().where(
                        move_table.c.player_id == p).execute().fetchall()
                    for m in moves_dump:
                        summit_index = select([func.count(summit_table.c.id)]).where(
                            summit_table.c.game_id == g[0]).where(
                            summit_table.c.id <= m[2]).execute().fetchone()[0]
                        move = {"id":m[0],
                            "player_id":m[1],
                            "game_id":g[0],
                            "player_index":int(player_indexes[m[1]]) - 1,
                            "summit_id":m[2],
                            "summit_index":int(summit_index)-1,
                            "harvest":m[3]}
                        games_list[g[0]]["moves"].append(move)

        return games_list

    def create_games(self, games_arr):
        self.clear_database()
        game_table = self.meta.tables['game']
        summit_table = self.meta.tables['summit']
        player_table = self.meta.tables['player']
        for game in games_arr:
            game_table.insert().values().execute()

        i = 0
        for game in game_table.select().execute().fetchall():
            summit_table.insert().values(game_id = game[0]).execute()
            summit = summit_table.select().order_by(
                summit_table.c.id.desc()).execute().fetchall()[0]
            for player in range(0,games_arr[i]):
                player_table.insert().values(
                    summit_id=summit[0],password=uuid.uuid4()).execute()
            i+=1

    def clear_database(self):
        login_table = self.meta.tables['login']
        game_table = self.meta.tables['game']
        move_table = self.meta.tables['move']
        player_table = self.meta.tables['player']
        chat_table = self.meta.tables['chat']
        summit_table = self.meta.tables['summit']
        rule_table = self.meta.tables['rule']
        vote_table = self.meta.tables['vote']
        login_table.delete().where(player_table.c.id!=-1).execute()
        game_table.delete().where(game_table.c.id!=-1).execute()
        move_table.delete().where(player_table.c.id!=-1).execute()
        player_table.delete().where(player_table.c.id!=-1).execute()
        chat_table.delete().where(player_table.c.id!=-1).execute()
        summit_table.delete().where(player_table.c.id!=-1).execute()
        rule_table.delete().where(player_table.c.id!=-1).execute()
        vote_table.delete().where(player_table.c.id!=-1).execute()

    def connect(self, user, password, db, host='localhost', port=5432):
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(user, password, host, port, db)
        self.con = create_engine(url, client_encoding='utf8')
        self.meta = MetaData(bind=self.con, reflect=True)

    #sends chat to data base
    def send_chat(self, msg):
        game_table = self.meta.tables['chat']
        self.con.execute(game_table.insert().values(player_id = 1,text=msg["text"], game_id=1))

