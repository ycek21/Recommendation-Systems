import random
import pandas as pd
import json
from datetime import datetime, timedelta


class Optimizer():
    def __init__(self, data_from_partner, clickCostForPartner):
        self.data_from_partner = data_from_partner
        self.products_seen_so_far = []
        self.optimized_days = []
        self.clickCost = clickCostForPartner
        self.previous_optimized_day = None
        self.profit_gain_list = []
        self.sustained_profit_list = []
        self.accumulated_profit_gain = []
        self.accumulated_sustained_profit = []
        self.profit_ratio_list = []

    def optimize_day(self, today_df: pd.DataFrame):
        products_to_exclude_tomorrow = []

        products_to_exclude_tomorrow = self.__get_excluded_products_pseudorandomly(
            self.products_seen_so_far, 3.1, 12)

        products_to_exclude_tomorrow_as_set = set(products_to_exclude_tomorrow)

        todays_products_as_set = set(today_df['product_id'])

        products_actually_excluded_tomorrow = todays_products_as_set.intersection(
            products_to_exclude_tomorrow_as_set)

        self._add_missing_days(today_df['click_timestamp'].iloc[0])

        self._calculate_indicators(
            today_df, products_actually_excluded_tomorrow)

        optimized_day = {
            "day": today_df['click_timestamp'].iloc[0],
            "productsSeenSoFar": self.products_seen_so_far,
            "productsToExclude": sorted(products_to_exclude_tomorrow),
            "productsActuallyExcluded": sorted(list(products_actually_excluded_tomorrow))
        }

        self.optimized_days.append(optimized_day)

        product_seen_so_far_set = set(self.products_seen_so_far)
        product_seen_so_far_set.update(todays_products_as_set)

        self.products_seen_so_far = sorted(list(product_seen_so_far_set))
        self.previous_optimized_day = today_df['click_timestamp'].iloc[0]

    def _add_missing_days(self, today_date):
        if(self.previous_optimized_day == None):
            return

        today_date_as_date = datetime.strptime(today_date, '%Y-%m-%d')
        previous_date_as_date = datetime.strptime(
            self.previous_optimized_day, '%Y-%m-%d')

        dates_subtraction = today_date_as_date - previous_date_as_date

        if dates_subtraction.days > 1:
            for i in range(dates_subtraction.days - 1):
                amount_of_days_to_subtract = ((dates_subtraction.days - 1) - i)
                day_to_add = today_date_as_date - \
                    timedelta(days=amount_of_days_to_subtract)
                self._add_missing_day_to_plots_data()

                self.optimized_days.append(
                    self._generate_empty_day(day_to_add))

    def _generate_empty_day(self, date):
        return {
            "day": datetime.strftime(date, '%Y-%m-%d'),
            "productsSeenSoFar": [],
            "productsToExclude": [],
            "productsActuallyExcluded": []
        }

    def log_optimized_days(self, partner_id):

        logs = {
            "strategy": "random",
            "days": self.optimized_days
        }

        logs_filename = f'logs_partner_id_{partner_id}.json'

        logs_file = open(logs_filename, 'w')
        json.dump(logs, logs_file)

        logs_file.close()

    def __get_excluded_products_pseudorandomly(self, products, how_many_ratio, random_seed):
        dummy_list_of_potentially_excluded_products = products
        dummy_list_of_potentially_excluded_products = list(
            dummy_list_of_potentially_excluded_products)

        dummy_list_of_potentially_excluded_products.sort()
        dummy_how_many_products = round(
            len(dummy_list_of_potentially_excluded_products) / how_many_ratio)

        random.seed(random_seed)
        excluded_products = random.sample(
            dummy_list_of_potentially_excluded_products,  dummy_how_many_products)

        return excluded_products

    def _add_missing_day_to_plots_data(self):
        self.profit_gain_list.append(0)
        self.sustained_profit_list.append(0)
        self.accumulated_profit_gain.append(
            self.accumulated_profit_gain[-1])
        self.accumulated_sustained_profit.append(
            self.accumulated_sustained_profit[-1])
        self.profit_ratio_list.append(self.profit_ratio_list[-1])

    def _calculate_indicators(self, today_df, products_actually_excluded_tomorrow):
        actually_excluded_rows = today_df[today_df['product_id'].isin(
            list(products_actually_excluded_tomorrow))]

        today_df_after_subtraction_actually_excluded_rows = today_df[~today_df['product_id'].isin(
            list(products_actually_excluded_tomorrow))]

        today_profit_gain = self._calculate_profit_gain(actually_excluded_rows)

        today_sustained_profit = self._calculate_sustained_profit(
            today_df_after_subtraction_actually_excluded_rows)

        today_accumulated_profit_gain, today_accumulated_sustained_profit = self._calculate_accumulated_profit_gain_and_sustained_profit(
            today_profit_gain, today_sustained_profit)

        # ? CALCULATE TODAY PROFIT RATIO

        today_profit_ratio = (today_accumulated_profit_gain /
                              today_accumulated_sustained_profit)
        if(today_accumulated_sustained_profit != 0):
            self.profit_ratio_list.append(today_profit_ratio)

    def _calculate_profit(self, data: pd.DataFrame):
        number_of_clicks_in_day = len(data)
        partner_income = data[data['SalesAmountInEuro']
                              >= 0]['SalesAmountInEuro'].sum()

        return (number_of_clicks_in_day * self.clickCost) - (partner_income * 0.22)

    def _calculate_profit_gain(self, actually_excluded_rows):
        today_profit_gain = self._calculate_profit(actually_excluded_rows)
        self.profit_gain_list.append(today_profit_gain)
        return today_profit_gain

    def _calculate_sustained_profit(self, today_df_after_subtraction_actually_excluded_rows):
        today_sustained_profit = self._calculate_profit(
            today_df_after_subtraction_actually_excluded_rows)
        today_sustained_profit = today_sustained_profit * -1
        self.sustained_profit_list.append(today_sustained_profit)

        return today_sustained_profit

    def _calculate_accumulated_profit_gain_and_sustained_profit(self, today_profit_gain, today_sustained_profit):
        today_accumulated_profit_gain = 0
        today_accumulated_sustained_profit = 0

        if(len(self.accumulated_profit_gain) == 0):
            today_accumulated_profit_gain = today_profit_gain
            today_accumulated_sustained_profit = today_sustained_profit
            self.accumulated_profit_gain.append(
                today_accumulated_profit_gain)
            self.accumulated_sustained_profit.append(
                today_accumulated_sustained_profit)
        else:
            today_accumulated_profit_gain = self.accumulated_profit_gain[-1] + \
                today_profit_gain
            today_accumulated_sustained_profit = self.accumulated_sustained_profit[-1] + \
                today_sustained_profit
            self.accumulated_profit_gain.append(today_accumulated_profit_gain)
            self.accumulated_sustained_profit.append(
                today_accumulated_sustained_profit)

        return today_accumulated_profit_gain, today_accumulated_sustained_profit
