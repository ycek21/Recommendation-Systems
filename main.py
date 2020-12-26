from data_splitter import partnerDataSplitter
from partner_data_reader import PartnerDataReader

# partnerDataSplitter.split_dataSet_into_partners()

partner_04A66CE7327C6E21493DA6F3B9AACC75 = PartnerDataReader(
    '04A66CE7327C6E21493DA6F3B9AACC75')

print(partner_04A66CE7327C6E21493DA6F3B9AACC75.get_day(3))
