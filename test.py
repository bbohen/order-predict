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
    test_results = {}
    successes = []
    warnings = []
    failures = []

    for material_id in items:
        print "--- Test: " + str(material_id)

        orders_with_items = data_frame.loc[
            ((data_frame.materialId == material_id) & (data_frame.customer == customer)),
            ["date", "quantity"]]
        sorted_item_orders = orders_with_items.sort_values("date")
        reality_date = sorted_item_orders.head(1)["date"].values[0]
        message_color = ""

        if material_id in prediction:
            predicted_item = prediction[material_id]

            if "next_order_date" in predicted_item:
                prediction_delta = np.timedelta64(predicted_item["next_order_date"] - reality_date, "D")
                success = (prediction_delta < np.timedelta64(1, "D")) and (prediction_delta > np.timedelta64(-1, "D"))
                warning = (prediction_delta < np.timedelta64(3, "D")) and (prediction_delta > np.timedelta64(-3, "D"))
                message_color = "okgreen" if success else "warning"

                if success:
                    successes.append(material_id)
                    message_color = "okgreen"
                elif warning:
                    warnings.append(material_id)
                    message_color = "warning"
                else:
                    failures.append(material_id)
                    message_color = "fail"

                print "Confidence Level : " + str(predicted_item["confidence"])
                print "Predicted Date   : " + str(predicted_item["next_order_date"])
                print "Reality Date     : " + str(reality_date)
                print colors.line(
                    message_color,
                    "Delta            : " + str(prediction_delta))

                test_results[material_id] = {
                    "confidence": predicted_item["confidence"],
                    "predicted_date": predicted_item["next_order_date"],
                    "reality_date": reality_date,
                    "prediction_delta": prediction_delta,
                    "success": success
                }

            else:
                print "Not ordering enough data to predict this item"

        else:
            print "This item was not in previous orders"

    # print successes
    success_percentage = 100 * (float(len(successes)) / float(len(test_results)))
    warning_percentage = 100 * (float(len(warnings)) / float(len(test_results)))
    failure_percentage = 100 * (float(len(failures)) / float(len(test_results)))

    print colors.line("okgreen", "--- Success percentage (within 1 day)    : " + str(success_percentage))
    print colors.line("warning", "--- Warning percentage (within 3 days)   : " + str(warning_percentage))
    print colors.line("fail", "--- Failure percentage (everything else) : " + str(failure_percentage))

    return test_results

test_prediction()
