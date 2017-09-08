import requests
import logging

logger = logging.getLogger('spam_application')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)


address= '0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a'

apikey = 'QDZZNB41B2NMCYNZ7ENYSVQAFGMQ43EDHE'

class EtherStats(object):

  def __init__(self):
    self.url = 'https://api.etherscan.io/api'
    self.apikey = apikey

  def _apiQuery(self):

    params = {'module': self.module,
              'url': self.url,
              'action': self.action,
              'address': self.address,
              'tag': self.tag,
              'apikey': self.apikey}
    try:
      r = requests.get(self.url, params)
      response = r.json()
      return response
    except Exception as e:
      logger.error(e)

class EtherAccountStats(EtherStats):
  """API for finding accounts stats for a given Ether address"""

  def __init__(self, address, module='account'):
    super(EtherAccountStats, self).__init__()
    self.module = module
    self.address = address

  def getBalance(self):
    """Get Ether Balance for a single Address"""
    self.action = 'balance'
    self.tag = 'latest'
    return super(EtherAccountStats, self)._apiQuery()


  def getBalanceMultiple(self, addresses):
    """Get Ether Balance for multiple Addresses in a single call
    
    :param addresses: list of addresses
    :type addresses: list
    :returns: Ex - 
    {"status":"1","message":"OK",
    "result":[{"account":"0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a", "balance":"40807168564070000000000"},
              {"account":"0x198ef1ec325a96cc354c7266a038be8b5c558f67","balance":"66926418709092372528"}]}
    :rtype: {json}
    """
    self.action = 'balancemulti'
    self.tag = 'latest'
    return super(EtherAccountStats, self)._apiQuery()


  def getNormalTransactions(self, startblock=0, endblock=99999999):
    """Get a list of 'Normal' Transactions by Address

    Note: (Returns up to a maximum of the last 10000 transactions only)
    
    :param startblock: startig blockno to retreive results, defaults to 0
    :type startblock: number, optional
    :param endblock: ending blockNo to retrieve results, defaults to 99999999
    :type endblock: number, optional
    :returns: list of transactions
    :rtype: {json}
    """
    
    self.action = 'txlist'
    self.startblock = startblock
    self.endblock = endblock
    return super(EtherAccountStats, self)._apiQuery()


  def getInternalTransactions(self, startblock=0, endblock=2702578):
    """Get a list of 'Internal' Transactions by Address
    [Optional Parameters] startblock: starting blockNo to retrieve results, endblock: ending blockNo to retrieve results
    """
    self.action = txlistinternal
    self.startblock = startblock
    self.endblock = endblock
    return super(EtherAccountStats, self)._apiQuery()


  def getBlocksMined(self):
    """Get a list of Blocks Mined by Address"""
    self.action = getminedblocks
    return super(EtherAccountStats, self)._apiQuery()

class EtherContractsStats(EtherStats):

  def __init__(self, address, module='contract'):
    super(EtherContractsStats, self).__init__()
    self.mdoule = module
    self.address = address

  def getContractABI(self):
    """Get Contract ABI for Verified Contraact Source Codes"""
    self.action = getabi
    logger.info("Getting mined blocks for address %s"%self.address)
    return super(EtherContractsStats, self)._apiQuery()    

class EtherTransactionStats(EtherStats):

  def __init__(self, address, module='transaction'):
    super(EtherTransactionStats, self).__init__()
    self.module = module
    self.address = address

  def checkExecutionStatus(self):
    """[BETA] check contract Execution status (if there was an error during contract execution)
    Note: isError":"0" = Pass , isError":"1" = Error during Contract Execution 
    """
    self.action = getstatus
    return super(EtherTransactionStats, self)._apiQuery()



if __name__ == '__main__':
  e = EtherAccountStats(address)
  logger.info(e.getBalance())
  logger.info(e.getBalanceMultiple([0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a,\
                            0x63a9975ba31b0b9626b34300f7f627147df1f526,\
                            0x198ef1ec325a96cc354c7266a038be8b5c558f67]))
  logger.info(e.getNormalTransactions())

