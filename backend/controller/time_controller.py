from backend.db.query.time_query import TimeQuery

class TimeController:
    def __init__(self):
        self.time_query = TimeQuery()

    def get_all_times(self):
        return self.time_query.find_all_times()
