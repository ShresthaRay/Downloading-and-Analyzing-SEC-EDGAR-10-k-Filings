from sec_api import XbrlApi
import pandas as pd 

API_KEY = 'API_KEY_HERE'

xbrlApi = XbrlApi(API_KEY)

# URL of Google's 10-K filings
url_10k = 'https://www.sec.gov/Archives/edgar/data/1652044/000165204423000016/goog-20221231.htm'

xbrl_json = xbrlApi.xbrl_to_json(htm_url=url_10k)

# convert XBRL-JSON of income statement to pandas dataframe
def get_income_statement(xbrl_json):
    income_statement_store = {}

    # iterate over each US GAAP item in the income statement
    for usGaapItem in xbrl_json['StatementsOfIncome']:
        values = []
        indicies = []

        for fact in xbrl_json['StatementsOfIncome'][usGaapItem]:
            # only consider items without segment. not required for our analysis.
            if 'segment' not in fact:
                index = fact['period']['startDate'] + '-' + fact['period']['endDate']
                # ensure no index duplicates are created
                if index not in indicies:
                    values.append(fact['value'])
                    indicies.append(index)                    

        income_statement_store[usGaapItem] = pd.Series(values, index=indicies) 

    income_statement = pd.DataFrame(income_statement_store)
    # switch columns and rows so that US GAAP items are rows and each column header represents a date range
    return income_statement.T 


income_statement_google = get_income_statement(xbrl_json)


print("Income statement from Google's 2022 10-K filing as dataframe")
print('------------------------------------------------------------')
income_statement_google

# Google's 10Ks of the last 5 years, 2018 to 2022, with data from 2016 to 2022
url_10k_2018 = 'https://www.sec.gov/Archives/edgar/data/1652044/000165204419000004/goog10-kq42018.htm'
url_10k_2019 = 'https://www.sec.gov/Archives/edgar/data/1652044/000165204420000008/goog10-k2019.htm'
url_10k_2020 = 'https://www.sec.gov/Archives/edgar/data/1652044/000165204421000010/goog-20201231.htm'
url_10k_2021 = 'https://www.sec.gov/Archives/edgar/data/1652044/000165204422000019/goog-20211231.htm'
url_10k_2022 = 'https://www.sec.gov/Archives/edgar/data/1652044/000165204423000016/goog-20221231.htm'

xbrl_json_2018 = xbrlApi.xbrl_to_json(htm_url=url_10k_2018)
xbrl_json_2019 = xbrlApi.xbrl_to_json(htm_url=url_10k_2019)
xbrl_json_2020 = xbrlApi.xbrl_to_json(htm_url=url_10k_2020)
xbrl_json_2021 = xbrlApi.xbrl_to_json(htm_url=url_10k_2021)
xbrl_json_2022 = xbrlApi.xbrl_to_json(htm_url=url_10k_2022)

# fix naming inconsistency
xbrl_json_2020['StatementsOfIncome']['RevenueFromContractWithCustomerExcludingAssessedTax'] = xbrl_json_2020['StatementsOfIncome']['Revenues']
del xbrl_json_2020['StatementsOfIncome']['Revenues']
xbrl_json_2021['StatementsOfIncome']['RevenueFromContractWithCustomerExcludingAssessedTax'] = xbrl_json_2021['StatementsOfIncome']['Revenues']
del xbrl_json_2021['StatementsOfIncome']['Revenues']

income_statement_2018 = get_income_statement(xbrl_json_2018)
income_statement_2019 = get_income_statement(xbrl_json_2019)
income_statement_2020 = get_income_statement(xbrl_json_2020)
income_statement_2021 = get_income_statement(xbrl_json_2021)
income_statement_2022 = get_income_statement(xbrl_json_2022)

income_statements_merged = pd.concat([income_statement_2018, 
                                      income_statement_2019, 
                                      income_statement_2020, 
                                      income_statement_2021, 
                                      income_statement_2022], axis=0, sort=False)

