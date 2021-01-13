from data_splitter import partnerDataSplitter
from partner_data_reader import PartnerDataReader
from optimizer import Optimizer
import json
from datetime import datetime
from simulation_core import SimulationCore

simulationCore = SimulationCore()

partner_id = 'C0F515F0A2D0A5D9F854008BA76EB537'
second_partner_id = '04A66CE7327C6E21493DA6F3B9AACC75'

simulationCore.run_simulation_for_particular_partner(
    partner_id)

print(simulationCore.check_logs_with_validation_data(
    partner_id))

simulationCore.generate_plot_profit_gain()
simulationCore.generate_plot_sustainded_profit()
simulationCore.generate_plot_profit_gain_and_sustained_profit()

simulationCore.generate_plot_accumulated_profit_gain()
simulationCore.generate_plot_accumulated_sustained_gain()
simulationCore.generate_plot_accumulated_profit_gain_and_sustained_profit()

simulationCore.generate_plot_accumulated_profit_gain_ratio()

# simulationCore.create_csv_with_results()
# simulationCore.run_simulation_for_particular_partner(
#     second_partner_id)

# print(simulationCore.check_logs_with_validation_data(
#     second_partner_id))
