# Pump data into predict, get output

# Compare output to the next ordered date of each item in the filtered NEXT PERIOD data

import os
import datetime
import predict
import colors
import pandas as pd
import numpy as np

prediction_csv_path = os.environ["PREDICTION_CSV_PATH"]
reality_csv_path = os.environ["REALITY_CSV_PATH"]
customer = os.environ["CUSTOMER"]

def test_prediction():
    print colors.line("okgreen", "--- Testing ---")
    prediction = predict.predict_order_date_of_items_for_customer(
        customer,
        prediction_csv_path,
        datetime.datetime.now())
    print "--- Comparing to reality... ---"
    data_frame = pd.read_csv(reality_csv_path, parse_dates=["date"], index_col="order")
    customer_data = data_frame.loc[
        (data_frame.customer == customer), ["date", "quantity", "materialId"]]
    items = customer_data["materialId"].unique()

    for material_id in items:
        print "--- Test: " + str(material_id)

        orders_with_items = data_frame.loc[
            ((data_frame.materialId == material_id) & (data_frame.customer == customer)),
            ["date", "quantity"]]
        sorted_item_orders = orders_with_items.sort_values("date")
        reality_date = sorted_item_orders.head(1)["date"].values[0]
        predicted_item = {}

        if material_id in prediction:
            predicted_item = prediction[material_id]

            if "next_order_date" in predicted_item:
                prediction_delta = np.timedelta64(predicted_item["next_order_date"] - reality_date, "D")
                success = (prediction_delta < np.timedelta64(1, "D")) and (prediction_delta > np.timedelta64(-1, "D"))
                message_color = "okgreen" if success else "warning"

                print "Confidence Level: " + str(predicted_item["confidence"])
                print "Predicted Date: " + str(predicted_item["next_order_date"])
                print "Reality Date: " + str(reality_date)
                print colors.line(message_color, "Delta: " + str(prediction_delta))
            else:
                print colors.line("warning", "No date was predicted")

        else:
            print "This item was not in previous orders"

test_prediction()
