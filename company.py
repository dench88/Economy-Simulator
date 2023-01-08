import pandas as pd

class Company:
    """An abstract base class representing a company - Either farm, builder or resource co"""
    def __init__(self, name, company_type, number_of_workers, initial_investment, market, society, worker_productivity,
                 resource_productivity, resources_stock):
        self.name = name
        self.company_type = company_type
        self.number_of_workers = number_of_workers
        self.initial_investment = initial_investment
        self.market = market
        self.society = society
        self.worker_productivity = worker_productivity
        self.resource_productivity = resource_productivity
        self.resources_stock = resources_stock
        self.resources_bought = None
        self.resources_spot_price = None
        self.sales_price_per_unit = None
        self.initial_investment = initial_investment
        self.cash_held = initial_investment
        self.production_vol = 0
        self.sales = 0
        self.vol_to_sell = None
        self.planning_to_hire = False
        self.stock = 0
        self.resources_to_buy = None
        self.have_ideal_cash = None
        self.produce_at_capacity = True
        self.wages_bill = None
        self.record = {'Period': [], 'Num workers - start': [], 'Num workers - end': [], 'Num workers - hired': [],
                       'Production': [], 'Sales': [], 'Sales price per unit': [], 'Stock - starting (units)': [],
                       'Resources stock - start (units)': [], 'Resources consumed (units)': [],
                       'Resources stock - end (units)': [], 'Resources consumed (dollars)': [],
                       'Wages': [], 'Profit': [], 'Resources bought - units': [], 'Resources bought - dollars': [],
                       'Resources spot price': [], 'Cash - start': [], 'Cash - end': []}
        self.cash_runway = None
        self.resources_consumed_units = 0
        self.resources_consumed_dollar_value = None
        self.period = 1
        self.num_to_hire = 0
        self.full_record_df = None
        sales_6m_columns = ['Food bought - units', 'Housing bought - units', 'Resources bought - units',
                            'Resources bought - Farm1 - units', 'Resources bought - Builder1 - units']
        self.sales_6m_df = pd.DataFrame(columns=sales_6m_columns)

    def produce_goods(self):
        print(f"Beginning 'produce_goods' module...")
        # Add beginning cash and res stock to record
        self.record['Stock - starting (units)'].append(self.stock)
        self.record['Cash - start'].append(self.cash_held)
        self.record['Resources stock - start (units)'].append(self.resources_stock)
        # PRODUCTION CALCULATION ! ---------Based on number of workers.
        self.production_vol = self.number_of_workers * self.worker_productivity
        # Check company has sufficient resources to produce at capacity, except resources company, which will always produce at capacity
        if self.company_type == 'resources':
            self.produce_at_capacity = True
        else:
            # 1/ If resources are insufficient, use all resources remaining to produce what you can;
            if self.resources_stock < self.production_vol / self.resource_productivity:
                self.produce_at_capacity = False
            # 2/ If resources are sufficient, use resources to produce at capacity;
            else:
                self.produce_at_capacity = True
        # print(f"Produce at capacity variable is currently: {self.produce_at_capacity}")
        if self.produce_at_capacity:
            # no change to production determined in first line of this method above.
            pass
        else:
            self.production_vol = self.resources_stock * self.resource_productivity
        # Credit stock and debit resources
        self.stock += self.production_vol
        if self.company_type != 'resources': self.resources_stock -= self.production_vol / self.resource_productivity

    def sell_to_market(self):
        print(f"Beginning 'sell_to_market' module...")
        # Market response returns a tuple with first entry True or False and second entry the price
        market_response = self.market.check_trade_is_possible(self.production_vol, self.company_type)
        trade_is_successful = market_response[0]
        self.sales_price_per_unit = market_response[1]
        # REVERSING THIS CONDITION: ==> PPP- TO FIX: DONT BUY IF THE PRICE IS LOW.
        # if self.sales_price_per_unit < 0.4 * self.market.equilibrium_prices[self.company_type]:
        #     print("Holding onto produced volume until price recovers...")
        #     self.sales = 0
        if trade_is_successful:
            self.market.trade(self.name, self.stock, self.company_type)
            self.sales = self.stock * self.sales_price_per_unit
            self.stock -= self.stock
            print(f"Cash held before selling to market: {'${:,.0f}'.format(self.cash_held)}")
            self.cash_held += self.sales
            print(f"Sold {'{:,.0f}'.format(self.production_vol)} goods to market at price of {'${:,.0f}'.format(self.sales_price_per_unit)} for total value of {'${:,.0f}'.format(self.sales)}")
            print(f"Cash held after selling to market: {'${:,.0f}'.format(self.cash_held)}")
        else:
            print(f"No sale.")
            self.sales = 0

    def pay_workers(self):
        print(f"Beginning 'pay_workers' module...")
        # Check company has funds to pay then # Make payment anyway - later I will introduce a lending scheme
        self.wages_bill = self.number_of_workers * self.market.worker_pay
        self.cash_held -= self.wages_bill
        self.society.receive_wages(self.wages_bill)
        print(f"Total wages bill was {self.wages_bill}")

    def calculate_performance(self):
        print(f"Beginning 'calculate_performance' module...")
        # Calculate profit
        if self.company_type == 'resources':
            self.resources_consumed_units = 0
        else:
            self.resources_consumed_units = self.production_vol / self.resource_productivity
        self.resources_consumed_dollar_value = self.resources_consumed_units * self.market.prices[
            'resources']
        self.profit = self.sales - self.wages_bill - self.resources_consumed_dollar_value
        print(f"Profit was {'${:,.0f}'.format(self.profit)}")

    def plan_hiring(self):
        print(f"Beginning 'plan_hiring' module...")
        self.record['Num workers - start'].append(self.number_of_workers)
        # Hire only if the following conditions are met
        # 1/ cash held > 2 months cost and profit > 1.5 x worker pay
        est_resource_spend = self.resources_consumed_units * self.market.prices['resources']
        if self.profit > self.market.worker_pay * 1.5:
            if self.cash_held > (self.wages_bill + est_resource_spend) * 2:
                self.num_to_hire = self.number_of_workers // 15
                print(f"number of workers to hire is {self.num_to_hire}")
                self.hire_workers(self.num_to_hire)
            else:
                print(f"Not hiring.")
                self.num_to_hire = 0
        elif sum(self.record['Profit'][-2:]) < 1000:
            self.num_to_hire = -1 * self.number_of_workers // 10
            print(f"Profit negative for two periods: Firing {self.num_to_hire} workers")
            self.hire_workers(self.num_to_hire)
        else:
            self.num_to_hire = 0
            print(f"Not hiring.")

        # 2/ Profit has been positive for 8 weeks straight   ------))))))))))--------> Not Done Yet

    def plan_supply(self):
        """ Buy resources according to the following algorithm:
        If we have more than 4 months resources stock, buy nothing.
        If we have enough cash (ie 30% buffer), buy resources stock to reach 6 weeks stock.
        Else if we dont have enough cash to bring stock up to 6 wks then buy one week's worth"""
        print(f"Beginning 'plan_supply' module...")
        if self.company_type == 'resources':
            pass
        else:
            _4m_resources_stock = 4 * self.resources_consumed_units
            cost_4m_stock_res = _4m_resources_stock * self.market.prices['resources']
            if self.resources_stock > _4m_resources_stock:
                print(f"No need to buy resources this period.")
                self.resources_to_buy = 0
                self.resources_bought = 0
            elif self.cash_held >= 1.3 * cost_4m_stock_res:
                self.resources_to_buy = _4m_resources_stock - self.resources_stock
                print(f"Attempting to buy {self.resources_to_buy} units of resources.")
                self.buy_resources(self.resources_to_buy)
            else:
                self.resources_to_buy = self.resources_consumed_units
                print(f"Attempting to buy {self.resources_to_buy} units of resources.")
                self.buy_resources(self.resources_to_buy)

    def hire_workers(self, number):
        print(f"Beginning 'hire_workers' module...")
        self.number_of_workers += number

    def buy_resources(self, volume):
        print(f"Beginning 'buy_resources' module...")
        market_response2 = self.market.check_trade_is_possible(-1 * volume, 'resources')
        trade_is_successful = market_response2[0]
        self.resources_spot_price = market_response2[1]
        print(f"Trade attempt outcome: {trade_is_successful}")
        if trade_is_successful:
            # market has enough resources so execute trade:
            self.market.trade(self.name, (-1 * volume), 'resources')
            self.resources_stock += volume
            self.cash_held -= volume * self.resources_spot_price
            print(f"Bought {'{:.1f}'.format(volume)} units of resources at {'${:,.0f}'.format(self.resources_spot_price)}")
            self.resources_bought = volume * self.resources_spot_price
        else:
            self.resources_to_buy = 0
            self.resources_bought = 0
            print(f"Bought 0 units of resources")

    def apply_for_loan(self):
        pass

    def log_results(self):
        self.record['Period'].append(self.period)
        self.record['Num workers - end'].append(self.number_of_workers)
        self.record['Num workers - hired'].append(self.num_to_hire)
        self.record['Production'].append(self.production_vol)
        self.record['Sales'].append(self.sales)
        self.record['Sales price per unit'].append(self.sales_price_per_unit)
        self.record['Resources stock - end (units)'].append(self.resources_stock)
        self.record['Resources consumed (units)'].append(self.resources_consumed_units)
        self.record['Resources consumed (dollars)'].append(self.resources_consumed_dollar_value)
        self.record['Wages'].append(self.wages_bill)
        self.record['Profit'].append(self.profit)
        self.record['Resources bought - units'].append(self.resources_to_buy)
        self.record['Resources bought - dollars'].append(self.resources_bought)
        self.record['Resources spot price'].append(self.resources_spot_price)
        self.record['Cash - end'].append(self.cash_held)
        print(f"Results for this period logged.")
        # Update market 6m sales file: 1/ Convert csv to df, 2/ update df, 3/ revert to csv
        if self.company_type == 'resources':
            pass
        else:
            # 1
            self.sales_6m_df = pd.read_csv("data/6m_sales.csv")
            # 2
            self.sales_6m_df.loc[self.period - 1, f"Resources bought - {self.name} - units"] = self.resources_to_buy
            # 3
            self.sales_6m_df.to_csv("data/6m_sales.csv", sep=',', index=False)
            print(f"6m Sales CSV updated...")
            pd.set_option('display.max_columns', None)
            # print(self.sales_6m_df)
        self.period += 1

    def log_all(self):
        self.full_record_df = pd.DataFrame(self.record)
        self.full_record_df.to_csv(f"data/{self.name}_full_log.csv", sep=',', index=False)

    def play_turn(self):
        self.produce_goods()
        self.sell_to_market()
        self.pay_workers()
        self.calculate_performance()
        self.plan_hiring()
        self.plan_supply()
        self.log_results()


class Farm(Company):
    """A subclass representing a farm"""

    def __init__(self, name, company_type, number_of_workers, initial_investment, market, society, worker_productivity,
                 resource_productivity, resources_stock):
        super().__init__(name, company_type, number_of_workers, initial_investment, market, society,
                         worker_productivity, resource_productivity, resources_stock)


class Builder(Company):
    """A subclass representing a farm"""

    def __init__(self, name, company_type, number_of_workers, initial_investment, market, society, worker_productivity,
                 resource_productivity, resources_stock):
        super().__init__(name, company_type, number_of_workers, initial_investment, market, society,
                         worker_productivity, resource_productivity, resources_stock)


class ResourceCo(Company):
    """A subclass representing a farm"""

    def __init__(self, name, company_type, number_of_workers, initial_investment, market, society, worker_productivity,
                 resource_productivity, resources_stock):
        super().__init__(name, company_type, number_of_workers, initial_investment, market, society,
                         worker_productivity, resource_productivity, resources_stock)

    def play_turn(self):
        self.produce_goods()
        self.sell_to_market()
        self.pay_workers()
        self.calculate_performance()
        self.plan_hiring()
        self.log_results()
