import csv

# link on Fund, Account, Department & Program ID

def cleanup():

    fieldnames = [
        'Fund ID',
        'Department ID',
        'Program ID',
        'Account ID',
        'Fund',
        'Department',
        'Description',
        'Actuals 2013',
        'Actuals 2014',
        'Actuals 2015',
        'Actuals 2016',
        'Actuals 2017',
        'Actuals 2018',
        'Actuals 2019',
        'Estimates 2020',
        'Estimates 2021'
    ]

    budget_2021 = 'raw/2021 Adopted Budget - VOP - Data2018-2021.csv'
    budget_2019 = 'raw/2019 Adopted Budget - VOP - Data2016-2017.csv'
    budget_2017 = 'raw/2017 Adopted Budget - Data2013-2015.csv'
    
    all_rows = []
    # start with 2021 budget
    with open(budget_2021) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            all_rows.append(row)
    
    # append 2019 budget
    with open(budget_2019) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for main_row in all_rows:
                if match_rows(row, main_row):
                    main_row['Actuals 2016'] = row['2016 Actual']
                    main_row['Actuals 2017'] = row['2017 Actual']

    # append 2017 budget
    with open(budget_2017) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for main_row in all_rows:
                if match_rows(row, main_row):
                    main_row['Actuals 2013'] = row['2013 Actual']
                    main_row['Actuals 2014'] = row['2014 Actual']
                    main_row['Actuals 2015'] = row['2015 Actual']
    
    # loop through the result and fill in blanks with zeroes
    for row in all_rows:
        row['Actuals 2013'] = row.get('Actuals 2013', '0')
        row['Actuals 2014'] = row.get('Actuals 2014', '0')
        row['Actuals 2015'] = row.get('Actuals 2015', '0')
        row['Actuals 2016'] = row.get('Actuals 2016', '0')
        row['Actuals 2017'] = row.get('Actuals 2017', '0')
        for k,v in row.items():
            if 'Estimates' in k or 'Actuals' in k:
                row[k] = process_cell(v)

    outp = open('final/oak_park_budget_cleaned.csv', 'w')
    writer = csv.DictWriter(outp, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(all_rows)
    outp.close()

def match_rows(a, b):
    if  a['Fund ID'] == b['Fund ID'] and a['Department ID'] == b['Department ID'] and a['Program ID'] == b['Program ID'] and a['Account ID'] == b['Account ID']:
        return True
    else:
        return False

def process_cell(v):
    if v is None:
        v = 0
    v = v.replace('$', '').replace(',','')
    try:
        int(v)
        v=int(v)*-1
    except:
        v = 0
    return v

if __name__ == "__main__":
    cleanup()
