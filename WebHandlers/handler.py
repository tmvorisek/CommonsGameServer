import sqlalchemy

class Handler():
    def __init__(self, cursor, params = {}):
        self.cursor = cursor
        

    def handle_connection(self, msg):
        pass

    def handle_chat(self,msg):
        """

        > handle_chat({"player_id":"12", "text": "hey guys, sup?"})
        
        """
        if len(msg["text"]) > 0:
            msg["text"] = msg["text"].replace("<","")
            self.cursor.execute(
                """INSERT INTO chat (player_id, text)
                    VALUES(%s, %s)""",
                    (str(msg["player_id"]), msg["text"]))
            return msg

        return {}

