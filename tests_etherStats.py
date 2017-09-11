from etherStats import EtherAccountStats
import json
from etherStats_testData import normalTransactionsData, normalTransactionsData2, internalTransactionsData, internalTransactionsData_paginated, getBalanceData

address = '0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae'
apikey = 'QDZZNB41B2NMCYNZ7ENYSVQAFGMQ43EDHE'


class TestAccountStats(object):

  # def setup_client(self):
  #   self.client = EtherAccountStats(address)

  def test_getBalance(self):

    test_data = {"status":"1","message":"OK","result":"740021582819750779479303"}
    assert EtherAccountStats(address, apikey).getBalance() == test_data


  def test_getBalanceMultiple(self):
    addressList = '0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a',\
                  '0x63a9975ba31b0b9626b34300f7f627147df1f526',\
                  '0x198ef1ec325a96cc354c7266a038be8b5c558f67'

    assert EtherAccountStats(address, apikey).getBalanceMultiple(addressList) == getBalanceData


  def test_getNormalTransactions(self):

    errors = []

    #transactions will vary, also no. of confirmations, so asserting for immutable part
    if not EtherAccountStats(address, apikey).getNormalTransactions()['result'][0]['blockNumber'] == normalTransactionsData['result'][0]['blockNumber']:
      errors.append("Block number check failed")
    if not EtherAccountStats(address, apikey).getNormalTransactions()['result'][0]['input'] == normalTransactionsData['result'][0]['input']:
      errors.append("Input data not correct")

    # assert no error message has been registered, else print messages
    assert not errors, "errors occured:\n{}".format("\n".join(errors))


  def test_getNormalTransactions_paginated(self):

    errors = []

    response = EtherAccountStats(address, apikey).getNormalTransactions(page=2, offset =1)

       #transactions will vary, also no. of confirmations, so asserting for immutable part
    if not response['result'][0]['blockNumber'] == normalTransactionsData2['result'][0]['blockNumber']:
      errors.append("Block number check failed")
    if not response['result'][0]['input'] == normalTransactionsData2['result'][0]['input']:
      errors.append("Input data not correct")

    # assert no error message has been registered, else print messages
    assert not errors, "errors occured:\n{}".format("\n".join(errors))


  def test_internalTransactionsData(self):

    response = EtherAccountStats(address, apikey).getInternalTransactions()['result'][0:10]

    assert response == internalTransactionsData['result'][0:10]

  def test_interalTransactionsData_paginated(self):

    response = EtherAccountStats(address, apikey).getInternalTransactions(page=1, offset=2)

    assert response == internalTransactionsData_paginated




