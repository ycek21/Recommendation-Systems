from data_splitter import partnerDataSplitter
from partner_data_reader import PartnerDataReader
from optimizer import Optimizer
import json
from datetime import datetime
from matplotlib import pyplot as plt


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

        # plt.plot(optimizer.profit_gain_list)
        # plt.plot(optimizer.sustained_profit_list)

        # plt.plot(optimizer.accumulated_profit_gain)
        # plt.plot(optimizer.accumulated_sustained_profit)

        plt.plot(optimizer.profit_ratio_list)

        plt.show()

        optimizer.log_optimized_days(partner_id)

    def check_logs_with_validation_data(self, partner_id: str):
        validationPath = f'resources/validation_data/partner_riegiel_id_{partner_id}.json'
        createdLogsPath = f'logs_partner_id_{partner_id}.json'

        with open(validationPath) as validationFile:
            validationData = json.load(validationFile)
        with open(createdLogsPath) as createdLog:
            createdData = json.load(createdLog)

        return (validationData == createdData)
