from flask import Flask, render_template
from bs4 import BeautifulSoup
from operator import itemgetter
import urllib2
import re

app = Flask(__name__)

class team:
	def __init__(self, captain, roster, results, total):
		self.captain = captain
		self.roster = roster
		self.results = results
		self.total = 0

def minProPoints(matchPointString):
	mps = int(matchPointString)
	if mps >= 36:
		return 15
	elif mps == 35:
		return 12
	elif mps == 34:
		return 11
	elif mps == 33:
		return 10
	elif mps == 31:
		return 8
	elif mps == 30:
		return 6
	elif mps == 28 or mps == 29:
		return 4
	else:
		return 3

@app.route('/')
def fantasydraft():

	teams = []
	teams.append(team('Stephen', ['Cuneo, Andrew', 'Floch, Ivan', 'Utter-Leyton, Josh'], [], 0))
	teams.append(team('Drew', ['Juza, Martin', 'Yasooka, Shota', 'Nakamura, Shuhei'], [], 0))


	coverageUrl = 'http://magic.wizards.com/en/events/coverage/ptaer'
	coverageResponse = urllib2.urlopen(coverageUrl)
	coveragePage = BeautifulSoup(coverageResponse.read(), 'html.parser')
	standingsUrl = coveragePage.find_all(href=re.compile('standings'))[-1].get('href')

	standingsResponse = urllib2.urlopen(standingsUrl)
	standingsHtml = BeautifulSoup(standingsResponse.read(), 'html.parser')

	rows = standingsHtml.table.find_all('tr')
	for row in rows [1:]:
		cells = row.find_all('td')
		name = cells[1].getText()
		for t in teams:
			for n in t.roster:
				if n in name: 
					t.results.append(n + " | Match Points: " + cells[2].getText() + " | Min Pro Points: " + 
						str(minProPoints(cells[2].getText())))
					t.total += minProPoints(cells[2].getText())

	teams.sort(key = lambda x: x.total, reverse=True)

	res = render_template ('index.html', title = standingsHtml.title.getText(), teams = teams)
	return res

if __name__ == "__main__":
    app.run()
