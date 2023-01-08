import pandas as pd

class Market:
    def __init__(self, name):
        self.name = name
        self.worker_pay = 4500
        self.cash_held = 50000000
        self.margin = 0.10
        self.period = 1
        # Unit is 200kg of wood equivalent; wood is the only resource,
        # food Unit is one person-day of food, housing Unit is one small house
        self.equilibrium_prices = {'farm': 10, 'builder': 200000, 'resources': 200}
        self.stock = {'farm': 200000, 'builder': 10, 'resources': 50000}
        self.record = {'Period': [], 'Stock - food': [], 'Stock - housing': [], 'Stock - resources': [],
                       'Price - food': [], 'Price - housing': [], 'Price - resources': [], 'Cash - end': []}
        self.transactions = []
        self.optimal_stock_levels = {'farm': 1, 'builder': 1, 'resources': 1}
        self.relative_stock_levels = {'farm': 1, 'builder': 1, 'resources': 1}
        # Prices start at equilibrium prices then adjust with market stock levels
        self.prices = {'farm': 10, 'builder': 200000, 'resources': 200}
        self.price_multiple = {'farm': 1, 'builder': 1, 'resources': 1}

    def adjust_prices(self):
        """This is a supply-demand curve proxy. When the market has a stock deficiency,
        it pays top dollar. When there is a glut, prices drop. Also, the prices it
        sells to consumers at should be defined by a profit margin over bought prices"""
        # 1/ Compare stock levels with a base, desirable stock level
        # 2/ Alter prices depending on stock deficiency or glut
        # For 1/ Lets say the market aims to have 6 months of stock based on recent sales volumes
        self.sales_6m_df = None
        if self.period < 2:
            pass
        else:
            num_periods_to_look = min(self.period, 6)
            self.sales_6m_df = pd.read_csv("data/6m_sales.csv")
            print(self.sales_6m_df)
            food_1m_sales = sum(self.sales_6m_df['Food bought - units'][-num_periods_to_look:]) * (1 / num_periods_to_look)
            self.optimal_stock_levels['farm'] = food_1m_sales
            housing_6m_sales = sum(self.sales_6m_df['Housing bought - units'][-num_periods_to_look:]) * (6 / num_periods_to_look)
            self.optimal_stock_levels['builder'] = housing_6m_sales
            resources_6m_sales = sum(self.sales_6m_df['Resources bought - units'][-num_periods_to_look:]) * (6 / num_periods_to_look)
            self.optimal_stock_levels['resources'] = resources_6m_sales
            # 2/ Alter prices depending on stock deficiency or glut
            for i in self.stock:
                # If resources bought lately is zero then we get a division by zero error so:
                try:
                    self.relative_stock_levels[i] = self.stock[i] / self.optimal_stock_levels[i]
                except ZeroDivisionError:
                    self.relative_stock_levels[i] = 15
            print(f"Relative stock levels are: {self.relative_stock_levels}")
            # REPLACE BELOW WITH CALL TO NEW PRCE FUNCTION
            self.prices = {k: self.price_function(self.relative_stock_levels)[k] * self.equilibrium_prices[k] for k in self.equilibrium_prices}
            # MIGHT BE BETTER TO RETURN TO THE OLD WAY BELOW. MEASURE OF BEST PRICE FUNCTION IS THE ONE THAT BEST APROXIMATES ZERO EXCESS DEMAND <---------------------------***
            # for i in self.prices:
            #     self.prices[i] = self.equilibrium_prices[i] / self.relative_stock_levels[i]
            print(f"Relative price levels are: {self.price_function(self.relative_stock_levels)}")

    def price_function(self, relative_stock_levels: dict):
        updated_prices = {}
        for i in relative_stock_levels.keys():
            # print(f"i in price_function is {i} =============== --------==============")
            if relative_stock_levels[i] < 1 / 6:
                updated_prices[i] = 3.5
            elif relative_stock_levels[i] > 6:
                updated_prices[i] = (7 / 12)
            else:
                updated_prices[i] = ((1 / (2 * relative_stock_levels[i])) + (1 / 2))
        return updated_prices

    def check_trade_is_possible(self, incoming_volume_to_market, company_type):
        if incoming_volume_to_market > 0:
            # This is a company selling goods to the market
            # Decline trade request if market has insufficient funds OR market stock levels are too high
            if self.cash_held >= incoming_volume_to_market * self.prices[company_type] and self.relative_stock_levels[company_type] < 5:
                print(f"Trade successful.")
                return (True, self.prices[company_type])
            else:
                print(f"Trade unsuccessful. Market has insufficient funds to buy {incoming_volume_to_market} of {company_type} goods at {self.prices[company_type]} unit price")
                print(f"Market has {'${:,.0f}'.format(self.cash_held)} in cash")
                return (False, self.prices[company_type])
        elif incoming_volume_to_market < 0:
            # This is a purchase of goods from the market
            if self.stock[company_type] > -1 * incoming_volume_to_market:
                print(f"Trade successful.")
                return (True, self.prices[company_type])
            else:
                print(f"Trade unsuccessful. Market has insufficient {company_type} resources")
                return (False, self.prices[company_type])
        else:
            print(f"Trade volume is zero. Trade rejected.")
            return (False, self.prices[company_type])

    def trade(self, customer, incoming_volume_to_market, company_type):
        self.stock[company_type] += incoming_volume_to_market
        self.cash_held -= incoming_volume_to_market * self.prices[company_type]
        log = {'Period': self.period, 'Customer': customer, 'Resource': company_type,
               'Volume': incoming_volume_to_market, 'Price': self.prices[company_type]}
        self.transactions.append(log)

    def log_results(self):
        self.record['Period'].append(self.period)
        self.record['Stock - food'].append(self.stock['farm'])
        self.record['Stock - housing'].append(self.stock['builder'])
        self.record['Stock - resources'].append(self.stock['resources'])
        self.record['Price - food'].append(self.prices['farm'])
        self.record['Price - housing'].append(self.prices['builder'])
        self.record['Price - resources'].append(self.prices['resources'])
        self.record['Cash - end'].append(self.cash_held)

    def log_all(self):
        self.full_record_df = pd.DataFrame(self.record)
        self.full_record_df.to_csv(f"data/{self.name}_full_log.csv", sep=',', index=False)
        self.transactions_df = pd.DataFrame(self.transactions)
        self.transactions_df.to_csv("data/market_transactions.csv", sep=',', index=False)

    def play_turn(self):
        self.log_results()
        self.adjust_prices()
        self.period += 1