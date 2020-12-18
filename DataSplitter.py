import pandas as pd
import os
import pickle


class partnerDataSplitter():

    @staticmethod
    def split_dataSet_into_partners(self):
        criteo_as_dataFrame = pd.read_csv('criteoCategorized_as_category.csv')
        number_of_partners = criteo_as_dataFrame['partner_id'].value_counts()

        sorted_criteo_as_dataFrame = criteo_as_dataFrame.sort_values(
            'click_timestamp', ascending=False)
        grouped_by_partner_id = sorted_criteo_as_dataFrame.groupby(
            'partner_id')

        for index, partnerData in grouped_by_partner_id:
            partnerFilePath = os.path.join(
                os.getcwd(), 'partners', 'partner_id_' + str(index) + '.csv')
            partnerData.to_csv(partnerFilePath, index=False)

        @staticmethod
        def validate_partner_data(self):
