import pandas as pd
import os
import pickle
from datetime import datetime


class partnerDataSplitter():

    @staticmethod
    def split_dataSet_into_partners():
        criteo_as_dataFrame = pd.read_csv("resources/CriteoSearchData.csv", sep="\t", header=0,
                                          names=['Sale', 'SalesAmountInEuro', 'time_delay_for_conversion', 'click_timestamp',
                                                 'nb_clicks_1week', 'product_price', 'product_age_group', 'device_type', 'audience_id',
                                                 'product_gender', 'product_brand', 'prod_category1', 'prod_category2', 'prod_category3',
                                                 'prod_category4', 'prod_category5', 'prod_category6', 'prod_category7',
                                                 'product_country', 'product_id', 'product_title', 'partner_id', 'user_id'
                                                 ])

        # criteo_as_dataFrame['click_timestamp'] = [datetime.fromtimestamp(
        #     x) for x in criteo_as_dataFrame['click_timestamp']]
        sorted_criteo_as_dataFrame = criteo_as_dataFrame.sort_values(
            'click_timestamp')
        grouped_by_partner_id = sorted_criteo_as_dataFrame.groupby(
            'partner_id')

        for index, partnerData in grouped_by_partner_id:
            partnerData['click_timestamp'] = partnerData['click_timestamp'].apply(
                lambda x: str(pd.to_datetime(int(x), unit='s').date()))
            partnerFilePath = os.path.join(
                os.getcwd(), 'partners', 'partner_id_' + str(index) + '.csv')
            partnerData.to_csv(partnerFilePath, index=False)
