import pandas as pd


class Society:
    def __init__(self, initial_pop, market):
        self.population = initial_pop
        self.market = market
        self.annual_birth_rate = 0.06
        self.annual_death_rate = 1 / 100
        self.annual_growth_rate = (1 + self.annual_birth_rate) * (1 - self.annual_death_rate) - 1
        self.farm_employees = 0
        self.builder_employees = 0
        self.resources_employees = 0
        self.unemployment_rate = 0
        self.consumer_cash = 6000000
        self.inflation = 2.5 / 100
        self.people_per_house = 3.2
        self.housing_shortfall = 0
        self.num_houses = initial_pop // self.people_per_house
        self.average_food_consumption = 90  # Units of food per month per person
        self.record = {'Period': [], 'Population': [], 'Housing bought - units': [], 'Food bought - units': [],
                       'Unemployment rate': [], 'Number of houses': [], 'Cash': []}
        self.period = 1
        self.full_record_df = None
        self.food_bought = 0
        self.houses_bought = 0
        sales_6m_columns = ['Food bought - units', 'Housing bought - units', 'Resources bought - units',
                            'Resources bought - Farm1 - units', 'Resources bought - Builder1 - units']
        self.sales_6m_df = pd.DataFrame(columns=sales_6m_columns)

    def receive_wages(self, wages_amount):
        self.consumer_cash += wages_amount

    def consume(self):
        self.housing_shortfall = self.population // self.people_per_house - self.num_houses
        if self.housing_shortfall >= 1:
            self.buy_housing(self.housing_shortfall)
        else:
            self.houses_bought = 0
        food_consumption = self.average_food_consumption * self.population
        self.buy_food(food_consumption)

    def buy_housing(self, volume):
        market_response = self.market.check_trade_is_possible(-1 * volume, 'builder')
        purchase_is_possible = market_response[0]
        spot_price = market_response[1]
        if purchase_is_possible:
            self.market.trade('Consumer', -1 * volume, 'builder')
            self.consumer_cash -= volume * spot_price
            self.num_houses += volume
            self.houses_bought = volume

    def buy_food(self, volume):
        market_response = self.market.check_trade_is_possible(-1 * volume, 'farm')
        purchase_is_possible = market_response[0]
        spot_price = market_response[1]
        if purchase_is_possible:
            self.market.trade('Consumer', -1 * volume, 'farm')
            self.consumer_cash -= volume * spot_price
            self.food_bought = volume

    def population_growth(self):
        period_growth_pc = (1 + self.annual_growth_rate) ** (1 / 12) - 1
        self.population = (self.population * (1 + period_growth_pc))
        # self.population = self.population // 1

    def log_results(self):
        self.record['Period'].append(self.period)
        self.record['Population'].append(self.population)
        self.record['Unemployment rate'].append(self.unemployment_rate)
        self.record['Number of houses'].append(self.num_houses)
        self.record['Cash'].append(self.consumer_cash)
        self.record['Housing bought - units'].append(self.houses_bought)
        self.record['Food bought - units'].append(self.food_bought)
        # Update market 6m sales file: 1/ Convert csv to df, 2/ update df, 3/ revert to csv
        # 1
        self.sales_6m_df = pd.read_csv("data/6m_sales.csv")
        # 2
        self.sales_6m_df.loc[self.period - 1, 'Housing bought - units'] = self.houses_bought
        self.sales_6m_df.loc[self.period - 1, 'Food bought - units'] = self.food_bought
        # Finally - all entries for this period have been completed - so calculate total resources bought.
        self.sales_6m_df.loc[self.period - 1, 'Resources bought - units'] = \
            self.sales_6m_df.iloc[self.period - 1, 3] + self.sales_6m_df.iloc[self.period - 1, 4]
        # 3
        self.sales_6m_df.to_csv("data/6m_sales.csv", sep=',', index=False)
        print(f"6m Sales CSV updated...")

    def play_turn(self):
        self.consume()
        self.population_growth()
        self.log_results()
        self.period += 1

    def log_all(self):
        self.full_record_df = pd.DataFrame(self.record)
        self.full_record_df.to_csv(f"data/Society_full_log.csv", sep=',', index=False)