# sort & reset the index of the merged dataframe
income_statements_merged = income_statements_merged.sort_index().reset_index()

# convert cells to float
income_statements_merged = income_statements_merged.applymap(lambda x: pd.to_numeric(x, errors='ignore'))


print("Merged, uncleaned financials of all income statements")
print('-----------------------------------------------------')
income_statements_merged.head(10)

income_statements = income_statements_merged.groupby('index').max()

# reindex the merged dataframe using the index of the first dataframe
income_statements = income_statements.reindex(income_statement_2019.index)

# loop over the columns
for col in income_statements.columns[1:]:
    # extract start and end dates from the column label
    splitted = col.split('-')
    start = '-'.join(splitted[:3])
    end = '-'.join(splitted[3:])

    # convert start and end dates to datetime objects
    start_date = pd.to_datetime(start)
    end_date = pd.to_datetime(end)

    # calculate the duration between start and end dates
    duration = (end_date - start_date).days / 360

    # drop the column if duration is less than a year
    if duration < 1:
        income_statements.drop(columns=[col], inplace=True)

# convert datatype of cells to readable format, e.g. "2.235460e+11" becomes "223546000000"
income_statements = income_statements.apply(lambda row: pd.to_numeric(row, errors='coerce', downcast='integer').astype(str), axis=1) 


print("Income statements from Google's 10-K filings (2016 to 2022) as dataframe")
print('------------------------------------------------------------------------')
income_statements

all_revenues_json = xbrl_json_2018['StatementsOfIncome']['RevenueFromContractWithCustomerExcludingAssessedTax'] + \
                    xbrl_json_2019['StatementsOfIncome']['RevenueFromContractWithCustomerExcludingAssessedTax'] + \
                    xbrl_json_2020['StatementsOfIncome']['RevenueFromContractWithCustomerExcludingAssessedTax'] + \
                    xbrl_json_2021['StatementsOfIncome']['RevenueFromContractWithCustomerExcludingAssessedTax'] + \
                    xbrl_json_2022['StatementsOfIncome']['RevenueFromContractWithCustomerExcludingAssessedTax']

all_revenues = pd.json_normalize(all_revenues_json)

# explode segment list of dictionaries
all_revenues = all_revenues.explode('segment')

segment_split = all_revenues['segment'].apply(pd.Series)
segment_split = segment_split.rename(columns={'dimension': 'segment.dimension', 'value': 'segment.value'})
segment_split = segment_split.drop(0, axis=1)

all_revenues = all_revenues.combine_first(segment_split)
all_revenues = all_revenues.drop('segment', axis=1)
all_revenues = all_revenues.reset_index(drop=True)

all_revenues

xbrl_dimensions = all_revenues.pivot(columns='segment.dimension', values='segment.value').dropna(how='all')
xbrl_dimensions = pd.DataFrame([(col, xbrl_dimensions[col].unique()) for col in xbrl_dimensions.columns], \
                             columns=['segment.dimension', 'segment.values'])

xbrl_dimensions

all_revenues['value'] = all_revenues['value'].astype(int)
mask = all_revenues['segment.dimension'] == 'srt:StatementGeographicalAxis'
revenue_region = all_revenues[mask]
revenue_region = revenue_region.drop_duplicates(subset=['period.endDate', 'segment.value'])

# pivot the dataframe to create a new dataframe with period.endDate as the index, 
# segment.value as the columns, and value as the values
revenue_region_pivot = revenue_region.pivot(index='period.endDate', columns='segment.value', values='value')


print("Google's revenues by region from 2016 to 2022")
print('---------------------------------------------')
revenue_region_pivot

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# plot the histogram bar chart
ax = revenue_region_pivot.plot(kind='bar', stacked=True, figsize=(8, 6))

# rotate the x-axis labels by 0 degrees
plt.xticks(rotation=0)

