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
    
    all_rows = {}
    # start with 2021 budget
    print('importing 2021 budget ...')
    with open(budget_2021) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            unique_key = create_unique_key(row)
            if unique_key not in all_rows:
                all_rows[unique_key] = {}
            for k, v in row.items():
                if k in ['Actuals 2018', 'Actuals 2019', 'Estimates 2020', 'Estimates 2021']:
                    all_rows[unique_key][k] = set_or_add(all_rows[unique_key], row, k)
                else:
                    all_rows[unique_key][k] = v
    
    print ('imported %s rows' % len(all_rows))
    
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
        for year in range(2020, 2022):
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
        'Actuals 2016': 168366528,
        'Actuals 2017': 175297842,
        'Actuals 2018': 132912921,
        'Actuals 2019': 144118821,
        'Estimates 2020': 198502979,
        'Estimates 2021': 150680135,
    }

    for k, v in correct_sums.items():
        summed_value = sum_value(rows_to_print, k)
        if summed_value == v:
            print('%s: %s : sum is correct' % (k,v))
        else:
            print('%s: %s : sum is incorrect' % (k,v))
            print('  off by %s' % (summed_value - v))
    
    print('writing output ...')       
    outp = open('final/oak_park_budget_cleaned.csv', 'w')
    writer = csv.DictWriter(outp, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(rows_to_print)
    outp.close()

def append_budget(filepath, keys, all_rows):
    rows_import = {}
    count = 0
    unique_key_sets = []

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

def match_rows(a, b):
    if  a['Fund ID'] == b['Fund ID'] and a['Department ID'] == b['Department ID'] and a['Program ID'] == b['Program ID'] and a['Account ID'] == b['Account ID']:
        return True
    else:
        return False

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
