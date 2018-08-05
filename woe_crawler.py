#!python

'''
NovaRO WoE Crawler
'''

import urllib.request
from bs4 import BeautifulSoup
import re

class Guild(object):
    def _int_(self, nome, id):
        self.nome = nome
        self.id = id
        self.damage_dealt = 0
        self.kills = 0
        self.damage_reduced = 0
        self.deaths = 0
        self. skills = 0
        self.emp_hits = 0
        self.hp_pots = 0
        self.speed_pots = 0
        self.players = 0

url_nova = "https://www.novaragnarok.com/"
url = url_nova + "?module=woe_stats"

guilds = {
            'Alliance':Guild('Alliance', 3968),
            'Russian Squad':Guild('Russian Squad', 3015),
            'Ravage':Guild('Ravage', 6641),
            'Washed Up':Guild('Washed Up', 9593),
            'Pawring':Guild('Pawring', 2297),
            'Others':Guild('Others', -1)
        }

try:
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    table = soup.find("table", {"id":"woe-stats"})

    print(len(table))

    # if table is not None:
    #     for row in table.findAll("tr")[1:]:
    #         col = row.findAll("td")
    #
    #         departure_number = int(col[1].text)
    #         departures_total += departure_number
    #
    #         accessibles = len(re.findall(r'(?=horarioAdaptado)', str(col[2])))
    #         accessibles_total += accessibles
    #
    #     percentual = accessibles_total/departures_total
    #     line_info = {"route_id": line_name, "departures": departures_total, "departures_adapted": accessibles_total, "direction": directions_names[idx], "accessibility_score": percentual, "shape": shapes[idx]}
    #     success_lines.append(line_info)
    # else:
    #     print("Page not found for line %s, direction %s" % (line_name, directions_names[idx]))
    #     line_info = (line_name, directions_names[idx])
    #     not_found_lines.append(line_info)
except:
    print("Error - Can't read website")
