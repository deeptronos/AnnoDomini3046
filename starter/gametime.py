import os

    #   The game has two 45-day seasons to a year: Spryng and Otom

class GameTime:
    def __init__(self):
        self.currentDate = 1
        self.dayCounter = 0 #   Used to keep track of how many days it has been since the year began, and reset on year change
        self.currentSeason = "spryng"
        self.year = 0

    def advanceDate(self):
        dayCounter += 1
        if self.currentDate < 45:
            self.currentDate += 1
        else:
            self.currentDate == 0
            self.changeSeason()

        if self.dayCounter == 90:
            self.dayCounter = 0
            self.year += 1


    def changeSeason(self):
        if self.currentSeason == "spryng":
            self.currentSeason = "otom"

        elif self.currentSeason == "otom":
            self.year += 1
            self.currentSeason = "spryng"

    def formattedDate(self):
        dayExt = "th"
        if self.currentDate%10 == 1:
            dayExt = "st"
        elif self.currentDate%10 == 2:
            dayExt = "nd"
        elif self.currentDate%10 == 3:
            dayExt = "rd"
        if self.currentDate > 12 and self.currentDate < 20:
            dayExt = "th"

        return "{season} {day}{ext}, {year}".format(season = self.currentSeason, day = self.currentDate, ext = dayExt, year = (3049 + self.year))
