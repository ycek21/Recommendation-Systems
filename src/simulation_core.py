from data_splitter import partnerDataSplitter
from partner_data_reader import PartnerDataReader
from optimizer import Optimizer
import json
from datetime import datetime
from matplotlib import pyplot as plt
import pandas as pd


class SimulationCore():
    def __init__(self):
        self.optimizer = None

    def split_dataset_into_partners(self):
        partnerDataSplitter.split_dataSet_into_partners()

    def run_simulation_for_particular_partner(self, partner_id: str):
        partner = PartnerDataReader(
            partner_id)

        clickCost = partner.average_click_cost

        self.optimizer = Optimizer(
            partner.grouped_by_day, clickCost)

        for index in range(len(self.optimizer.data_from_partner) - 1):
            self.optimizer.optimize_day(
                self.optimizer.data_from_partner[index])

        self.optimizer.log_optimized_days(partner_id)

    def generate_plot_profit_gain(self):
        plt.plot(self.optimizer.profit_gain_list)
        plt.grid()
        plt.xlabel('Days of simulation')
        plt.ylabel('Profit gain')
        plt.legend(['C0F515F0A2D0A5D9F854008BA76EB537'])
        plt.show()

    def generate_plot_sustainded_profit(self):
        plt.plot(self.optimizer.sustained_profit_list)
        plt.grid()
        plt.xlabel('Days of simulation')
        plt.ylabel('Sustained profit')
        plt.legend(['C0F515F0A2D0A5D9F854008BA76EB537'])
        plt.show()

    def generate_plot_accumulated_profit_gain(self):
        plt.plot(self.optimizer.accumulated_profit_gain)
        plt.grid()
        plt.xlabel('Days of simulation')
        plt.ylabel('Accumulated profit gain')
        plt.legend(['C0F515F0A2D0A5D9F854008BA76EB537'])
        plt.show()

    def generate_plot_accumulated_sustained_gain(self):
        plt.plot(self.optimizer.accumulated_sustained_profit)
        plt.grid()
        plt.xlabel('Days of simulation')
        plt.ylabel('Accumulated sustained gain')
        plt.legend(['C0F515F0A2D0A5D9F854008BA76EB537'])
        plt.show()

    def generate_plot_profit_gain_and_sustained_profit(self):
        plt.plot(self.optimizer.profit_gain_list)
        plt.plot(self.optimizer.sustained_profit_list)
        plt.grid()
        plt.xlabel('Days of simulation')
        plt.ylabel('EUR')
        plt.legend(['Profit gain', 'Sustained gain'])
        plt.show()

    def generate_plot_accumulated_profit_gain_and_sustained_profit(self):
        plt.plot(self.optimizer.accumulated_profit_gain)
        plt.plot(self.optimizer.accumulated_sustained_profit)
        plt.grid()
        plt.xlabel('Days of simulation')
        plt.ylabel('EUR')
        plt.legend(['Accumulated profit gain', 'Accumulated sustained gain'])
        plt.show()

    def generate_plot_accumulated_profit_gain_ratio(self):
        plt.plot(self.optimizer.profit_ratio_list)
        plt.grid()
        plt.xlabel('Days of simulation')
        plt.ylabel('Accumulated profit gain ratio')
        plt.legend(['C0F515F0A2D0A5D9F854008BA76EB537'])
        plt.show()

    def check_logs_with_validation_data(self, partner_id: str):
        validationPath = f'resources/validation_data/partner_riegiel_id_{partner_id}.json'
        createdLogsPath = f'logs_partner_id_{partner_id}.json'

        with open(validationPath) as validationFile:
            validationData = json.load(validationFile)
        with open(createdLogsPath) as createdLog:
            createdData = json.load(createdLog)

        return (validationData == createdData)

    def create_csv_with_results(self):
        dataframe_dictionary = {'profit_gain_list': self.optimizer.profit_gain_list,
                                'sustained_profit_list': self.optimizer.sustained_profit_list,
                                'accumulated_profit_gain': self.optimizer.accumulated_profit_gain,
                                'accumulated_sustained_profit': self.optimizer.accumulated_sustained_profit,
                                'profit_ratio_list': self.optimizer.profit_ratio_list
                                }
        dataframe = pd.DataFrame(dataframe_dictionary)

        dataframe.to_csv('results_dataframe_JE.csv')
