import configparser
import synapseclient
import os
from synapse_span_table import SynapseSpanTable

# Config.
config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))
config.sections()

# Connect to Synapse.
syn = synapseclient.Synapse()
synProjectName= config['SYNAPSE']['ProjectName']
synUserName= config['SYNAPSE']['UserName']
apiKey= config['SYNAPSE']['apiKey']
syn.login(email=synUserName, apiKey=apiKey)

def afterTest() :
  global syn
  global synProjectName
  children = syn.getChildren(synProjectName)
  for entity in children:
    syn.delete(entity['id'])

#
# Test
#

TestName = 'Should insert records with different schemas into the same table.'
tableName = 'test'
columnLimit = 3
data1 = {
  "id": "1",
  "a": "1",
  "b": "1",
  "c": "1",
  "d": "1",
  "e": "1",
  "f": "1",
  "g": "1"
}
data2 = {
  "id": "2",
  "a": "2",
  "b": "2",
  "c": "2",
  "p": "2",
  "d": "2",
  "f": "2",
  "g": "2",
  "h": "2",
  "i": "2",
  "j": "2"
}
synapse_span_table = SynapseSpanTable(syn, synProjectName, tableName)
synapse_span_table.flexsert_span_table_record(tableName, data1, columnLimit)
synapse_span_table.flexsert_span_table_record(tableName, data2, columnLimit)
record1 = synapse_span_table.read_span_table_record(tableName, data1['id'])
record2 = synapse_span_table.read_span_table_record(tableName, data2['id'])
allValuesMatch = True
for key in data1.keys() :
  if record1[key] != data1[key] :
    allValuesMatch = False
for key in data2.keys():
  if record2[key] != data2[key]:
    allValuesMatch = False
if allValuesMatch:
  print('Passed: ' + TestName)
else :
  raise RuntimeError('Failed: ' + TestName) from error
afterTest()

#
# Test
#

TestName = 'Should update a record with the same schema.'
tableName = 'test'
columnLimit = 3
data = {
  "id": "1",
  "a": "1",
  "b": "1",
  "c": "1",
  "d": "1",
  "e": "1",
  "f": "1",
  "g": "1"
}
synapse_span_table = SynapseSpanTable(syn, synProjectName, tableName)
synapse_span_table.flexsert_span_table_record(tableName, data, columnLimit)
data['g'] = '1a'
synapse_span_table.flexsert_span_table_record(tableName, data, columnLimit)
recordUpdated = synapse_span_table.read_span_table_record(tableName, data['id'])
if recordUpdated['g'] == '1a' :
  print('Passed: ' + TestName)
else :
  raise RuntimeError('Failed: ' + TestName) from error
afterTest()

#
# @TODO Test
#

TestName = 'Should update a record with a different schema.'

#
# @TODO Test
#

TestName = 'Should properly handle other types of data.'

#
# @TODO Test
#

TestName = 'Should delete a record.'