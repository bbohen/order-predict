import os
import time
import datetime
import pandas as pd
import numpy as np

def predict_order_date_of_items_for_customer(customer, csv_path, desired_date_time):
    print "Analyzing order data "
    print "Customer is " + customer
    start_time = time.time()

    # parse csv data
    data_frame = pd.read_csv(csv_path, parse_dates=["date"], index_col="order")
    # filter to customer, get relevant data
    customer_data = data_frame.loc[
        (data_frame.customer == customer), ["date", "quantity", "materialId"]]
    total_customer_orders = customer_data.index.unique().values
    items = customer_data["materialId"].unique()
    desired_date_time_64 = np.datetime64(desired_date_time)
    result_dic = {}
    result_list = []

    print "--- Customer has " + str(len(total_customer_orders)) + " orders with " + str(len(items)) + " items"

    # run calculations on every item ordered by the customer
    # is there a way to do this without the for loop? a method of dataframe maybe?
    for material_id in items:
        print "Material ID: " + str(material_id)

        # select orders that contain this item
        orders_with_items = data_frame.loc[
            ((data_frame.materialId == material_id) & (data_frame.customer == customer)),
            ["date", "quantity"]]

        # calculate the percentage of orders this item was in
        item_ordered_percentage = 100 * (
            float(len(orders_with_items.index)) / float(len(total_customer_orders)))

        # sort the selected orders by date
        sorted_item_orders = orders_with_items.sort_values("date")

        # reset values
        last_ordered_date = 0
        next_order_date = 0
        time_until_next_order = 0

        # need more than 1 order to predict a trend (for now)
        if len(sorted_item_orders) > 1:
            sorted_item_orders_diff = sorted_item_orders["date"].diff()
            days_between_orders = sorted_item_orders_diff[
                sorted_item_orders_diff != np.timedelta64(0, "D")]
            average_days_between_orders = days_between_orders.mean()
            last_ordered_date = sorted_item_orders.tail(1)["date"].values[0]
            next_order_date = last_ordered_date + average_days_between_orders
            time_until_next_order = next_order_date - desired_date_time_64

            print "Confidence            : " + str(item_ordered_percentage)
            print "Last Order            : " + str(last_ordered_date)
            print "Next Order            : " + str(next_order_date)
            print "Time Until Next Order : " + str(time_until_next_order)

            # Dictionary to test again
            result_dic[material_id] = {
                "confidence": item_ordered_percentage,
                "last_ordered_date": last_ordered_date,
                "predicted_next_order_date": next_order_date,
                "time_until_next_order": time_until_next_order
            }

            result_list.append({
                "material_id": material_id,
                "confidence": item_ordered_percentage,
                "last_ordered_date": last_ordered_date,
                "predicted_next_order_date": next_order_date,
                "time_until_next_order": time_until_next_order
            })
        else:
            message = "Not ordering enough data to predict this item"

            print message

            result_dic[material_id] = {
                "confidence": item_ordered_percentage,
                "message": message
            }

        print "---"

    #Do excel stuff (maybe move this to run.py?)
    excel_output_file_name = "predictions.xlsx"
    writer = pd.ExcelWriter(excel_output_file_name, engine="xlsxwriter")
    item_results_data_frame = pd.DataFrame(result_list, columns=["material_id", "confidence", "last_ordered_date", "predicted_next_order_date", "time_until_next_order"])
    item_results_data_frame.to_excel(writer, sheet_name="Predictions")
    writer.save()

    print "Predictions written to: " + excel_output_file_name
    print "--- Report generated in %s seconds ---" % (time.time() - start_time)

    return result_dic
