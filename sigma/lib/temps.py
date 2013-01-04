import calendar
import datetime

class Periode(object):
    def __init__(self, debut, fin, mois=None, iter_by='month'):
        self.debut = debut
        self.fin = fin
        self.mois, self.premier_mois = self.calc_mois()
        self.__iter_by = iter_by
        if mois:
            self.mois = mois

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '<Periode: %s - %s, %s mois, %s jours>' % (
            self.debut,
            self.fin,
            self.mois,
            self.jours
            )

    def __reset(self):
        if self.debut and self.fin:
            self.__current_month = self.premier_mois
            self.__current_day = self.debut
        else:
            self.__current_month = None
            self.__current_day = None
        self.__iter_index = 0

    def days_in_month(self, date):
        # Retourne le nombre de jours dans un mois.
        return calendar.monthrange(
            date.year,
            date.month,
            )[1]

    @property
    def month_iterator(self):
        self.__iter_by = 'month'
        return self

    @property
    def days_iterator(self):
        self.__iter_by = 'days'
        return self

    def __iter__(self):
        self.__reset()
        self.__return_first = True
        return self

    def next(self):
        self.__iter_index += 1
        if self.__iter_by == 'month':
            if self.__iter_index > 1:
                # Start adding after first iteration.
                self.__current_month += datetime.timedelta(
                    self.days_in_month(self.__current_month)
                    )

            if not self.debut or not self.fin:
                raise StopIteration()
            if self.__iter_index > self.mois:
                raise StopIteration()
            return self.__current_month
        elif self.__iter_by == 'days':
            if self.__iter_index > 1:
                # Start adding after first iteration.
                self.__current_day += datetime.timedelta(1)
            if not self.debut or not self.fin:
                raise StopIteration()
            if self.__current_day > self.fin:
                raise StopIteration()
            return self.__current_day

    def calc_mois(self):
        if not self.debut or not self.fin:
            return 0, None

        calc_debut = datetime.date(
            self.debut.year,
            self.debut.month,
            1,
            )

        calc_fin = datetime.date(
            self.fin.year,
            self.fin.month,
            1,
            )

        if self.debut.day > 20:
            calc_debut += datetime.timedelta(
                days=self.days_in_month(calc_debut)
                )
        first_month = calc_debut

        if (self.fin.day < 20 and
            calc_fin - datetime.timedelta(1) >= calc_debut):
            calc_fin -= datetime.timedelta(1)

        # + 1 parce que inclusif
        return (((calc_fin.year - calc_debut.year) * 12)
                + calc_fin.month
                - (calc_debut.month)
                + 1
                ), first_month

    @property
    def jours(self):
        # +1 parce que c'est inclusif.
        if not self.fin or not self.debut:
            return 0
        return (self.fin - self.debut).days + 1

    def __add__(self, periode):
        return Periode(
            self.debut or periode.debut or None,
            (
                self.fin + datetime.timedelta(days=periode.jours)
                if self.debut else periode.fin or None
             ),
            mois=self.mois + periode.mois,
            )


