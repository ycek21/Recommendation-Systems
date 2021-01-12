from data_splitter import partnerDataSplitter
from partner_data_reader import PartnerDataReader
from optimizer import Optimizer
import json
from datetime import datetime
from matplotlib import pyplot as plt
import pandas as pd


class SimulationCore():
    def __init__(self):
        pass

    def split_dataset_into_partners(self):
        partnerDataSplitter.split_dataSet_into_partners()

    def run_simulation_for_particular_partner(self, partner_id: str):
        partner = PartnerDataReader(
            partner_id)

        clickCost = partner.average_click_cost

        # print('partner.average_click_cost', clickCost)

        optimizer = Optimizer(
            partner.grouped_by_day, clickCost)

        for index in range(len(optimizer.data_from_partner) - 1):
            optimizer.optimize_day(optimizer.data_from_partner[index])

        plt.plot(optimizer.profit_gain_list)
        # plt.plot(optimizer.sustained_profit_list)

        # plt.plot(optimizer.accumulated_profit_gain)
        # plt.plot(optimizer.accumulated_sustained_profit)
        # print(optimizer.profit_ratio_list)

        # plt.plot(optimizer.profit_ratio_list)

        plt.show()

        dataframe_dictionary = {'profit_gain_list': optimizer.profit_gain_list,
                                'sustained_profit_list': optimizer.sustained_profit_list,
                                'accumulated_profit_gain': optimizer.accumulated_profit_gain,
                                'accumulated_sustained_profit': optimizer.accumulated_sustained_profit,
                                'profit_ratio_list': optimizer.profit_ratio_list
                                }
        print('optimizer.profit_gain_list', len(optimizer.profit_gain_list))
        print('optimizer.sustained_profit_list',
              len(optimizer.sustained_profit_list))

        print('optimizer.accumulated_profit_gain',
              len(optimizer.accumulated_profit_gain))
        print('optimizer.accumulated_sustained_profit',
              len(optimizer.accumulated_sustained_profit))
        print('optimizer.profit_ratio_list',
              len(optimizer.profit_ratio_list))

        dataframe = pd.DataFrame(dataframe_dictionary)

        dataframe.to_csv('dataframeJE.csv')

        optimizer.log_optimized_days(partner_id)

    def check_logs_with_validation_data(self, partner_id: str):
        validationPath = f'resources/validation_data/partner_riegiel_id_{partner_id}.json'
        createdLogsPath = f'logs_partner_id_{partner_id}.json'

        with open(validationPath) as validationFile:
            validationData = json.load(validationFile)
        with open(createdLogsPath) as createdLog:
            createdData = json.load(createdLog)

        return (validationData == createdData)
