import random


class Optimizer():
    def __init__(self):
        self.products_seen_so_far = []

    def optimze_day(self):
        products_to_exclude_tomorrow = []

      # ! adjust method attributes

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
