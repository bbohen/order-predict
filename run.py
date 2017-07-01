import os
import predict
import datetime

prediction_csv_path = os.environ["PREDICTION_CSV_PATH"]
customer = os.environ["CUSTOMER"]

predict.predict_order_date_of_items_for_customer(
    customer,
    prediction_csv_path,
    datetime.datetime.now()
)