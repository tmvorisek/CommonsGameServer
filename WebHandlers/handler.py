from sqlalchemy import insert, update, create_engine

engine = create_engine('postgresql://postgres:pass123@localhost/commons')

class Handler():
    def __init__(self, player_count, params = {}):
        games_arr = self.compute_game_players_counts(player_count)


    def compute_game_players_counts(self, player_count):
        rem = player_count % 8
        groups = int(player_count / 8)
        games = []
        for i in range(0,groups):
            games.append(8)
        if (rem < 4):
            i = 0
            while rem > 0:
                games[i] += 1
                rem -= 1
                i += 1
                if i >= len(games):
                    i = 0
        elif (rem >= 4):
            games.append(rem)

        return games

    def open(self,msg):
        # self.id = self.get_argument("Id")
        self.stream.set_nodelay(True)
        clients[self.id] = {"id": self.id, "object": self}
        msg = json.dumps({"name":"commons", "number":str(self.id), "type":"connect"})
        broadcast(msg)
        cursor.execute("INSERT INTO player (round_id, name, worth, password) VALUES (%s,%s,%s,%s)", (2, "JohnnyQ", 0, "blah"))
    
    def close(self, id):
        pass


    def connection(self, msg):
        pass
        # cursor.execute("""SELECT player.name, text, time 
            # FROM chat 
            # INNER JOIN player ON player.id = chat.player_id 
            # ORDER BY time ASC LIMIT 1000;""")
        # chat_log = cursor.fetchall()
        # for log in chat_log:
        # self.write_message(json.dumps({"name":log[0], "text":log[1], "type":"chat"}))


    def move(self, msg):
        pass

    def chat(self,msg):
        """

        > handle_chat({"player_id":"12", "text": "hey guys, sup?"})
        
        """
        if len(msg["text"]) > 0:
            msg["text"] = msg["text"].replace("<","")

            self.cursor.execute(
                """INSERT INTO chat (player_id, text, game_id)
                    VALUES(%s,%s,1)""",
                    (6, msg["text"]))
            return msg
        return {}

