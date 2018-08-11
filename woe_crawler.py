#!python

'''
NovaRO WoE Crawler
'''

import requests
from bs4 import BeautifulSoup
import re
import copy
import sys

class Guild(object):
    def __init__(self, nome):
        self.name = nome
        self.death_skill = {}
        self.damage_dealt = 0
        self.kills = 0
        self.damage_taken = 0
        self.damage_reduced = 0
        self.deaths = 0
        self.skills = 0
        self.emp_hits = 0
        self.hp_pots = 0
        self.speed_pots = 0
        self.players = 0

def simple_line(str):
    return int(str.string.replace(',',''))

def double_line(str):
    return int(str.prettify()[str.prettify().find("</span>") + 9 : len(str.prettify()) - 7].replace(',',''))

def read_info_deaths(guilds, col):
    str = col.findAll("td")[4].string.strip()
    if str not in guilds[guild_id].death_skill:
        guilds[guild_id].death_skill[str] = 0

    guilds[guild_id].death_skill[str] += 1

def read_info(guilds, col):
    """
    0. Total damage taken
    2. Reduced by gear
    7. Emperium hits
    12-1. Kills
    12-2. Skills casted
    13-1. Deaths
    14-2. HP pot used
    16-1. Damage dealt
    19-1. Speed pots
    """
    guilds[guild_id].damage_taken += simple_line(col[0].find_all("td")[2])

    guilds[guild_id].damage_reduced += simple_line(col[2].find_all("td")[1])

    guilds[guild_id].emp_hits += simple_line(col[7].find_all("td")[1])

    aux = col[12].find_all("td")
    guilds[guild_id].kills +=double_line(aux[0])

    guilds[guild_id].skills +=simple_line(aux[2])

    guilds[guild_id].deaths +=double_line(col[13].find_all("td")[0])

    guilds[guild_id].hp_pots +=simple_line(col[14].find_all("td")[2])

    guilds[guild_id].damage_dealt +=double_line(col[16].find_all("td")[0])

    guilds[guild_id].speed_pots +=double_line(col[19].find_all("td")[0])

    guilds[guild_id].players += 1

url_nova = "http://www.novaragnarok.com"
url_woe = url_nova + "/?module=woe_stats"

base = {
            '3968':Guild('1-Alliance'),
            '3015':Guild('2-Russian Squad'),
            '6641':Guild('3-Ravage'),
            '9593':Guild('4-Washed Up'),
            '2297':Guild('5-Pawring'),
            '-1':Guild('6-Others')
        }

guilds = copy.deepcopy(base)
jobs = {}

try:
    page = requests.get(url_woe)
    soup = BeautifulSoup(page.text, "html.parser")
    table = soup.find(id="woe-stats")

    if table is not None:
        for row in table.findAll("tr")[1:]:
            rows = row.findAll("td")
            url = rows[1].find('a')
            url_player = url_nova + url.get('href')
            if rows[2].string is None:
                job = 'Unknown'
            else:
                job = rows[2].string.strip()
            if job not in jobs:
                jobs[job] = copy.deepcopy(base)

            page = requests.get(url_player)
            soup = BeautifulSoup(page.text, "html.parser")
            col = soup.find(id = "table-stats").findAll("tr")

            guild_url = col[0].find_all("img")[1]['src']
            guild_id = guild_url[guild_url.find("id=")+3:]
            if not guild_id in guilds:
                guild_id = '-1'

            read_info(guilds, col)
            read_info(jobs[job], col)

            death_table = soup.find(id = "table-deaths")
            if death_table is not None:
                cols = death_table.findAll("tr")
                for col in cols:
                    read_info_deaths(guilds, col)
                    read_info_deaths(jobs[job], col)



except:
    e = sys.exc_info()
    print( e )

print("name \t job \t count \t damage dealt \t average damage dealt \t damage taken \t average damage taken\t damage reduced by gear \t average damage reduced by gear\t damage reduced %\t emp hits \t average emp hits \t kills \t average kills \t deaths \t average deaths \t kdr \t skills \t average skills \t hp pots \t average hp pots \t speed pots \t average speed pots")
for id in guilds:
    guild = guilds[id]
    if guild.players > 0:
        print(guild.name + "\t All \t" + str(guild.players) +
    " \t " + str(guild.damage_dealt) + "\t" + str(int(guild.damage_dealt/guild.players)) + "" +
    " \t " + str(guild.damage_taken) + "\t" + str(int(guild.damage_taken/guild.players)) + "" +
    " \t " + str(guild.damage_reduced) + "\t" + str(int(guild.damage_reduced/guild.players)) + "" +
    " \t\t " + str(guild.emp_hits) + "\t" + str(int(guild.emp_hits/guild.players)) + "" +
    " \t " + str(guild.kills) + "\t" + str(int(guild.kills/guild.players)) + "" +
    " \t " + str(guild.deaths) + "\t" + str(int(guild.deaths/guild.players)) + "" +
    " \t\t " + str(guild.skills) + "\t" + str(int(guild.skills/guild.players)) + "" +
    " \t " + str(guild.hp_pots) + "\t" + str(int(guild.hp_pots/guild.players)) + "" +
    " \t " + str(guild.speed_pots) + "\t" + str(int(guild.speed_pots/guild.players)) + "")

    for job in jobs:

        guild = jobs[job][id]
        if guild.players > 0:
            print(guild.name + " \t " + job + " \t " + str(guild.players) +
        " \t " + str(guild.damage_dealt) + "\t" + str(int(guild.damage_dealt/guild.players)) + "" +
        " \t " + str(guild.damage_taken) + "\t" + str(int(guild.damage_taken/guild.players)) + "" +
        " \t " + str(guild.damage_reduced) + "\t" + str(int(guild.damage_reduced/guild.players)) + "" +
        " \t\t " + str(guild.emp_hits) + "\t" + str(int(guild.emp_hits/guild.players)) + "" +
        " \t " + str(guild.kills) + "\t" + str(int(guild.kills/guild.players)) + "" +
        " \t " + str(guild.deaths) + "\t" + str(int(guild.deaths/guild.players)) + "" +
        " \t\t " + str(guild.skills) + "\t" + str(int(guild.skills/guild.players)) + "" +
        " \t " + str(guild.hp_pots) + "\t" + str(int(guild.hp_pots/guild.players)) + "" +
        " \t " + str(guild.speed_pots) + "\t" + str(int(guild.speed_pots/guild.players)) + "")
print()
print("************************************************************************")
print()
print("name \t job \t skill \t count")
for id in guilds:
    guild = guilds[id]
    if guild.deaths > 0 :
        aux = 0
        print(guild.name + "\t All \t Total \t" + str(guild.deaths) + "")
        for skill, value in sorted(guild.death_skill.items(), key = lambda x:x[1], reverse = True)[0:10]:
            print(guild.name + "\t All \t" + skill + " \t " + str(value) + "")
            aux += value
        print(guild.name + "\t All \tOthers \t" + str(guild.deaths - aux) + "")
    for job in jobs:
        guild = jobs[job][id]
        if guild.deaths > 0 :
            print(guild.name + "\t "+job+" \t Total \t" + str(guild.deaths) + "")
            aux = 0
            for skill, value in sorted(guild.death_skill.items(), key = lambda x:x[1], reverse = True)[0:10]:
                print(guild.name + "\t "+job+" \t" + skill + " \t " + str(value) + "")
                aux += value
            print(guild.name + "\t "+job+" \tOthers \t" + str(guild.deaths - aux) + "")
