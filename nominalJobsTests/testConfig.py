import unittest
from client.gal import TroiaClient
from testSettings import *
from bs4 import BeautifulSoup


class TestConfiguration(unittest.TestCase):

    def setUp(self):
        self.client = TroiaClient(ADDRESS)
        self.initialConfigParams = self._get_config_params()

    def tearDown(self):
        #revert any of the config changes
        response = self.client.post_config(self.initialConfigParams)
        self.assertEqual(200, response.status_code)
        self.client.delete()

    def _get_config_params(self):
        response = self.client.get_config()
        htmlPage = BeautifulSoup(response.content)

        configParams = {}
        configParams['JOBS_STORAGE'] = htmlPage.find_all("option", {'selected':'selected'})[0]['value']

        for inputTag in htmlPage.find_all("input"):
            try:
                configParams[inputTag['name']] = inputTag['value']
            except:
                pass
        return configParams

    def test_Status(self):
        response = self.client.status()
        self.assertEqual('OK', response['status'])
        self.assertEqual('OK', response['result']['status'])
        #self.assertEqual('OK', response['result']['job_storage_status'])

    @unittest.skip('Skipping until the test is fixed')
    def test_GetDefaultConfig(self):
        response = self.client.get_config()
        self.assertEqual(200, response.status_code)

    @unittest.skip('Skipping until the test is fixed')
    def test_SetWrongDbUrl(self):
        inputParams = {'JOBS_STORAGE':'DB_FULL',
                       'DB_DRIVER_CLASS':'com.mysql.jdbc.Driver',
                       'DB_URL':'dbUrl',
                       'DB_NAME':'Troia'
                      }
        response = self.client.post_config(inputParams)
        self.assertEqual(500, response.status_code)
        self.assertEqual(u'No suitable driver found for dbUrl?useUnicode=true&characterEncoding=utf-8', response.text)

    @unittest.skip('Skipping until the test is fixed')
    def test_SetWrongDbAccessSettings(self):
        inputParams = {'JOBS_STORAGE':'DB_FULL',
                       'DB_DRIVER_CLASS':'com.mysql.jdbc.Driver',
                       'DB_URL':'jdbc:mysql://localhost/',
                       'DB_NAME':'Troia',
                       'DB_PASSWORD':'dbPassword',
                       'DB_USER':'dbUser',
                       'DOWNLOADS_PATH':'dbDownloadPath'}
        response = self.client.post_config(inputParams)
        self.assertEqual(500, response.status_code)
        self.assertEqual(u'Access denied for user \'dbUser\'@\'localhost\' (using password: YES)', response.text)

    @unittest.skip('Skipping until the test is fixed')    
    def test_SetConfigParams(self):
        inputParams = {'CACHE_DUMP_TIME':'600',
                  'CACHE_SIZE':'100',
                  'DB_DRIVER_CLASS':'com.mysql.jdbc.Driver',
                  'DB_NAME':'Troia',
                  'DB_PASSWORD':'root',
                  'DB_URL':'jdbc:mysql://localhost/',
                  'DB_USER':'root',
                  'DOWNLOADS_PATH':'dbDownloadPath',
                  'EXECUTOR_THREADS_NUM':'10',
                  'FREEZE_CONFIGURATION_AT_START':'false',
                  'MEMCACHE_EXPIRATION_TIME':'100',
                  'MEMCACHE_PORT':'30',
                  'MEMCACHE_URL':'memCacheUrl',
                  'RESPONSES_CACHE_SIZE':'10',
                  'RESPONSES_DUMP_TIME':'100',
                  'JOBS_STORAGE':'DB_FULL'}
        response = self.client.post_config(inputParams)
        self.assertEqual(200, response.status_code)

        currentConfigParams = self._get_config_params()

        for key in inputParams.keys():
            self.assertEqual(inputParams[key], currentConfigParams[key])

    @unittest.skip('Skipping until the test is fixed')
    def test_ResetDB(self):
        response = self.client.resetDB()
        self.assertEqual(200, response.status_code)
