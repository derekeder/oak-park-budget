import csv

# link on Fund, Account, Department & Program ID

def cleanup():
    
    # 2021 budget
    f = open('raw/2021 Adopted Budget - VOP - Data2018-2021.csv', 'r')
    reader = csv.DictReader(f)
    all_rows = []
    for row in reader:
        for k,v in row.items():
            row[k] = process_row(k,v)
        all_rows.append(row)
    outp = open('final/oak_park_budget_cleaned.csv', 'w')
    
    writer = csv.DictWriter(outp, row.keys(), quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(all_rows)
    f.close()
    outp.close()

def process_row(k,v):
    if 'Estimates' in k or 'Actuals' in k:
        v = v.replace('$', '').replace(',','')
        try:
            int(v)
            v=int(v)*-1
        except:
            v = 0
    return v

if __name__ == "__main__":
    cleanup()