# set the title and labels for the chart
ax.set_title("Google's Revenue by Region", fontsize=16, fontweight='bold')
ax.set_xlabel('Period End Date', fontsize=12)
ax.set_ylabel('Revenue (USD)', fontsize=12)

# set the legend properties
ax.legend(title='Product Category', loc='upper left', fontsize='small', title_fontsize=10)

# add gridlines
ax.grid(axis='y', linestyle='--', alpha=0.3)

# remove the top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# format y-axis ticks to show values in millions in dollars
formatter = ticker.FuncFormatter(lambda x, pos: '$%1.0fB' % (x*1e-9))
plt.gca().yaxis.set_major_formatter(formatter)

# map the original labels to new labels
label_map = {
    'country:US': 'US',
    'goog:AmericasExcludingUnitedStatesMember': 'Americas Excluding US',
    'srt:AsiaPacificMember': 'Asia Pacific',
    'us-gaap:EMEAMember': 'EMEA'
}

# create a list of new labels based on the original labels
new_labels = [label_map[label] for label in sorted(revenue_region['segment.value'].unique())]
handles, _ = ax.get_legend_handles_labels()
plt.legend(handles=handles[::-1], labels=new_labels[::-1])

# add the values in billions of dollars to each part of the bar
for p in ax.containers:
    ax.bar_label(p, labels=['%.1f' % (v/1e9) for v in p.datavalues], 
                 label_type='center', fontsize=8)

plt.show()

all_revenues['value'] = all_revenues['value'].astype(int)

mask_1 = all_revenues['segment.dimension'] == 'srt:ProductOrServiceAxis'
mask_2 = all_revenues['segment.dimension'] == 'us-gaap:StatementBusinessSegmentsAxis'

revenue_product = all_revenues[mask_1 | mask_2]

revenue_product = revenue_product.drop_duplicates(subset=['period.endDate', 'segment.value'])

# pivot the dataframe to create a new dataframe with period.endDate as the index, 
# segment.value as the columns, and value as the values
revenue_product_pivot = revenue_product.pivot(index='period.endDate', columns='segment.value', values='value')


print("Google's revenues by product from 2016 to 2022")
print('-----------------------------------------------')
revenue_product_pivot

revenue_product_pivot['goog:GoogleNetwork'] = revenue_product_pivot['goog:GoogleNetworkMember'].fillna(revenue_product_pivot['goog:GoogleNetworkMembersPropertiesMember'])
revenue_product_pivot = revenue_product_pivot.drop(['goog:GoogleNetworkMember', 'goog:GoogleNetworkMembersPropertiesMember'], axis=1)

revenue_product_pivot = revenue_product_pivot[['goog:GoogleSearchOtherMember', 
                                               'goog:YouTubeAdvertisingRevenueMember', 
                                               'goog:GoogleNetwork', 
                                               'goog:GoogleCloudMember',
                                               'goog:OtherRevenuesMember']]

# remove 2016 row
revenue_product_pivot = revenue_product_pivot.iloc[1:]

revenue_product_pivot
sorted(list(revenue_product_pivot.columns.unique()))

# plot the histogram bar chart
ax = revenue_product_pivot.plot(kind='bar', stacked=True, figsize=(8, 6))

# rotate the x-axis labels by 0 degrees
plt.xticks(rotation=0)

# set the title and labels for the chart
ax.set_title("Google's Revenue by Product", fontsize=16, fontweight='bold')
ax.set_xlabel('Period End Date', fontsize=12)
ax.set_ylabel('Revenue (USD)', fontsize=12)

# set the legend properties
ax.legend(title='Product Category', loc='upper left', fontsize='small', title_fontsize=10)

# add gridlines
ax.grid(axis='y', linestyle='--', alpha=0.3)

# remove the top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# format y-axis ticks to show values in millions in dollars
formatter = ticker.FuncFormatter(lambda x, pos: '$%1.0fB' % (x*1e-9))
plt.gca().yaxis.set_major_formatter(formatter)

