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
        resource_data = {
            'resource_id': '/subscriptions/3ec64e1e-1ce8-4f2c-82a0-a7f6db0899ca/resourceGroups/jiyoon-rg-april-067/providers/Microsoft.Compute/virtualMachineScaleSets/jiyoon-vmss-always-stopped',
            'cloud_service_group': 'Compute',
            'cloud_service_type': 'VmScaleSet',
            'subscription_id': '3ec64e1e-1ce8-4f2c-82a0-a7f6db0899ca',
            'resource_group_name': 'jiyoon-rg-april-067',
            'vm_scale_set_name': 'jiyoon-vmss-always-stopped'
        }
        resource_stream = self.power_scheduler.Controller.start({'secret_data': self.azure_credentials, 'resource_data': resource_data})
        # resource_stream = self.power_scheduler.Controller.stop({'secret_data': self.azure_credentials, 'resource_data': resource_data})

        print("resource_stream")
        print(resource_stream)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
