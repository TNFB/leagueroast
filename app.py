import riot_module

def main():
    liste_joueurs = []
    while True:
        print("Entrez le nom d'un joueur avec son tag (Joueur#EUW) ou 'fin' pour arrêter la saisie :")
        pseudo = input()
        if pseudo == 'fin':
            break
        if pseudo == 'debug':
            debug()
            break
        riot_id = {
            "gameName": pseudo.split("#")[0],
            "tagLine": pseudo.split("#")[1]
        }
        liste_joueurs.append(riot_id)
    
    for riot_id in liste_joueurs:
        result = riot_module.get_stats(riot_id["gameName"], riot_id["tagLine"])
        k = result[0]
        d = result[1]
        a = result[2]
        print("Nom du joueur : " + str(riot_id["gameName"]+"#"+riot_id["tagLine"]))
        print("Kills : " + str(k))
        print("Deaths : " + str(d))
        print("Assists : " + str(a))
        if d-k > k*2:
            print("AVHFIFUBZEOIFKNZNV OZENFZ GROSSE MERDE")

def debug():
    puuid = riot_module.get_summoner_puuid("Chimorin", "9649")
    last_match = riot_module.get_last_match(puuid)
    match_details = riot_module.get_match_details_for_puuid(last_match, puuid)
    print(puuid)
    print(last_match)
    print(match_details)

if __name__ == "__main__":
    main()