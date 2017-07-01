# order-predict

Work in progress attempt to predict the next time a customer will order an item based on historical data

## Usage

Need to have historical ordering data in a `.csv` file with the following format

```
customer,order,materialId,uom,date,dayOfWeek,isHoliday,quantity
({int},{int},{int},{string},{string of date to be parsed},{int (1-7)},{boolean},{int}
1321`72613,1001223513,9211308,CS,05-24-2015,0,true,1.000
...
```

The path to the historical ordering data as well as the desired customer id need to be passed as environment variables

`CSVPATH=test.csv CUSTOMER=1000072613 python predict.py`

The output will consist of results as seen below for each item the customer orders somewhat frequently. `Time Until Next Order` is currently only using today's date for comparison, making this dynamic is on the [todo](TODO.md) list.

```
---------------------------
Material ID: 5543871.0
Confidence: 14.2857142857
Last Order: 2015-05-19T20:00:00.000000000-0400
Next Order: 2015-06-04 08:00:00
Time Until Next Order: -759 days +21:03:04.406325
---------------------------
```