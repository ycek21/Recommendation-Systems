import pandas as pd


class PartnerDataReader():
    def __init__(self, partner_id):
        partner_filepath = f'./partners/partner_id_{partner_id}.csv'

        self.partner_dataFrame = pd.read_csv(partner_filepath)

        self.number_of_clicks_for_partner = len(self.partner_dataFrame)

        self.sum_of_sales_amount_in_euro = self._sum_sales_amount_in_euro()

        self.average_click_cost = self._calculate_click_cost()

        self.grouped_by_day = []

        self._group_partner_dataFrame_by_day()

    def _sum_sales_amount_in_euro(self):
        return self.partner_dataFrame[self.partner_dataFrame['SalesAmountInEuro']
                                      >= 0]['SalesAmountInEuro'].sum()
        # return self.partner_dataFrame[self.partner_dataFrame['Sale']
        #                               == 1]['SalesAmountInEuro'].sum()

    def _calculate_click_cost(self):
        return (0.12 * self.sum_of_sales_amount_in_euro) / self.number_of_clicks_for_partner

    def _group_partner_dataFrame_by_day(self):
        for index, group in self.partner_dataFrame.groupby('click_timestamp'):
            self.grouped_by_day.append(group)

    def get_day(self, day_number):
        return self.grouped_by_day[day_number]
