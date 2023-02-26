import csv

fieldnames = [
        'Fund ID',
        'Department ID',
        'Program ID',
        'Account ID',
        'Fund',
        'Fund Description',
        'Function',
        'Function Description',
        'Department',
        'Department Description',
        'Description',
        'Actuals 2013',
        'Actuals 2014',
        'Actuals 2015',
        'Actuals 2016',
        'Actuals 2017',
        'Actuals 2018',
        'Actuals 2019',
        'Actuals 2020',
        'Actuals 2021',
        'Estimates 2022',
        'Estimates 2023',
    ]

budget_cleaned = 'raw/oak_park_budget_cleaned.csv'
function_descriptions = 'raw/function_descriptions.csv'
budget_data = []
with open(budget_cleaned) as csvfile:
    budget_data = list(csv.DictReader(csvfile))

    print('adding function descriptions ...')
    with open(function_descriptions) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for p in budget_data:
                if row['Function'] == p['Function']:
                    p['Function Description'] = row['Description']

print('writing output ...')       
outp = open('final/oak_park_budget_cleaned.csv', 'w')
writer = csv.DictWriter(outp, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
writer.writeheader()
writer.writerows(budget_data)
outp.close()
