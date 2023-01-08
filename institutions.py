import pandas as pd

class AnalysisOfSociety:
    def __init__(self, society_object, list_of_cos):
        self.society_object = society_object
        self.list_of_cos: list = list_of_cos
        self.unemployment_rate: float = 0
        self.record: dict = {'Unemployment rate': []}
        self.full_record_df = None

    def get_unemployment_rate(self):
        num_employed_ppl = 0
        for i in range(len(self.list_of_cos)):
            num_employed_ppl += getattr(self.list_of_cos[0], 'number_of_workers')
        self.unemployment_rate = 1 - num_employed_ppl / getattr(self.society_object, 'population')
        print(f"Unemployment rate is: {self.unemployment_rate}")
        # Now need to feed this data point into a CSV file...

    def log_results(self):
        self.record['Unemployment rate'].append(self.unemployment_rate)

    def log_all(self):
        self.full_record_df = pd.DataFrame(self.record)
        self.full_record_df.to_csv(f"data/society_unemployment_full_log.csv", sep=',', index=False)

    def play_turn(self):
        self.get_unemployment_rate()
        self.log_results()

class Bank:
    def __init__(self, initial_cash):
        self.interest_rate = 0.12
        self.deposits_total = 0
        self.loan_book = []
        self.cash_held = initial_cash

    def evaluate_application(self, customer_name, profit_per_period, cost_per_period, amount):
        pass

    def provide_loan(self, start_period, amount, customer_name):
        # Log loan
        self.loan_book.append({start_period, customer_name, amount})
        # Debit cash
        self.cash_held -= amount
        # For now assume all loans are approved
        return [True, self.interest_rate]


class CentralBank:
    def __init__(self):
        self.cash_rate = 0.03

    def buy_govt_bonds(self):
        pass


class Government:
    def __init__(self):
        self.cash_held = 10000000

