import config
import os
import predict
import datetime

prediction_csv_path = config.settings["prediction_csv_path"]
customer = config.settings["customer"]

predict.predict_order_date_of_items_for_customer(
    customer,
    prediction_csv_path,
    datetime.datetime.now()
)