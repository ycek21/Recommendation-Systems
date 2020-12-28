from data_splitter import partnerDataSplitter
from partner_data_reader import PartnerDataReader
from optimizer import Optimizer
import json
from datetime import datetime

# partnerDataSplitter.split_dataSet_into_partners()

# partner_04A66CE7327C6E21493DA6F3B9AACC75 = PartnerDataReader(
#     '04A66CE7327C6E21493DA6F3B9AACC75')

# partner_C0F515F0A2D0A5D9F854008BA76EB537 = PartnerDataReader(
#     'C0F515F0A2D0A5D9F854008BA76EB537')


# optimizer = Optimizer(partner_04A66CE7327C6E21493DA6F3B9AACC75.grouped_by_day)

# for index in range(len(optimizer.data_from_partner) - 1):
#     optimizer.optimize_day(optimizer.data_from_partner[index])

# optimizer.log_optimized_days('04A66CE7327C6E21493DA6F3B9AACC75')


# optimizer = Optimizer(partner_C0F515F0A2D0A5D9F854008BA76EB537.grouped_by_day)

# for index in range(len(optimizer.data_from_partner) - 1):
#     optimizer.optimize_day(optimizer.data_from_partner[index])

# optimizer.log_optimized_days('C0F515F0A2D0A5D9F854008BA76EB537')

with open('resources/validation_data/partner_riegiel_id_C0F515F0A2D0A5D9F854008BA76EB537.json') as notMyFile:
    Rigieldata = json.load(notMyFile)


with open('logs_partner_id_C0F515F0A2D0A5D9F854008BA76EB537.json') as MyFile:
    myData = json.load(MyFile)

print(myData == Rigieldata)
