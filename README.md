# order-predict

Work in progress attempt to predict the next time a customer will order an item based on historical data

## Configuration

Need to have historical ordering data in a `.csv` file with the following format

```bash
# test.csv
customer,order,materialId,uom,date,dayOfWeek,isHoliday,quantity
({int},{int},{int},{string},{string of date to be parsed},{int (1-7)},{boolean},{int}
132172613,1001223513,9211308,CS,05-24-2015,0,true,1.000
...
```

Configure settings within [the config file](config.py) as follows

## Usage

`run.py` needs the path to the historical ordering data as well as the desired customer id passed as environment variables.

```bash
python run.py
````

To test predicted results against real ordering data include a second `.csv` and run `test.py`

```bash
python test.py
``` 

## Output

The predictions are output in `.xlsx` format to a file specified in the config. `Time Until Next Order` is currently only using today"s date for comparison, making this dynamic is on the [todo](TODO.md) list.

Running the test will output statistics output in `.xlsx` format with a sheet representing overall results and a sheet specific to titems.