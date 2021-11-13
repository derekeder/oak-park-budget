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
        'Estimates 2021',
        'Estimates 2022',
    ]

    budget_2022 = 'raw/2022 Recommended Budget - VOP.csv'
    budget_2021 = 'raw/2021 Adopted Budget - VOP - Data2018-2021.csv'
    budget_2019 = 'raw/2019 Adopted Budget - VOP - Data2016-2017.csv'
    budget_2017 = 'raw/2017 Adopted Budget - Data2013-2015.csv'
    dept_descriptions = 'raw/VOP Department descriptions - VOP Departments.csv'
    fund_descriptions = 'raw/VOP Department descriptions - VOP Funds.csv'
    
    all_rows = {}
    # start with 2022 budget
    print('importing 2022 budget ...')
    with open(budget_2022) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            unique_key = create_unique_key(row)
            if unique_key not in all_rows:
                all_rows[unique_key] = {}
            for k, v in row.items():
                if k in ['Estimates 2022']:
                    all_rows[unique_key][k] = set_or_add(all_rows[unique_key], row, k)
                else:
                    all_rows[unique_key][k] = v
    
    print ('imported %s rows' % len(all_rows))
    
    # append 2021 budget
    print('importing 2021 budget ...')
    append_budget(budget_2021, ['Actuals 2018', 'Actuals 2019', 'Estimates 2020', 'Estimates 2021'], all_rows)
    
    # append 2019 budget
    print('importing 2019 budget ...')
    append_budget(budget_2019, ['Actuals 2016','Actuals 2017'], all_rows)

    # append 2017 budget
    print('importing 2017 budget ...')
    append_budget(budget_2017, ['Actuals 2013','Actuals 2014','Actuals 2015'], all_rows)
    
    print ('final length: %s' % len(all_rows))
    
    print('cleaning values ...')
    # loop through the result and fill in blanks with zeroes
    rows_to_print = []
    for unique_key, row in all_rows.items():
        # note - second stop parameter is not inclusive in the range
        for year in range(2013, 2020): 
            row['Actuals %s' % year] = row.get('Actuals %s' % year, '0')
        for year in range(2020, 2023):
            row['Estimates %s' % year] = row.get('Estimates %s' % year, '0')

        for k,v in row.items():
            if 'Estimates' in k or 'Actuals' in k:
                row[k] = invert_cell(process_cell(v))
        
        rows_to_print.append(row)

    print('testing sums ...')
    correct_sums = {
        'Actuals 2013': 116102095,
        'Actuals 2014': 127783862,
        'Actuals 2015': 157918447,
        'Actuals 2016': 168010484,
        'Actuals 2017': 175297842,
        'Actuals 2018': 132912921,
        'Actuals 2019': 144118821,
        'Estimates 2020': 198502979,
        'Estimates 2021': 150680135,
        'Estimates 2022': 171891925,
    }

    for k, v in correct_sums.items():
        summed_value = sum_value(rows_to_print, k)
        if summed_value == v:
            print('%s: %s : sum is correct' % (k,v))
        else:
            print('%s: %s : sum is incorrect' % (k,v))
            print('  off by %s' % (summed_value - v))
    
    print('adding department descriptions ...')
    with open(dept_descriptions) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for p in rows_to_print:
                if row['Department ID'] == p['Department ID']:
                    p['Department Description'] = row['Description']

    print('adding fund descriptions ...')
    with open(fund_descriptions) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for p in rows_to_print:
                if row['Fund ID'] == p['Fund ID']:
                    p['Fund Description'] = row['Description']
    
    fieldnames.append('Department Description')
    fieldnames.append('Fund Description')
    print('writing output ...')       
    outp = open('final/oak_park_budget_cleaned.csv', 'w')
    writer = csv.DictWriter(outp, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(rows_to_print)
    outp.close()

def append_budget(filepath, keys, all_rows):
    rows_import = {}

    # read in the flie to a dict
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            unique_key = create_unique_key(row)
            if unique_key not in all_rows:
                all_rows[unique_key] = {}
            for k, v in row.items():
                if k in keys:
                    all_rows[unique_key][k] = set_or_add(all_rows[unique_key], row, k)
                else:
                    all_rows[unique_key][k] = v

def sum_value(l, k):
    val = 0
    for row in l:
        val += row[k]
    return val

def create_unique_key(a):
    return ('%s-%s-%s-%s' %(a['Fund ID'],a['Department ID'],a['Program ID'],a['Account ID']))

def set_or_add(a, b, k):
    val = a.get(k, 0)
    val = process_cell(val)
    val += process_cell(b[k])
    return val

def process_cell(v):
    if v is None:
        return 0
    if isinstance(v, str): 
        v = v.replace('$', '').replace(',','')
    try:
        v=int(v)
    except:
        v = 0
    return v

def invert_cell(v):
    return int(v)*-1

if __name__ == "__main__":
    cleanup()
