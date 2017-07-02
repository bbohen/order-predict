# order-predict

Work in progress attempt to predict the next time a customer will order an item based on historical data

## Usage

Need to have historical ordering data in a `.csv` file with the following format

```bash
# test.csv
customer,order,materialId,uom,date,dayOfWeek,isHoliday,quantity
({int},{int},{int},{string},{string of date to be parsed},{int (1-7)},{boolean},{int}
132172613,1001223513,9211308,CS,05-24-2015,0,true,1.000
...
```

`run.py` needs the path to the historical ordering data as well as the desired customer id passed as environment variables.

```bash
PREDICTION_CSV_PATH=test.csv CUSTOMER=1000075613 python run.py
````

To test predicted results against real ordering data include a second `.csv` and run `test.py`

```bash
PREDICTION_CSV_PATH=test.csv REALITY_CSV_PATH=reality.csv CUSTOMER=1000075613 python test.py
``` 

## Output

The output will consist of results as seen below for each item the customer orders. `Time Until Next Order` is currently only using today"s date for comparison, making this dynamic is on the [todo](TODO.md) list.

```bash
---------------------------
Material ID: 5543871.0
Confidence: 14.2857142857
Last Order: 2015-05-19T20:00:00.000000000-0400
Next Order: 2015-06-04 08:00:00
Time Until Next Order: -759 days +21:03:04.406325
```

Running the test will output statistics about the accuracy of each items prediction, more to come here soon

```bash
------------------- Testing
Material ID: 1581263.0
Predicted Date: 2015-06-04 01:42:51.428571428
Confidence Level: 60.7142857143
Reality Date: 2015-06-02T20:00:00.000000000-0400
```