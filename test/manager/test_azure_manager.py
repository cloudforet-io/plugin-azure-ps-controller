import os
from unittest.mock import patch
import unittest
import json
from spaceone.core.unittest.result import print_data
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core.service import *
from spaceone.core import config
from spaceone.core import utils
from spaceone.core.transaction import Transaction
from pprint import pprint
from spaceone.power_scheduler.connector.azure_vm_connector import AzureVMConnector
from spaceone.power_scheduler.manager.vm_manager import AzureVmManager
from spaceone.power_scheduler.service import ControllerService
'''

NOTE: Please, Run test case one by one when you run test. 
Test case must run one at a time, due to its running time for each APIs on Azure.

'''


class TestPowerSchedulerService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.power_scheduler')
        config_path = os.environ.get('TEST_CONFIG')
        test_config = utils.load_yaml_from_file(config_path)

        cls.schema = 'azure_client_secret'
        cls.azure_credentials = test_config.get('AZURE_CREDENTIALS', {})
        cls.vm_connector = AzureVMConnector(transaction=Transaction(), config={}, secret_data=cls.azure_credentials)
        # cls.resource_data =
        cls.vm_manager = AzureVmManager(azure_vm_connector=cls.vm_connector)
        super().setUpClass()

    # @classmethod
    # def test_stop_service_compute_vm(self, *args):
    #     # Stop to - Instance Group
    #     secret_data = _get_credentials()
    #     resource_id = 'https://www.googleapis.com/compute/v1/projects/bluese-cloudone-20200113/zones/asia-northeast1-a/instances/sec-server-2'
    #     resource_type = 'inventory.Server?provider=google_cloud&cloud_service_group=ComputeEngine&cloud_service_type=Instance'
    #     resource_data = {}
    #     controller_svc = ControllerService({})
    #     controller_manager = controller_svc.call_manager(resource_type)
    #     response = controller_manager.stop(secret_data, resource_type, resource_id, resource_data)
    #
    #     print_data(response, 'test_stop_instance_group')

    # @classmethod
    # def test_start_service_compute_vm(self, *args):
    #     # Stop to - Instance Group
    #     secret_data = _get_credentials()
    #     resource_id = 'https://www.googleapis.com/compute/v1/projects/bluese-cloudone-20200113/zones/asia-northeast1-a/instances/sec-server-1'
    #     resource_type = 'ComputeEngine&Instance'
    #     resource_data = {}
    #     controller_svc = ControllerService({})
    #     controller_manager = controller_svc.call_manager(resource_type)
    #     response = controller_manager.start(secret_data, resource_type, resource_id, resource_data)
    #
    #     print_data(response, 'test_start_instance_group')

    # @classmethod
    # def test_reboot_manager_compute_vm(self, *args):
    #     # reboot - Instance Group
    #     secret_data = _get_credentials()
    #     resource_id = 'https://www.googleapis.com/compute/v1/projects/bluese-cloudone-20200113/zones/asia-northeast1-a/instances/sec-server-2'
    #     resource_type = 'inventory.Server?provider=google_cloud&cloud_service_group=ComputeEngine&cloud_service_type=Instance'
    #     resource_data = {}
    #     controller_svc = ControllerService({})
    #     controller_manager = controller_svc.call_manager(resource_type)
    #     response = controller_manager.reboot(secret_data, resource_type, resource_id, resource_data)
    #
    #     print(f'response: {response}')
    #
    #     print_data(response, 'test_reboot_manager_compute_vm')
    #
    #
    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_start_manager_vm(self, *args):
        # Start to - VMs
        secret_data = self.azure_credentials
        resource_type = 'VirtualMachine'
        resource_data = {
            'resource_id': '/subscriptions/3ec64e1e-1ce8-4f2c-82a0-a7f6db0899ca/resourceGroups/jiyoon-rg-0401/providers/Microsoft.Compute/virtualMachines/jiyoon-vm-april',
            'cloud_service_group': 'Compute',
            'cloud_service_type': 'VirtualMachine',
            'subscription_id': '3ec64e1e-1ce8-4f2c-82a0-a7f6db0899ca',
            'resource_group_name': 'jiyoon-rg-0401',
            'vm_name': 'jiyoon-vm-april'
        }

        params = {'secret_data': secret_data, 'resource_data': resource_data}

        controller_svc = ControllerService({})
        controller_manager = controller_svc.call_manager(resource_type)
        response = controller_manager.reboot(params)
        pprint(response)
        print_data(response, 'test_start_manager_azure_vm')

    # @classmethod
    # def test_stop_manager_instance_group(self, *args):
    #     # Stop to - Instance Group
    #     secret_data = _get_credentials()
    #     resource_id = 'https://www.googleapis.com/compute/v1/projects/bluese-cloudone-20200113/zones/asia-northeast3-a/instanceGroups/instance-group-magnaged-zonal-mode-on'
    #     resource_type = 'inventory.CloudService?provider=google_cloud&cloud_service_type=ComputeEngine&cloud_service_type=InstanceGroup'
    #     resource_data = {
    #         "instance_group_type": "STATELESS",
    #         "origin_max_size": 5,
    #         "type": "zone",
    #         "recommend_size": 1,
    #         "origin_min_size": 1,
    #         "mode": "ON"
    #     }
    #
    #     controller_svc = ControllerService({})
    #     controller_manager = controller_svc.call_manager(resource_type)
    #     response = controller_manager.stop(secret_data, resource_type, resource_id, resource_data)
    #     pprint(response)
    #     print_data(response, 'test_stop_manager_instance_group')
    #
    #
    # @classmethod
    # def test_start_manager_sql(self, *args):
    #     # Stop to - SQL
    #     secret_data = _get_credentials()
    #     resource_id = 'https://sqladmin.googleapis.com/sql/v1beta4/projects/bluese-cloudone-20200113/instances/on-off-test-for-mysql'
    #     resource_type = 'CloudSQL&Instance'
    #     resource_data = {}
    #
    #     controller_svc = ControllerService({})
    #     controller_manager = controller_svc.call_manager(resource_type)
    #     response = controller_manager.start(secret_data, resource_type, resource_id, resource_data)
    #
    #     print_data(response, 'test_start_manager_sql')
    #
    # @classmethod
    # def test_stop_manager_sql(self, *args):
    #     # Stop to - SQL
    #     secret_data = _get_credentials()
    #     resource_id = 'https://sqladmin.googleapis.com/sql/v1beta4/projects/bluese-cloudone-20200113/instances/on-off-test-for-mysql'
    #     resource_type = 'CloudSQL&Instance'
    #     resource_data = {}
    #
    #     controller_svc = ControllerService({})
    #     controller_manager = controller_svc.call_manager(resource_type)
    #     response = controller_manager.stop(secret_data, resource_type, resource_id, resource_data)
    #
    #     print_data(response, 'test_stop_manager_sql')

if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
