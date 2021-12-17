import pandas as pd
import json
from pprint import pprint
import matplotlib.pyplot as plt

import names


def calculate_probs(w_elo, l_elo):
    return 1 / (1 + 10**((w_elo - l_elo) / 400))

# def calculate_probs(w_elo, l_elo):
#     return w_elo / (w_elo + l_elo) bonjour? Essa vida???? Cette vie?!?!?! Ise Buena xd Isto é tenis? Yas, pensavas que era o quê? xd
# Estou a brincar, eu já mudo para plog xD :(
# Eu só meti o tenis porque É mais fixe, mas pronto vamos ter de sair da aula xD
# Até já então xd  <3 SOu capaz de demorar 20 minutos só? tu consegues vir aqui ter sem te perderes!?!?!?!??!?!?!?!?!?!P?!?!?!?!?!?!
# Isso já não consigo garantir xD
# O stor deve estar aí na aula a ver teescrever bué rápido e a pensar: Nossa, aquele gajo é que programa, alguém pare o homem que ele está possuido xD
# Ele foi a uma gaja que tu conheces que obviamente eu já não me lembro do nome dela xd e ela disse:
# Oh sô pssô eu já fiz o projeto o ano passado, não posso usar o que já fiz? :chorão: Não me acredito xdxdxd
# Juro que é verdade xD Que gaja estúpida. É uma loira de óculos não? Exatamente xD É a Carolina, é uma brasielira rrrrosqueeee xD
# Por acaso pareceu me braSileiro <- (ninguém viu)(tou cegoooo) xd o sotaque dela
# O trabalho de plog hoje está a andar de carago
# Mesmo nós estamos a progredir de uma maneira que ninguém ia conseguir sequer imaginar xD Estamos a pegar fogo mesmo
# O meu pc até está a ficar com as teclas encravadas xD As ventoinhas do meu predador até estão ao pics com o ar condicionado xD
# Agora estás sempre com o ar condicionado ligado? Por acaso nem estou, era só pra piada mesmo xd
# Pensei que tinhas gostado da ideia e agora já era rotina xD Not, ainda só usei uma vez e foi dessa vez que estavas comigo, nunca mais
# Ah okz, gostei do facto de eu ter estado presente nesse primeiro acontecimento importante xD <3 <3
# E não quero tê lo ligado agora para ver como me sinto, se sentir frio é cuvides xd E se sentir calor se calhar é cuvides também
# Oh diabo, então espero que não tenhas frio nem calor para o resto da tua vida xD
# coitado do covid, ele também merece viver, não é filho de Deus também?
# É capaz e se for vamos todos quinar xD A foda é que vou ter de pagar 20 euros por cada noite que ele aqui dormir comigo porque não posso ter convidados xD
# Que boa xD Eu demorei uma beca a perceber xD Desculpa me, devia ter avisado que esta piada era nivel de scrum master xd
# O meu nível é só de developer xD
# Olhei agora para cima, Jesus, quem é que escreveu isto tudo? xd
# Nós estamos a programar a um ritmo que nem é imaginável xD
# Houve outra gaja que fez a mesma pergunta ao sô pssô xD Está tudo maluquinho? xd
# Completamente, aparentemente somo só nós os duros que já estamos habituados ao chumbo xD É um talento desenvolvido ao longo dos anos
# Exato, a esta altura já devemos estar subdesenvolvidos xD xd Chumbar tornou se rotineiro, é como ir à missa ao domingo xd
# Que boa xD Espera, lembrei me agora doutra mesmo boa... :olhinhos:
# :tambores............. xD: era fazer um trabalhinho de plog (tens de ler isso como se fosse eu a dizer daquela maneira especifica xd)
# Era mesmo isso que fiz e estou a passar uma beca mal xD xd
# (momento de recuperação) xd
# Então só vai fazer plog ou tens alguma ideia mais fixe? TENHO, mas se calhar é melhor fazer plog xd
# Okz, então vou ter de te, infelizmente, expulsar desta sessão momentaneamente para passar à sessão mais rosque >:(
# Desculpa me, não sou eu que faço as regras o'o (isto era o chorão, mas não correu tão bem como eu estava a pensar XD ADEUS ADEUS) Só vai



def prob_to_odd(prob):
    return prob / (1 - prob) + 1


def sim_tournament(filename, jsonname, money):
    elo_ratings_file = open(jsonname)
    elo_ratings_dict = json.load(elo_ratings_file)

    tour = pd.read_csv(filename)
    year = tour["Date"].iloc[0].split("/")[2]

    stats = {
        "Total games": tour.shape[0],
        "Number of bets": 0,
        "Number of winning bets": 0,
        "Number of losing bets": 0,
        "Percentage of success": 0,
        "Percentage of fails": 0,
        "Money": 0
    }

    money_list = [money]

    for _, game in tour.iterrows():
        winner_name = game["Winner"]
        loser_name = game["Loser"]

        winner_odd = game["B365W"]
        loser_odd = game["B365L"]

        winner_elo = -1
        loser_elo = -1
        find_winner = False
        find_loser = False

        for player_name in elo_ratings_dict.keys():
            if find_winner and find_loser:
                break

            elif names.names_compare(player_name, winner_name):
                winner_elo = elo_ratings_dict[player_name][year]["Elo"]
                find_winner = True

            elif names.names_compare(player_name, loser_name):
                loser_elo = elo_ratings_dict[player_name][year]["Elo"]
                find_loser = True

        if (winner_elo > 0) and (loser_elo > 0):
            winner_prob = calculate_probs(winner_elo, loser_elo)
            loser_prob = 1 - winner_prob

            winner_true_odd = prob_to_odd(winner_prob)
            loser_true_odd = prob_to_odd(loser_prob)

            print("Loser odds: {} - {}".format(loser_odd, loser_true_odd))
            print("Winner odds: {} - {}".format(winner_odd, winner_true_odd))

            if winner_odd > winner_true_odd:
                money += money * 0.1 * (winner_odd - 1)
                stats["Number of winning bets"] += 1
                stats["Number of bets"] += 1
            elif loser_odd > loser_true_odd:
                money *= 0.9
                stats["Number of losing bets"] += 1
                stats["Number of bets"] += 1

            money_list.append(money)

    stats["Percentage of success"] = (stats["Number of winning bets"] / stats["Number of bets"]) * 100
    stats["Percentage of fails"] = (stats["Number of losing bets"] / stats["Number of bets"]) * 100
    stats["Money"] = money

    pprint(stats)

    plt.plot(money_list)
    plt.show()


sim_tournament("ausopen2019.csv", "wta_elo_ratings.json", 40)
