from tennisabstract import TennisAbstract

tennis = TennisAbstract("http://tennisabstract.com/reports/wta_elo_ratings.html", "wta_elo_ratings.json")
tennis.scrap_ratings()
tennis.save()
tennis.close()
