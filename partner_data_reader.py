import pandas as pd


class PartnerDataReader():
    def __init__(self, partner_id):
        partner_filepath = f'./partners/partner_id_{partner_id}.csv'

        self.partner_dataFrame = pd.read_csv(partner_filepath)

        # timestamp changes to datetime
        # self.partner_dataFrame['click_timestamp'] = self.partner_dataFrame['click_timestamp'].apply(
        #     lambda x: str(pd.to_datetime(int(x), unit='s').date()))

        self.number_of_clicks_for_partner = len(self.partner_dataFrame)

        # ! dowiedziec sie czy wykluczyc produkty z product id = -1
        self.sum_of_sales_amount_in_euro = self.partner_dataFrame[
            self.partner_dataFrame['SalesAmountInEuro'] >= 0]['SalesAmountInEuro'].sum()

        self.average_click_cost = (
            0.12 * self.sum_of_sales_amount_in_euro) / self.number_of_clicks_for_partner

        self.grouped_by_day = []
        for index, group in self.partner_dataFrame.groupby('click_timestamp'):
            self.grouped_by_day.append(group)

        print(len(self.grouped_by_day))
