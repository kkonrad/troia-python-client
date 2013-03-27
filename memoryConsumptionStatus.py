import csv
from client.gal import TroiaClient
from troia_client.testSettings import *
import time


def getMemoryStatus():
    client = TroiaClient(ADDRESS)
    csvFile = open('memoryConsumption_Status.csv','wb')
    csvWriter = csv.writer(csvFile, delimiter=',', quotechar='"')
    counter = 1
    while (counter > 0):
        response = client.status()
        result = response['result']
        csvData = [counter, response['status'], result['memory']['total'], result['memory']['free'], result['memory']['max'], result['memory']['used']]
        print csvData
        csvWriter.writerow(csvData)
        csvFile.flush()
        time.sleep(1)
        counter += 1

if __name__ == '__main__':
    getMemoryStatus()
