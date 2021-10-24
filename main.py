from app import App
from soccer_data import getUpcomingFixtures

future_matches = getUpcomingFixtures("fixtures2021.csv").values.tolist()
app = App(future_matches)
app.start()