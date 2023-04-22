from airtable import Airtable

# Connect to Airtable
# bible_everyday
my_api_token = 'patBn9mrDiXaSWaTh.edf3240b99d954e0b574e77feca3fbcc9803495ba4f1fc39d3f16a2a1e72d8a3'

my_base_id = 'appGRYw6YLw3UvBID'  #Bible_Everyday

my_table_id = 'tbl7gIpM0Xm7XyCCe'
my_table_name = 'Notify'

# my_notify_tb_id = 'tbl2lxF2E7Bj0YuDL'
# my_notify_tb_name = 'Table 2'

import datetime

def notify_data():

    airtable = Airtable(my_base_id, my_table_id, my_api_token)

    recordList = []

    records = airtable.get_all()

    for myRecord in records:
        # print(myRecord)
        recordList.append(myRecord)

    # print(recordList)

    return recordList

