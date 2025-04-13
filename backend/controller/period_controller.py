from backend.db.query.period_query import PeriodQuery

class PeriodController:
    def __init__(self):
        self.period_query = PeriodQuery()

    def get_all_periods(self):
        return self.period_query.find_all_periods()
