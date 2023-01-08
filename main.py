from institutions import *
from market import *
from society import *
from company import *
from plots import *

import os
try:
    os.remove("data/6m_sales.csv")
except FileNotFoundError:
    print("CSV file not found to delete...")

# A PERIOD IS ONE MONTH: 3 Types of company: FARM, BUILDER AND RESOURCE CO
AVE_WORKER_P_F = 1000  # WORKER PRODUCTIVITY - UNITS OF FOOD PER PERSON PER PERIOD or COGS of 45%
AVE_WORKER_P_R = 50  # WORKER PRODUCTIVITY - UNITS OF RESOURCES PER WORKER PER PERIOD or COGS of 45%
AVE_WORKER_P_B = 0.05  # WORKER PRODUCTIVITY - UNITS OF HOUSING PER WORKER PER PERIOD or COGS of 45%
AVE_RESOURCE_P_F = 44  # RESOURCE PRODUCTIVITY - OF RESOURCES PER UNIT RESOURCE PER PERIOD or COGS of 0%
AVE_RESOURCE_P_B = 0.0022  # RESOURCE PRODUCTIVITY - UNITS OF HOUSING PER UNIT RESOURCE PER PERIOD or COGS of 45%
# Initialise the CSV file for market price adjustments
sales_6m_columns = ['Food bought - units', 'Housing bought - units', 'Resources bought - units',
                            'Resources bought - Farm1 - units', 'Resources bought - Builder1 - units']
sales_6m_df = pd.DataFrame(columns=sales_6m_columns)
sales_6m_df.to_csv("data/6m_sales.csv", sep=',', index=False)
print(f"Initialised market file looks like this (df): {sales_6m_df}")

market1 = Market('MarketCo1')
society1 = Society(2000, market1)
farm1 = Farm('Farm1', 'farm', 100, 10000000, market=market1, society=society1, worker_productivity=AVE_WORKER_P_F,
             resource_productivity=AVE_RESOURCE_P_F, resources_stock=19000)
builder1 = Builder('Builder1', 'builder', 40, 1000000, market=market1, society=society1, worker_productivity=AVE_WORKER_P_B,
                   resource_productivity=AVE_RESOURCE_P_B, resources_stock=2300)
resourceCo1 = ResourceCo('ResourceCo1', 'resources', 30, 4000000, market=market1, society=society1, worker_productivity=AVE_WORKER_P_R,
                         resource_productivity=0, resources_stock=0)
list_of_companies = [farm1, builder1, resourceCo1]
analysis_object = AnalysisOfSociety(society1, list_of_companies)
plot = Plot()

#  NEXT MOVES: 1/ Graph key metrics using matplotlib, 2/ Make market profitable, 3/ Fix up unemployment rate, 4/ Give market workers, 5/ Adjust consumption depending on price
for i in range(50):
    print(f"\n\n=====WEEK {i+1}, FARM ====")
    farm1.play_turn()
    print(f"\n\n=====WEEK {i + 1}, BUILDER ====")
    builder1.play_turn()
    print(f"\n\n=====WEEK {i + 1}, RESOURCES CO ====")
    resourceCo1.play_turn()
    print(f"\n\n=====WEEK {i + 1}, SOCIETY ====")
    society1.play_turn()
    print(f"\n\n=====WEEK {i + 1}, MARKET CO ====")
    market1.play_turn()
    analysis_object.play_turn()

farm1.log_all()
builder1.log_all()
resourceCo1.log_all()
market1.log_all()
society1.log_all()
analysis_object.log_all()
plot.plot()