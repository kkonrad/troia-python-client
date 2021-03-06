import unittest
import math
from client.gal import TroiaClient
from testSettings import *

class BugRegressionTests(unittest.TestCase):

    def setUp(self):
        self.client = TroiaClient(ADDRESS)

    def tearDown(self):
        self.client.delete()

    def test_GH_83(self):
        """ 
            Test for github issue https://github.com/ipeirotis/Troia-Server/issues/83
            Thanks to PeccatorImpius for reporting
        """
        categories = ['yes', 'no', 'blank']
        response = self.client.create(categories,
                                      prioritycalculator="CostBased",
                                      costMatrix=[{"value":5.0, "to":"blank", "from":"blank"},
                                                   {"value":5.0, "to":"no", "from":"blank"},
                                                   {"value":5.0, "to":"yes", "from":"blank"},
                                                   {"value":1.0, "to":"blank", "from":"no"},
                                                   {"value":0.0, "to":"no", "from":"no"},
                                                   {"value":1.0, "to":"yes", "from":"no"},
                                                   {"value":1.0, "to":"blank", "from":"yes"},
                                                   {"value":1.0, "to":"no", "from":"yes"},
                                                   {"value":0.0, "to":"yes", "from":"yes"}],
                                      epsilon=1.0E-4,
                                      iterations=10,
                                      algorithm='IDS',
                                      scheduler='NormalScheduler')
        self.assertEqual('OK', response['status'])
        assignedLabels = [
            ('A2G061ZJVQXGE', '21K74J79KQW6KZ5ZI8OFKD455U4HJ6', 'blank'),
            ('A2G061ZJVQXGE', '2FWPLSP75KLMPN1Y0O8QMQVJZMCZTJ', 'yes'),
            ('A224TK7J4KA1LV', '283PHIT3HVWAEB01E1AQA1727RZCKR', 'yes'),
            ('A224TK7J4KA1LV', '2S3YHVI44OS23CC3P15Z0BAPDTU4Y4', 'yes'),
            ('A224TK7J4KA1LV', '2NCXFCD45XCECEVNZ7BIV3TGXMSYWJ', 'yes'),
            ('A224TK7J4KA1LV', '295QQ7Q670519BUI3FTTYC1XUY7WC6', 'no'),
            ('A224TK7J4KA1LV', '255NVRH1KHO9X796JKEVHLKWFFDZQ5', 'yes'),
            ('A224TK7J4KA1LV', '21Z1Q6SVQ8H8RD8PIZWOJVCI99NN4U', 'yes'),
            ('A224TK7J4KA1LV', '2JGU98JHSTLBMCIANX0IWBJER94EQE', 'yes'),
            ('A224TK7J4KA1LV', '2Z3KH1Q6SVQ80ZQH28XLDOBVK0S2LC', 'yes'),
            ('A224TK7J4KA1LV', '2P3Z6R70G5R9R4QEF9574SSTVG2P9O', 'yes'),
            ('A224TK7J4KA1LV', '25UCF0CP5KXPC95DUBPGCPM7VGWWX9', 'yes'),
            ('A224TK7J4KA1LV', '2AOYTWX4H3H282M8LN7IEIJRJNW4ZT', 'no'),
            ('A224TK7J4KA1LV', '2J5JQ2172Z9998O6WZ3VMBU1B1FZR6', 'no'),
            ('A224TK7J4KA1LV', '2SIHFL42J1LYOZT2ELD0QGFKPVS2NE', 'yes'),
            ('A224TK7J4KA1LV', '2W36VCPWZ9RNWN0J7FJ70N3D1YKPA3', 'yes'),
            ('A224TK7J4KA1LV', '2F8S1CSTMOFXA4AZUQSE6DNXRXCROW', 'yes'),
            ('A224TK7J4KA1LV', '2TRKSSZVXX2QNWCPW4FYONIW95IN5Z', 'no'),
            ('A224TK7J4KA1LV', '2L13NAB6BFMFYFGTU7STRFDGMA2HU2', 'yes'),
            ('A224TK7J4KA1LV', '2B3RGNTBJ3MMWONA1LE6AKHBH439VT', 'yes'),
            ('A224TK7J4KA1LV', '24ZMVHVKCJ01KBK2GXY9SQW69QD758', 'yes'),
            ('A224TK7J4KA1LV', '2V99Y8TNKIMZBDNFRVJ2WM0POD59W3', 'yes'),
            ('A224TK7J4KA1LV', '2FK4E6AUBXHWB8PAXN0VJZWDZ3NX1B', 'yes'),
            ('A224TK7J4KA1LV', '2WAVGULF395SFX5BDTJ3VYNJJG5PBY', 'yes'),
            ('A224TK7J4KA1LV', '2DMZMAZHHRRLYHIJZ1MRP1KHWR4CLU', 'yes'),
            ('A224TK7J4KA1LV', '27E618N46UXFV4M09Q5TVDSN128RPD', 'yes'),
            ('A224TK7J4KA1LV', '2J9CJK63ZVE30IIF6W1QHJL5ZL59Y2', 'yes'),
            ('A224TK7J4KA1LV', '2DS6X3YOCCF0VGNF93KIVIIX6YURQ4', 'yes'),
            ('A224TK7J4KA1LV', '23ZGYQ4J3NABP2XHRTFY6IT1115PC5', 'yes'),
            ('A224TK7J4KA1LV', '2PFMB3Q39Z0BPLBJI7VE3STVZ26UJK', 'yes'),
            ('A224TK7J4KA1LV', '283FQ0ONNVRHKBZJLS7RJ76N3RBULM', 'no'),
            ('A224TK7J4KA1LV', '2F8S1CSTMOFXA4AZUQSE6DNXRXFORW', 'yes'),
            ('A224TK7J4KA1LV', '21UJ011K274JQ02L8KS8V46U5X5BD9', 'no'),
            ('A224TK7J4KA1LV', '2QAKMT6YTWX40UZX1PVDH9GIE0C0VB', 'yes'),
            ('A224TK7J4KA1LV', '2C18EBDPGFL6E37RBNINLWIO3JLH2M', 'yes'),
            ('A224TK7J4KA1LV', '2Y6VR14IXKO240KCQQNAEX3YWU59AV', 'yes'),
            ('A224TK7J4KA1LV', '2P7JWKUDD8XMUU8YLDRBEUTOEBXMB2', 'yes'),
            ('A224TK7J4KA1LV', '2525UFJ51Y7QXFHAA4J1KSTMWXQ9CX', 'yes'),
            ('A224TK7J4KA1LV', '2NCXFCD45XCECEVNZ7BIV3TGXMQWYF', 'yes'),
            ('A224TK7J4KA1LV', '27ZM8JIA0RYN20KIVYD0DBMJ1C8507', 'yes'),
            ('A224TK7J4KA1LV', '2I63W5XH0JPPB9KFASGL0P75S3FEKP', 'yes'),
            ('A224TK7J4KA1LV', '21RRJ85OZIZE0DS510FOY5EWXFB9XW', 'yes'),
            ('A224TK7J4KA1LV', '2LAMEZZ2MIKM60C31NP3GTWW50TN6F', 'yes'),
            ('A224TK7J4KA1LV', '241KM05BMJTU0PEXS7G9ZA7SDEFEJQ', 'yes'),
            ('A224TK7J4KA1LV', '2UZDM25L8I9NINOCQDXOM4QWFBYHRY', 'yes'),
            ('A224TK7J4KA1LV', '2J1E1M7PKK9LANOJBO30CLZXX3YZSU', 'yes'),
            ('A224TK7J4KA1LV', '2LWGDHDM25L8105U8K8E76OEC8MEO6', 'no'),
            ('A224TK7J4KA1LV', '2XANTL0XULRG6KTEF0DD55FPF5X2OT', 'yes'),
            ('A224TK7J4KA1LV', '2FC98JHSTLB34RX6VN9OJJEJZWORFD', 'yes'),
            ('A224TK7J4KA1LV', '2D2UDD8XMB3QM0HVNKLTW6T4MDIEPN', 'yes'),
            ('A224TK7J4KA1LV', '2C73TVOK5UFJOSG22SFZNYQS9UI743', 'yes'),
            ('A224TK7J4KA1LV', '25XXRDS4IC1EH45SVTD19A2I3GUWZ6', 'no'),
            ('A224TK7J4KA1LV', '2PG1THV8ER9YRK5FU0QSU5KFPAT2PA', 'yes'),
            ('A224TK7J4KA1LV', '2C79746OQ1SN9HPLILR59QKCV9RN39', 'yes'),
            ('A224TK7J4KA1LV', '2YDKCJ011K27NAP4W4N698N4ECQ9BQ', 'yes'),
            ('A224TK7J4KA1LV', '2XGQ4J3NAB6BYDXA0CPI11TJNV6ER,F', 'yes'),
            ('A224TK7J4KA1LV', '23K5L8I9NZW605H10SVQ47T8ER6UKJ', 'yes'),
            ('A224TK7J4KA1LV', '2ZCUU00OQKKAN90NK6TUA680MEQWWG', 'yes'),
            ('A224TK7J4KA1LV', '2P1HSTLB3L0FUARD0PAERREVMNHUI8', 'yes'),
            ('A224TK7J4KA1LV', '2581SNQQ7Q67JWJLWQER92TQKJN9TD', 'yes'),
            ('A224TK7J4KA1LV', '2LISPW1INMHGHHMEF11BEBFMNXHH4I', 'yes'),
            ('A224TK7J4KA1LV', '2SIHFL42J1LYOZT2ELD0QGFKPVRN2Y', 'yes'),
            ('A224TK7J4KA1LV', '2ZRNZW6HEZ6OXV8RJ7Z6HGUMAJRZPE', 'yes'),
            ('A224TK7J4KA1LV', '214T6YTWX4H30T76GR09OI6IR91X2S', 'yes'),
            ('A224TK7J4KA1LV', '2T5HMVHVKCJ0KS2XJIA7HKQWEJ1646', 'yes'),
            ('A224TK7J4KA1LV', '2ALDHJHP4BDD37MTK5JXHX3GBNY4XW', 'yes'),
            ('A224TK7J4KA1LV', '2IDP9746OQ1S6H822KY0D1QKK5I2ME', 'yes'),
            ('A224TK7J4KA1LV', '2WIOHOVR14IX3FKGLG8EKWA65LO76O', 'yes'),
            ('A224TK7J4KA1LV', '2GYKPEIB9BAW4J4S14WV5UD3UBHX08', 'yes'),
            ('A224TK7J4KA1LV', '2WQ06UFBNFSVZL3AFNWS46NG9XLH3X', 'yes'),
            ('A224TK7J4KA1LV', '2L13NAB6BFMFYFGTU7STRFDGMA2UHF', 'yes'),
            ('A224TK7J4KA1LV', '2ALDHJHP4BDD37MTK5JXHX3GBN04XY', 'no'),
            ('A224TK7J4KA1LV', '2F4NCWYB49F9BJAC9FSJWNSTDZYOSK', 'yes'),
            ('A224TK7J4KA1LV', '2BXBNFSVGULFM0NN8KEG9FS3VGE7LX', 'yes'),
            ('A224TK7J4KA1LV', '20JLY58B727MJ9YAWV41EYFS3XXU9S', 'no'),
            ('A224TK7J4KA1LV', '2FKAOO2GMMEG7FYL4QD6QAA20W877N', 'yes'),
            ('A224TK7J4KA1LV', '20JLY58B727MJ9YAWV41EYFS3XU9U4', 'yes'),
            ('A224TK7J4KA1LV', '2A79RA7S5WM1P0GN0TY0RMHLI0JZUA', 'yes'),
            ('A224TK7J4KA1LV', '2AOYTWX4H3H282M8LN7IEIJRJNY4ZV', 'yes'),
            ('A2ZUENR4ZLC3MN', '2K5AB6BFMFFOHP0OD7AFLGESKIHJW8', 'yes')]

        response = self.client.await_completion(self.client.post_assigned_labels(assignedLabels))
        self.assertEqual('OK', response['status'])

        response = self.client.await_completion(self.client.get_estimated_workers_quality())
        self.assertEqual('OK', response['status'])

    def test_GH_88(self):
        """
            Test for github issue https://github.com/ipeirotis/Troia-Server/issues/88
            Thanks to PeccatorImpius for reporting
        """
        categories = ['blank', 'confirm_closed', 'confirm_no', 'confirm_nonrestaurant', 'confirm_yes']
        algorithm = "BDS" # TODO XXX FIXME currently it won't work on IDS
        response = self.client.create(categories,
                                      prioritycalculator="CostBased",
                                      costMatrix=[ {"value":5.0,  "to":"blank", "from":"blank"},
                                                   {"value":5.0, "to":"confirm_closed", "from":"blank"},
                                                   {"value":5.0, "to":"confirm_no", "from":"blank"},
                                                   {"value":5.0, "to":"confirm_nonrestaurant", "from":"blank"},
                                                   {"value":5.0, "to":"confirm_yes", "from":"blank"},
                                                   {"value":5.0, "to":"blank", "from":"confirm_closed"},
                                                   {"value":0.0, "to":"confirm_closed", "from":"confirm_closed"},
                                                   {"value":5.0, "to":"confirm_no", "from":"confirm_closed"},
                                                   {"value":5.0, "to":"confirm_nonrestaurant", "from":"confirm_closed"},
                                                   {"value":5.0, "to":"confirm_yes", "from":"confirm_closed"},
                                                   {"value":1.0, "to":"blank", "from":"confirm_no"},
                                                   {"value":1.0, "to":"confirm_closed", "from":"confirm_no"},
                                                   {"value":0.0, "to":"confirm_no", "from":"confirm_no"},
                                                   {"value":1.0, "to":"confirm_nonrestaurant", "from":"confirm_no"},
                                                   {"value":1.0, "to":"confirm_yes", "from":"confirm_no"},
                                                   {"value":5.0, "to":"blank", "from":"confirm_nonrestaurant"},
                                                   {"value":5.0, "to":"confirm_closed", "from":"confirm_nonrestaurant"},
                                                   {"value":5.0, "to":"confirm_no", "from":"confirm_nonrestaurant"},
                                                   {"value":0.0, "to":"confirm_nonrestaurant", "from":"confirm_nonrestaurant"},
                                                   {"value":5.0, "to":"confirm_yes", "from":"confirm_nonrestaurant"},
                                                   {"value":1.0, "to":"blank", "from":"confirm_yes"},
                                                   {"value":1.0, "to":"confirm_closed", "from":"confirm_yes"},
                                                   {"value":1.0, "to":"confirm_no", "from":"confirm_yes"},
                                                   {"value":1.0, "to":"confirm_nonrestaurant", "from":"confirm_yes"},
                                                   {"value":0.0, "to":"confirm_yes", "from":"confirm_yes"}],
                                      epsilon=0.0001,
                                      iterations=10,
                                      algorithm=algorithm,
                                      scheduler='NormalScheduler')
        self.assertEqual('OK', response['status'])

        assignedLabels = [
                          ('A1R7CJMWXC79UO', '2OVZKPFE4EGD044XHZZIHNZWGWV7HC', 'confirm_yes'),
                          ('A2VRQML8Q3XYP4', '2OVZKPFE4EGD044XHZZIHNZWGWV7HC', 'confirm_yes'),
                          ('A3PRF4IIM2IQN2', '2OVZKPFE4EGD044XHZZIHNZWGWV7HC', 'confirm_yes'),
                          ('A3TXO6RKFIDFUV', '2Z3KH1Q6SVQ80ZQH28XLDOBVMXHL2G', 'confirm_yes'),
                          ('A3PRF4IIM2IQN2', '2Z3KH1Q6SVQ80ZQH28XLDOBVMXHL2G', 'confirm_yes'),
                          ('A31X3JCHS0BPFJ', '2Z3KH1Q6SVQ80ZQH28XLDOBVMXHL2G', 'confirm_yes'),
                          ('A1FQYUBCBNTQX7', '2V6ZFYQS1CST5FXS3RJ4QC1E8S3KN3', 'confirm_yes'),
                          ('A3PRF4IIM2IQN2', '2V6ZFYQS1CST5FXS3RJ4QC1E8S3KN3', 'confirm_yes'),
                          ('A31X3JCHS0BPFJ', '2V6ZFYQS1CST5FXS3RJ4QC1E8S3KN3', 'confirm_yes'),
                          ('A31X3JCHS0BPFJ', '2MCFJ51Y7QEOI6GL4F3S1MOF76TBEL', 'confirm_yes'),
                          ('A3PRF4IIM2IQN2', '2MCFJ51Y7QEOI6GL4F3S1MOF76TBEL', 'confirm_yes'),
                          ('A3TXO6RKFIDFUV', '2MCFJ51Y7QEOI6GL4F3S1MOF76TBEL', 'confirm_yes'),
                          ('A31X3JCHS0BPFJ', '2S4JTUHYW2GT8095J6WWU169874PK4', 'confirm_yes'),
                          ('A3PRF4IIM2IQN2', '2S4JTUHYW2GT8095J6WWU169874PK4', 'confirm_yes'),
                          ('AH5ZIMHL7TNWC', '2S4JTUHYW2GT8095J6WWU169874PK4', 'confirm_no'),
                          ('A3PRF4IIM2IQN2', '2S3YHVI44OS23CC3P15Z0BAPFQI4YO', 'confirm_yes'),
                          ('A31X3JCHS0BPFJ', '2S3YHVI44OS23CC3P15Z0BAPFQI4YO', 'confirm_closed'),
                          ('AH5ZIMHL7TNWC', '2S3YHVI44OS23CC3P15Z0BAPFQI4YO', 'confirm_yes'),
                          ('A31X3JCHS0BPFJ', '2KXDEY5COW0LZIHYKQIFTC6VX9G4VF', 'confirm_yes'),
                          ('A3PRF4IIM2IQN2', '2KXDEY5COW0LZIHYKQIFTC6VX9G4VF', 'confirm_yes'),
                          ('A2KET1HL1COET5', '2KXDEY5COW0LZIHYKQIFTC6VX9G4VF', 'confirm_yes'),
                          ('A31X3JCHS0BPFJ', '2FT49F9SSSHXKS1JZ6K5P5F8TJ4TX2', 'confirm_yes'),
                          ('AH5ZIMHL7TNWC', '2FT49F9SSSHXKS1JZ6K5P5F8TJ4TX2', 'confirm_no'),
                          ('A3TXO6RKFIDFUV', '2FT49F9SSSHXKS1JZ6K5P5F8TJ4TX2', 'confirm_no'),
                          ('A3PRF4IIM2IQN2', '27G2RCJK63ZVXUZMCYLIIQ9JVK87WC', 'confirm_yes'),
                          ('A19BL9GZGXFWFT', '27G2RCJK63ZVXUZMCYLIIQ9JVK87WC', 'confirm_yes'),
                          ('AH5ZIMHL7TNWC', '27G2RCJK63ZVXUZMCYLIIQ9JVK87WC', 'confirm_no'),
                          ('AH5ZIMHL7TNWC', '2JODG67D1X3VJ62VO2B2RE1MH40HAC', 'confirm_no'),
                          ('A31X3JCHS0BPFJ', '2JODG67D1X3VJ62VO2B2RE1MH40HAC', 'confirm_yes'),
                          ('A2VRQML8Q3XYP4', '2JODG67D1X3VJ62VO2B2RE1MH40HAC', 'confirm_yes'),
                          ('A31X3JCHS0BPFJ', '26ZIT3HVWAVK1XKIV4T1F2Z9J5XEMD', 'confirm_closed'),
                          ('A3TXO6RKFIDFUV', '26ZIT3HVWAVK1XKIV4T1F2Z9J5XEMD', 'confirm_closed'),
                          ('AH5ZIMHL7TNWC', '26ZIT3HVWAVK1XKIV4T1F2Z9J5XEMD', 'confirm_nonrestaurant'),
                          ('A3PRF4IIM2IQN2', '20N1Y7QEOZFY9JJ747DONXRD2JYEH4', 'confirm_yes'),
                          ('A31X3JCHS0BPFJ', '20N1Y7QEOZFY9JJ747DONXRD2JYEH4', 'confirm_yes'),
                          ('A2KET1HL1COET5', '20N1Y7QEOZFY9JJ747DONXRD2JYEH4', 'confirm_yes'),
                          ('A3PRF4IIM2IQN2', '241KM05BMJTU0PEXS7G9ZA7SFB2EJ9', 'confirm_yes'),
                          ('A2L2ZXRHK3SNOP', '241KM05BMJTU0PEXS7G9ZA7SFB2EJ9', 'confirm_yes'),
                          ('AH5ZIMHL7TNWC', '241KM05BMJTU0PEXS7G9ZA7SFB2EJ9', 'confirm_no'),
                          ('A3PRF4IIM2IQN2', '2YDWAVKI62NJ9TJ2ED09YH6BU0SRJZ', 'confirm_yes'),
                          ('A19BL9GZGXFWFT', '2YDWAVKI62NJ9TJ2ED09YH6BU0SRJZ', 'confirm_closed'),
                          ('AH5ZIMHL7TNWC', '2YDWAVKI62NJ9TJ2ED09YH6BU0SRJZ', 'confirm_no'),
                          ('A3PRF4IIM2IQN2', '2JV21O3W5XH02G7NUGBYMPLSZMLHB7', 'confirm_yes'),
                          ('A31X3JCHS0BPFJ', '2JV21O3W5XH02G7NUGBYMPLSZMLHB7', 'confirm_yes'),
                          ('A2L2ZXRHK3SNOP', '2JV21O3W5XH02G7NUGBYMPLSZMLHB7', 'confirm_yes'),
                          ('A3PRF4IIM2IQN2', '2JS1QP6AUC26W7O2PFO330FKAR5811', 'confirm_yes'),
                          ('A31X3JCHS0BPFJ', '2JS1QP6AUC26W7O2PFO330FKAR5811', 'confirm_yes'),
                          ('A1I3CXC17NIRWB', '2JS1QP6AUC26W7O2PFO330FKAR5811', 'confirm_yes'),
                          ('A3PRF4IIM2IQN2', '2CIFK0COK2JEKDPKWY0LZW6O9PSRKY', 'confirm_yes'),
                          ('A31X3JCHS0BPFJ', '2CIFK0COK2JEKDPKWY0LZW6O9PSRKY', 'confirm_yes'),
                          ('A2KET1HL1COET5', '2CIFK0COK2JEKDPKWY0LZW6O9PSRKY', 'confirm_yes'),
                          ('A3PRF4IIM2IQN2', '2IJK274J79KQFXJ3ZIXU5FCDEKDHFP', 'confirm_yes'),
                          ('AH5ZIMHL7TNWC', '2IJK274J79KQFXJ3ZIXU5FCDEKDHFP', 'confirm_no'),
                          ('A2L2ZXRHK3SNOP', '2IJK274J79KQFXJ3ZIXU5FCDEKDHFP', 'confirm_yes'),
                          ('A3TXO6RKFIDFUV', '234EGOOGQSCMP9S5E65I2UU0A36EEO', 'confirm_closed'),
                          ('A3PRF4IIM2IQN2', '234EGOOGQSCMP9S5E65I2UU0A36EEO', 'confirm_closed'),
                          ('A31X3JCHS0BPFJ', '234EGOOGQSCMP9S5E65I2UU0A36EEO', 'confirm_closed'),
                          ('A3TXO6RKFIDFUV', '23QJIA0RYNJ9LE1FYEWBUJTURDD27P', 'confirm_yes'),
                          ('A3PRF4IIM2IQN2', '23QJIA0RYNJ9LE1FYEWBUJTURDD27P', 'confirm_yes'),
                          ('A31X3JCHS0BPFJ', '23QJIA0RYNJ9LE1FYEWBUJTURDD27P', 'confirm_yes'),
                          ('AH5ZIMHL7TNWC', '2S5VP3TVOK5UYANWALHEWZFY07I52D', 'confirm_no'),
                          ('A2L2ZXRHK3SNOP', '2S5VP3TVOK5UYANWALHEWZFY07I52D', 'confirm_yes'),
                          ('A3PRF4IIM2IQN2', '2S5VP3TVOK5UYANWALHEWZFY07I52D', 'confirm_yes'),
                          ('A31X3JCHS0BPFJ', '2ETAT2D5NQYNO6LLCX751YMNMBF84E', 'confirm_yes'),
                          ('AH5ZIMHL7TNWC', '2ETAT2D5NQYNO6LLCX751YMNMBF84E', 'confirm_no'),
                          ('A2L2ZXRHK3SNOP', '2ETAT2D5NQYNO6LLCX751YMNMBF84E', 'confirm_yes'),
                          ('A3PRF4IIM2IQN2', '2Z2MN9U8P9Y3RKER9WUS2YIMAY9EVU', 'confirm_yes'),
                          ('AH5ZIMHL7TNWC', '2Z2MN9U8P9Y3RKER9WUS2YIMAY9EVU', 'confirm_no'),
                          ('A1I3CXC17NIRWB', '2Z2MN9U8P9Y3RKER9WUS2YIMAY9EVU', 'confirm_yes'),
                          ('ABT7QTMIYXYO0', '2GXYQS1CSTMOYO984I9C9EYDXCZPM9', 'confirm_yes'),
                          ('A3PRF4IIM2IQN2', '2GXYQS1CSTMOYO984I9C9EYDXCZPM9', 'confirm_yes'),
                          ('AH5ZIMHL7TNWC', '2GXYQS1CSTMOYO984I9C9EYDXCZPM9', 'confirm_no'),
                          ('AH5ZIMHL7TNWC', '2BLK4F0OHOVRKV0SW2TLH2HEMBR23K', 'blank'),
                          ('A3PRF4IIM2IQN2', '2BLK4F0OHOVRKV0SW2TLH2HEMBR23K', 'confirm_yes'),
                          ('A2L2ZXRHK3SNOP', '2BLK4F0OHOVRKV0SW2TLH2HEMBR23K', 'confirm_yes'),
                          ('A3PRF4IIM2IQN2', '2X6OGQSCM6IATTA9U8LU80OQUZQHHN', 'confirm_yes'),
                          ('A2KET1HL1COET5', '2X6OGQSCM6IATTA9U8LU80OQUZQHHN', 'confirm_yes'),
                          ('A31X3JCHS0BPFJ', '2X6OGQSCM6IATTA9U8LU80OQUZQHHN', 'confirm_yes'),
                          ('A31X3JCHS0BPFJ', '29UWY2AOO2GM55YJ0UHSKM6IKPI442', 'confirm_yes'),
                          ('A3PRF4IIM2IQN2', '29UWY2AOO2GM55YJ0UHSKM6IKPI442', 'confirm_yes'),
                          ('AH5ZIMHL7TNWC', '29UWY2AOO2GM55YJ0UHSKM6IKPI442', 'confirm_yes'),
                          ('A31X3JCHS0BPFJ', '2DJVP9746OQ1BE8LJ4X7851QUR3L1Z', 'confirm_yes'),
                          ('ABT7QTMIYXYO0', '2DJVP9746OQ1BE8LJ4X7851QUR3L1Z', 'confirm_yes'),
                          ('A3PRF4IIM2IQN2', '2DJVP9746OQ1BE8LJ4X7851QUR3L1Z', 'confirm_yes'),
                          ('A31X3JCHS0BPFJ', '25XXRDS4IC1EH45SVTD19A2I5DKWZS', 'confirm_yes'),
                          ('A3PRF4IIM2IQN2', '25XXRDS4IC1EH45SVTD19A2I5DKWZS', 'confirm_no'),
                          ('AH5ZIMHL7TNWC', '25XXRDS4IC1EH45SVTD19A2I5DKWZS', 'confirm_no'),
                          ('A2VRQML8Q3XYP4', '2DABRI8IUB2YD0QET6KLJ3L0PQZH56', 'confirm_yes'),
                          ('AH5ZIMHL7TNWC', '2DABRI8IUB2YD0QET6KLJ3L0PQZH56', 'confirm_no'),
                          ('A3PRF4IIM2IQN2', '2DABRI8IUB2YD0QET6KLJ3L0PQZH56', 'confirm_yes'),
                          ('A3PRF4IIM2IQN2', '2TOSK9RJ85OZ1QWCYO1PUOOQFTCU60', 'confirm_yes'),
                          ('AH5ZIMHL7TNWC', '2TOSK9RJ85OZ1QWCYO1PUOOQFTCU60', 'confirm_yes'),
                          ('A2L2ZXRHK3SNOP', '2TOSK9RJ85OZ1QWCYO1PUOOQFTCU60', 'confirm_yes'),
                          ('A3PRF4IIM2IQN2', '2IBHV8ER9Y8T6B0HB6D5SFHSC334RM', 'confirm_yes'),
                          ('ABT7QTMIYXYO0', '2IBHV8ER9Y8T6B0HB6D5SFHSC334RM', 'confirm_yes'),
                          ('AH5ZIMHL7TNWC', '2IBHV8ER9Y8T6B0HB6D5SFHSC334RM', 'confirm_no'),
                          ('A3TXO6RKFIDFUV', '294EZZ2MIKMNSLQKLCU81WWXSI97O0', 'confirm_yes'),
                          ('A19BL9GZGXFWFT', '294EZZ2MIKMNSLQKLCU81WWXSI97O0', 'confirm_yes'),
                          ('A1I3CXC17NIRWB', '294EZZ2MIKMNSLQKLCU81WWXSI97O0', 'confirm_yes'),
                          ('A2VRQML8Q3XYP4', '2AOYTWX4H3H282M8LN7IEIJRLKM4ZF', 'confirm_yes')]

        response = self.client.await_completion(self.client.post_assigned_labels(assignedLabels))
        self.assertEqual('OK', response['status'])
        
        if algorithm == "BDS":
            self.client.await_completion(self.client.post_compute())

        response = self.client.await_completion(self.client.get_estimated_workers_quality())
        self.assertEqual('OK', response['status'])
        for w in response['result']:
            val = float(w['value'])
            self.assertFalse(math.isnan(val))
