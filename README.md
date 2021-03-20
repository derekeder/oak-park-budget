Budget: Oak Park
=====================================

Explore the Village of Oak Park's budget from 2013 to 2021 and learn how the money is being spent.

Budget: Oak Park is a budget transparency tool for the Village of Oak Park, Illinois. It was built by Oak Park Residents Derek Eder and Alicia Chastain. It is not an official application from the Village.

By extracting data from the Village’s official budgets from 2017, 2019 and 2021, we were able to display and compare annual budgets from 2013 through 2021. The funds, departments and descriptions are as the Village officially reports them and are unchanged by us, with the exception of merging duplicate line items.

Our goal with this tool is to increase transparency around one of the most important but challenging parts of government: the budgeting process. We hope that by making this information more readily accessible and easier to understand, we can bring more informed voices into the discussions and debates around budget priorities in Oak Park.

For more information on the Oak Park Village budget and how we built this site, read our [Frequently Asked Questions »](https://budgetoakpark.com/faq.html)

#### Dependencies

- [jQuery](http://jquery.com)
- [python3](https://www.python.org/) (for CSV manipulation)
- [Backbone](http://backbonejs.org/) (javascript MVC framework)
- [Highcharts](http://www.highcharts.com/) (charting library)
- [Datatables](http://datatables.net) (sortable HTML tables)

## How to Re-Deploy
This code can be customized to visualize another data set.

####Data Prepatation
The budget data can be in various forms (CSV, google doc, Excel), but must adhere to a fixed format in order for the app to process it properly. Budget column headers include: Fund ID, Program ID, Department ID, Fund, Department, Description and. Values for Actuals and Estimates must be broken down into a separate column for each year.

Data for this project is drawn from 3 different budget CSVs and 2 description CSVs located in `data/raw`. The data is compiled into one CSV with the `data/cleanup.py` python script. To run the script:

```bash
cd data
python cleanup.py
```

See examples of prepped data:
  - [New Orleans](https://docs.google.com/spreadsheet/ccc?key=0AswuyKhD7LxVdGlERGdEckpaRDc4Q1RCN0tjZ2tMMGc&usp=sharing_eil#gid=0)
  - [Macoupin County](https://github.com/datamade/macoupin-budget/blob/master/data/macoupin-budget_1997-2014.csv)
  - [A blank template to populate](https://docs.google.com/spreadsheets/d/1I6xZe8syHTiLguZ56l6J1KW0nAJVrUilvq0eP-BpE2A/edit?usp=sharing)

####Configuration
1. Once the data is prepared, set dataSource in js/app.js to link up to your data.
  
  *If your budget data is in CSV form:*
  Drop the csv file in the data folder, and set dataSource to the file path.
  
  *If your data is in a google doc:*
  You will first need to publish the google doc to the web as a CSV. Then, set dataSource to the URL provided.
  
  ![alt-tag](https://cloud.githubusercontent.com/assets/1406537/3767681/94b15ba4-18cf-11e4-96b1-a2dca1f39c73.png) 
  ![alt-tag](https://cloud.githubusercontent.com/assets/1406537/3767658/55df1880-18cf-11e4-9593-51bc89b0744a.png)
  
2. Next, set the following configuration variables at the top of js/app.js:
  - startYear
  - endYear
  - activeYear
  - municipalityName

## Errors / bugs

If something is not behaving intuitively, it is a bug, and should be [reported as an issue](https://github.com/derekeder/oak-park-budget/issues)

You can also email info@budgetoakpark.com.

Copyright
---------

Copyright © 2021 DataMade (datamade.us), Derek Eder, Alicia Chastain, Nick Rougeux and Open City. Released under the MIT License.

See LICENSE for details https://raw.githubusercontent.com/derekeder/oak-park-budget/master/LICENSE.md
