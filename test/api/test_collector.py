import os
import unittest
import json

from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import utils
from spaceone.tester import TestCase, print_json
from spaceone.tester import TestCase


class TestCollector(TestCase):

    @classmethod
    def setUpClass(cls):
        azure_cred = os.environ.get('AZURE_CRED')
        test_config = utils.load_yaml_from_file(azure_cred)

        cls.schema = 'azure_client_secret'
        cls.azure_credentials = test_config.get('AZURE_CREDENTIALS', {})
        super().setUpClass()

    def test_init(self):
        v_info = self.inventory.Server.init({'options': {}})
        print_json(v_info)

    def test_verify(self):
        options = {
        }
        v_info = self.power_scheduler.Collector.verify({'options': options, 'secret_data': self.azure_credentials})
        print_json(v_info)

    def test_collect(self):
        options = {}
        filter = {}
        print("test_collect")
        '''
        resource_data = {
            'resource_id': '/subscriptions/3ec64e1e-1ce8-4f2c-82a0-a7f6db0899ca/resourceGroups/jiyoon-rg-april-067/providers/Microsoft.Compute/virtualMachineScaleSets/jiyoon-vmss-power-state-test',
            'cloud_service_group': 'Compute',
            'cloud_service_type': 'VmScaleSet',
            'subscription_id': '3ec64e1e-1ce8-4f2c-82a0-a7f6db0899ca',
            'resource_group_name': 'jiyoon-rg-april-067',
            'vm_scale_set_name': 'jiyoon-vmss-power-state-test'
        }
        '''
        resource_data = {
            "cloud_service_group": "Compute",
            "data": {
                "name": "jiyoon-vmss-normal",
                "subscription_id": "3ec64e1e-1ce8-4f2c-82a0-a7f6db0899ca",
                "resource_group":  "jiyoon-rg-may-071",
                "resource_group_id": "/subscriptions/3ec64e1e-1ce8-4f2c-82a0-a7f6db0899ca/resourceGroups/jiyoon-rg-may-071"
            },
            "provider": "azure",
            "reference": {
                "resource_id": "/subscriptions/3ec64e1e-1ce8-4f2c-82a0-a7f6db0899ca/resourceGroups/jiyoon-rg-may-071/providers/Microsoft.Compute/virtualMachineScaleSets/jiyoon-vmss-normal"
            },
            "server_type": "UNKNOWN",
            "region_code": "eastus2",
            "tags": {
            },
            "ip_addresses": [
            ],
            "collection_info": {
                "pinned_keys": [
                ],
                "change_history": [
                ],
                "service_accounts": [
                ],
                "secrets": [
                    "secret-19c714fea41a",
                    "secret-fe25ca834a20"
                ],
                "state": "MANUAL",
                "collectors": [
                ]
            },
            "cloud_service_type": "VmScaleSet",
            "metadata": {
            }
        }

        # resource_stream = self.power_scheduler.Controller.start({'secret_data': self.azure_credentials, 'resource_data': resource_data})
        resource_stream = self.power_scheduler.Controller.stop({'secret_data': self.azure_credentials, 'resource_data': resource_data})

        print(resource_stream)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
