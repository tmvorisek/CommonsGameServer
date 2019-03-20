from sqlalchemy import insert, update

class Handler():
    def __init__(self, cursor, params = {}):
        self.cursor = cursor

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

