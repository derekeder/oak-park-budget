import csv

# link on Fund, Account, Department & Program ID

def cleanup():
    f = open('raw/2021 Adopted Budget - VOP - Data2018-2021.csv', 'r')
    reader = csv.DictReader(f)
    all_rows = []
    for row in reader:
        for k,v in row.items():
            if 'Estimates' in k or 'Actuals' in k:
                v = v.replace('$', '').replace(',','').replace('-','')
                try:
                    float(v)
                except:
                    v = 0
            row[k] = v
        all_rows.append(row)
    outp = open('final/oak_park_budget_cleaned.csv', 'w')
    writer = csv.DictWriter(outp, row.keys())
    writer.writeheader()
    writer.writerows(all_rows)
    f.close()
    outp.close()

if __name__ == "__main__":
    cleanup()
