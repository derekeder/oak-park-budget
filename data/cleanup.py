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
    print('***importing 2021 budget***')
    with open(budget_2021) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            all_rows.append(row)
    
    print ('imported %s rows' % len(all_rows))
    
    # append 2019 budget
    print('***importing 2019 budget***')
    with open(budget_2019) as csvfile:
        reader = csv.DictReader(csvfile)
        rows_2019 = []
        count = 0
        for row in reader:
            for main_row in all_rows:
                if match_rows(row, main_row):
                    row['imported'] = True
                    main_row['Actuals 2016'] = row['Actuals 2016']
                    main_row['Actuals 2017'] = row['Actuals 2017']
                    count = count + 1
            rows_2019.append(row)

        print ('matched %s rows' % count) 

        # import the rows we didn't match
        count = 0
        for row in rows_2019:
            if 'imported' not in row.keys():
                count = count + 1
                all_rows.append(row)

        print ('imported %s additional rows' % count) 
        print ('rows parsed: %s' % len(rows_2019))

    # append 2017 budget
    print('***importing 2017 budget***')
    with open(budget_2017) as csvfile:
        reader = csv.DictReader(csvfile)
        rows_2017 = []
        count = 0
        for row in reader:
            for main_row in all_rows:
                if match_rows(row, main_row):
                    row['imported'] = True
                    main_row['Actuals 2013'] = row['Actuals 2013']
                    main_row['Actuals 2014'] = row['Actuals 2014']
                    main_row['Actuals 2015'] = row['Actuals 2015']
                    count = count + 1
            rows_2017.append(row)

        print ('matched %s rows' % count)

        # import the rows we didn't match
        count = 0
        for row in rows_2017:
            if 'imported' not in row.keys():
                count = count + 1
                all_rows.append(row)

        print ('imported %s additional rows' % count) 
        print ('rows parsed: %s' % len(rows_2017)) 
        print ('final length: %s' % len(all_rows))
    
    # loop through the result and fill in blanks with zeroes
    for row in all_rows:
        # note - second stop parameter is not inclusive in the range
        for year in range(2013, 2020): 
            row['Actuals %s' % year] = row.get('Actuals %s' % year, '0')
        for year in range(2020, 2022):
            row['Estimates %s' % year] = row.get('Estimates %s' % year, '0')

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
        return 0
    v = v.replace('$', '').replace(',','')
    try:
        int(v)
        v=int(v)*-1
    except:
        v = 0
    return v

if __name__ == "__main__":
    cleanup()
