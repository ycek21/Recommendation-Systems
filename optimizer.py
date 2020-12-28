import random
import pandas as pd
import json
from datetime import datetime, timedelta


class Optimizer():
    def __init__(self, data_from_partner):
        self.data_from_partner = data_from_partner
        self.products_seen_so_far = []
        self.optimized_days = []
        self.previous_day = None

    def optimize_day(self, today_df: pd.DataFrame):
        products_to_exclude_tomorrow = []

        products_to_exclude_tomorrow = self.__get_excluded_products_pseudorandomly(
            self.products_seen_so_far, 20, 12)

        products_to_exclude_tomorrow_as_set = set(products_to_exclude_tomorrow)

        todays_products_as_set = set(today_df['product_id'])

        products_actually_excluded_tomorrow = todays_products_as_set.intersection(
            products_to_exclude_tomorrow_as_set)

        self._add_missing_days(today_df['click_timestamp'].iloc[0])

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
        self.previous_day = today_df['click_timestamp'].iloc[0]

    def _add_missing_days(self, today_date):
        if(self.previous_day == None):
            return

        today_date_as_date = datetime.strptime(today_date, '%Y-%m-%d')
        previous_date_as_date = datetime.strptime(
            self.previous_day, '%Y-%m-%d')

        dates_subtraction = today_date_as_date - previous_date_as_date

        if dates_subtraction.days > 1:
            for i in range(dates_subtraction.days - 1):
                day_to_add = today_date_as_date - \
                    ((dates_subtraction.days - 1) + i)

                self.optimized_days.append(
                    self._generate_empty_day(day_to_add))

    def _generate_empty_day(self, date):
        return {
            "day": date,
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