# map the original labels to new labels
label_map = {
    'goog:GoogleCloudMember': 'Google Cloud',
    'goog:GoogleNetwork': 'Google Network',
    'goog:YouTubeAdvertisingRevenueMember': 'YouTube Ads',
    'goog:GoogleSearchOtherMember': 'Google Search & other',
    'goog:OtherRevenuesMember': 'Google other',
}

# create a list of new labels based on the original labels
new_labels = [label_map[label] for label in list(revenue_product_pivot.columns.unique())]
handles, _ = ax.get_legend_handles_labels()
plt.legend(handles=handles[::-1], labels=new_labels[::-1])

# add the values in billions of dollars to each part of the bar
for p in ax.containers:
    ax.bar_label(p, labels=['%.1f' % (v/1e9) for v in p.datavalues], 
                 label_type='center', fontsize=8)

plt.show()

fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 5))

revenue_region_pivot.iloc[1:].plot(kind='bar', stacked=True, ax=ax1)
revenue_product_pivot.plot(kind='bar', stacked=True, ax=ax2)

# set the title and labels for the chart
ax1.set_title("Google's Revenue by Region", fontsize=16, fontweight='bold')
ax1.set_xlabel('Period End Date', fontsize=12)
ax1.set_ylabel('Revenue (USD)', fontsize=12)
ax2.set_title("Google's Revenue by Product", fontsize=16, fontweight='bold')
ax2.set_xlabel('Period End Date', fontsize=12)

# set the legend properties
ax1.legend(title='Region', loc='upper left', fontsize='small', title_fontsize=10)
ax2.legend(title='Product Category', loc='upper left', fontsize='small', title_fontsize=10)

# add gridlines
ax1.grid(axis='y', linestyle='--', alpha=0.3)
ax2.grid(axis='y', linestyle='--', alpha=0.3)

# remove the top and right spines
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# map the original labels to new labels
label_map_1 = {
    'country:US': 'US',
    'goog:AmericasExcludingUnitedStatesMember': 'Americas Excluding US',
    'srt:AsiaPacificMember': 'Asia Pacific',
    'us-gaap:EMEAMember': 'EMEA'
}
label_map_2 = {
    'goog:GoogleCloudMember': 'Google Cloud',
    'goog:GoogleNetwork': 'Google Network',
    'goog:YouTubeAdvertisingRevenueMember': 'YouTube Ads',
    'goog:GoogleSearchOtherMember': 'Google Search & other',
    'goog:OtherRevenuesMember': 'Google other',
}

# create a list of new labels based on the original labels
new_labels1 = [label_map_1[label] for label in list(revenue_region_pivot.columns.unique())]
new_labels2 = [label_map_2[label] for label in list(revenue_product_pivot.columns.unique())]
handles1, _ = ax1.get_legend_handles_labels()
handles2, _ = ax2.get_legend_handles_labels()
ax1.legend(handles=handles1[::-1], labels=new_labels1[::-1])
ax2.legend(handles=handles2[::-1], labels=new_labels2[::-1])

# add the values in billions of dollars to each part of the bar
for p in ax1.containers:
    ax1.bar_label(p, labels=['%.1f' % (v/1e9) for v in p.datavalues], 
                 label_type='center', fontsize=8)

for p in ax2.containers:
    ax2.bar_label(p, labels=['%.1f' % (v/1e9) for v in p.datavalues], 
                 label_type='center', fontsize=8)

# format y-axis ticks to show values in millions in dollars
formatter = ticker.FuncFormatter(lambda x, pos: '$%1.0fB' % (x*1e-9))
ax1.yaxis.set_major_formatter(formatter)
ax2.yaxis.set_major_formatter(formatter)

# rotate the x-axis labels by 0 degrees
ax1.tick_params(axis='x', labelrotation=30)
ax2.tick_params(axis='x', labelrotation=30)

plt.show()