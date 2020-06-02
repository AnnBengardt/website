from blog import db
from blog.models import Flight
from random import randint, choice
from datetime import datetime

departure = ['Moscow', 'Saint-Petersburg', 'Voronezh', 'Ryazan', 'Omsk', 'Arkhangelsk']
arrival = ['Vladivostok', 'Samara', 'Ufa', 'Kazan', 'Sochi', 'Vologda']


for i in range(11):
    inp = str(randint(1, 30)) + '-08-2020 ' + str(randint(0, 23)) + ':00:00'
    flight = Flight(date=datetime.strptime(inp, '%d-%m-%Y %H:%M:%S'),
                    departure=choice(departure), arrival=choice(arrival), price=randint(3000, 10000))
    db.session.add(flight)
    db.session.commit()