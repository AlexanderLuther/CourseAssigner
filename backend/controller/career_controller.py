from backend.db.query.carrer_query import CareerQuery

class CareerController:
    def __init__(self):
        self.career_query = CareerQuery()

    def get_all_careers(self):
        return self.career_query.find_all_careers()
