import datetime

class Task:
    def __init__(self, title=None, text=None, due_date=None, rank=None):
        self.title = title
        self.text = text
        self.created_time = datetime.datetime.now()
        self.due_date = due_date
        self.rank = rank
    
