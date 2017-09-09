import requests

address= '0x57d90b64a1a57749b0f932f1a3395792e12e7055'

apikey = 'QDZZNB41B2NMCYNZ7ENYSVQAFGMQ43EDHE'

class EtherStats(object):

  def __init__(self):
    #initialized None so that the ones which are not used in a particular API
    #don't cause a error, since it a GET query missing keyvalues won't cause an issue
    self.url = 'https://api.etherscan.io/api'
    self.apikey = apikey
    self.module = None
    self.action = None
    self.contractaddress = None
    self.address = None
    self.sort = None
    self.page = None
    self.offset = None
    self.tag = None

  def _apiQuery(self):

    params = {'module': self.module,
              'url': self.url,
              'action': self.action,
              'address': self.address,
              'tag': self.tag,
              'apikey': self.apikey,
              'sort': self.sort,
              'contractaddress': self.contractaddress,
              'page': self.page,
              'offset': self.offset,
              }
    try:
      r = requests.get(self.url, params)
      response = r.json()
      return response['result']
    except Exception as e:
      raise

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


  def getNormalTransactions(self, page=None, offset=None, startblock=0, endblock=99999999,
                                  sort='asc' ):
    """Get a list of 'Normal' Transactions by Address

    Note: (Returns up to a maximum of the last 10000 transactions only)
    (To get paginated results use page=<page number> and offset=<max records to return>)
    
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
    self.page = page
    self.offset = offset
    self.sort = sort
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
    """Get Contract ABI for Verified Contraact Source Codes
    Note:Newly verified Contracts are synched to the API servers within 5 minutes or less
    """
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

class EtherBlockStats(EtherStats):
  def __init__(self, address, module='block'):
    super(EtherBlockStats, self).__init__()
    self.module = module
    self.address = address

  def getBlockRewards(self, blockno = '2165403'):
    self.action = 'getblockreward'
    self.blockno = 'blockno'
    return super(getBlockRewards, self)._apiQuery()

class EtherEventLogs(EtherStats):
  """[Beta] The Event Log API was designed to provide an alternative to the native eth_getLogs. 

  Below are the list of supported filter parameters: 
  fromBlock, toBlock, address
  topic0, topic1, topic2, topic3 (32 Bytes per topic)
  topic0_1_opr (and|or between topic0 & topic1),
  topic1_2_opr (and|or between topic1 & topic2),
  topic2_3_opr (and|or between topic2 & topic3),
  topic0_2_opr (and|or between topic0 & topic2)

  * fromBlock and toBlock accepts the blocknumber (integer, NOT hex) or 'latest' (earliest & pending is NOT supported yet)
  * Topic Operator (opr) choices are either 'and' or 'or' and are restricted to the above choices only
  * fromBlock and toBlock parameters are required 
  * Either the address and/or topic(X) parameters are required, when multiple topic(X) parameters are used the topicX_X_opr (and|or operator) is also required
  * For performance & security considerations, only the first 1000 results are return. So please narrow down the filter parameters

  """
  def __init__(self, address, module='logs'):
    super(EtherBlockStats, self).__init__()
    self.module = module
    self.address = address

  def getEventLogs(self,fromBlock, toBlock, topic0, topic1, topic2, topic3,
                    topic0_1_opr, topic1_2_opr, topic2_3_opr, topic0_2_opr):
    self.fromBlock = fromBlock
    self.toBlock = toBlock
    if topic0:
      self.topic0 = topic0
    if topic1:
      self.topic1 = topic1
    if topic3:
      self.topic3 = topic3
    if topic0_1_opr:
      self.topic0_1_opr = topic0_1_opr
    if topic1_2_opr:
      self.topic1_2_opr = topic1_2_opr
    if topic2_3_opr:
      self.topic2_3_opr = topic2_3_opr
    if topic0_2_opr:
      self.topic0_2_opr = topic0_2_opr

class EtherTokenStats(EtherStats):
  def __init__(self, address):
    super(EtherTokenStats, self).__init__()
    self.contractaddress = address

  def getTokenSupply(self):
    """Get ERC20-Token TotalSupply by ContractAddress"""
    self.action= 'tokensupply'
    self.module = 'stats'
    return super(EtherTokenStats, self)._apiQuery()
    
  def getTokenAccountBalance(self, address):
    """Get ERC20-Token Account Balance for TokenContractAddress"""
    self.module = 'account'
    self.action = 'tokenBalance'
    self.address = 'address'


if __name__ == '__main__':
  e = EtherAccountStats(address)
  print e.getBalance()
  e = EtherTokenStats(address)
  print e.getTokenSupply()
