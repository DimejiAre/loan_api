from src.common.database import Database
import uuid, math
from datetime import datetime


class Loan(object):

    def __init__(self, amount, date_due, loanee_name, loanee_id, interest_rate, date_collected=None, _id=None):
        self.amount_collected = amount
        self.amount_due = amount
        self.date_collected = datetime.now() if date_collected is None else date_collected
        self.date_due = datetime.strptime(date_due, "%d/%m/%Y")
        self.loanee_id = loanee_id
        self.loanee_name = loanee_name
        self.interest_rate = interest_rate
        self._id = str(uuid.uuid4()) if _id is None else _id

    def json(self):
        return {
            "amount_collected": self.amount_collected,
            "amount_due": self._amount_due(),
            "loanee_id": self.loanee_id,
            "date_collected": self.date_collected,
            "date_due": self.date_due,
            "loanee_name": self.loanee_name,
            "interest_rate": self.interest_rate,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.insert("loans", self.json())

    # function to update amount_due property
    def _amount_due(self):
        days = int((datetime.now() - self.date_collected).days)
        interest = self.amount_collected * (math.floor(days/2) * (int(self.interest_rate)/100))
        return self.amount_collected + interest

    # function to update database with current loan properties
    def _update_amount_due(self, match):
        Database.update(collection="loans", match={"_id": match}, data={"$set": self.json()})

    @staticmethod
    def view_loans():
        for i in Database.find(collection="loans"):
            loan = Loan(amount=i['amount_collected'], date_due=i['date_due'].strftime("%d/%m/%Y"),
                        loanee_name=i['loanee_name'], loanee_id=i['loanee_id'], date_collected=i['date_collected'],
                        interest_rate=i['interest_rate'], _id=i['_id'])
            loan._update_amount_due(match=loan._id)
        return [i for i in Database.find(collection="loans")]

    @staticmethod
    def get_loan(id):
        return Database.find_one(collection="loans", query={"_id": id})


    @staticmethod
    def delete_loan(id):
        Database.delete(collection="loans", query={"_id": id})
