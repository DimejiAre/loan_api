from src.common.database import Database
import uuid

from src.models.loans import Loan


class Loanee(object):
    def __init__(self, name, phone_number, email_address, _id = None):
        self.name = name
        self.phone_number = phone_number
        self.email_address = email_address
        self._id = str(uuid.uuid4()) if _id is None else _id

    def json(self):
        return {
            "name": self.name,
            "phone_number": self.phone_number,
            "email_address": self.email_address,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.insert("loanees", self.json())

    def create_loan(self, amount, date_due, interest_rate):
        loan = Loan(amount=amount, date_due=date_due, loanee_name=self.name, interest_rate=interest_rate,
                    loanee_id=self._id)
        loan.save_to_mongo()

    @staticmethod
    def view_loanees():
        return [i for i in Database.find(collection="loanees")]

    @staticmethod
    def get_loanee(id):
        return Database.find_one(collection="loanees", query={"_id": id})

    @staticmethod
    def delete_loanee(id):
        Database.delete(collection="loanees", query={"_id": id})