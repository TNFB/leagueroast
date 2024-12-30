playerList = []

def add_player(riot_id):
    player = {
        "gameName": riot_id.split("#")[0],
        "tagLine": riot_id.split("#")[1]
    }
    playerList.append(player)

def remove_player(riot_id):
    player = {
        "gameName": riot_id.split("#")[0],
        "tagLine": riot_id.split("#")[1]
    }
    playerList.remove(player)