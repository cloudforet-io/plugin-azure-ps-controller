__all__ = ['AzureVmManager']

import logging
# from spaceone.power_scheduler.error.google_cloud import *
from .controller_manager import ControllerManager
from spaceone.power_scheduler.libs.manager import AzureManager
from spaceone.power_scheduler.connector.azure_vm_connector import AzureVMConnector
_LOGGER = logging.getLogger(__name__)


class AzureVmManager(AzureManager):
    connector_name = 'AzureVMConnector'

    def __init__(self, azure_vm_connector=None, **kwargs):
        super().__init__(**kwargs)
        # self.azure_vm_connector: AzureVMConnector

    def start(self, params):
        """
            Start Virtual Machine,
            Args:
                params:
                    - options
                    - schema
                    - secret_data
                    - filter
                    - zones
                    - subscription_info
                    - resource_data

            Response:
        """

        azure_vm_connector: AzureVMConnector = self.locator.get_connector('AzureVMConnector')
        azure_vm_connector.get_connect(params['secret_data'])

        # self.set_connector(params['secret_data'])
        subscription_info = params['subscription_info']
        resource_data = params['resource_data']
        resource_id = resource_data.get('reference', '').get('resource_id', '')
        vm_name = resource_data.get('name', '')
        resource_group_name = resource_data.get('data', '').get('resource_group', '').get('resource_group_name')

        print(f'Compute VM |  Virtual Machine: {vm_name}, proceed to START!!')
        parameters: list = self.get_parameters(subscription_info['subscription_id'], resource_group_name, resource_id, vm_name)

        # Step 1 : Get vm from requested input params
        selected_vms = azure_vm_connector.get_selected_vms(parameters)
        # Step 2 : Start instance by status
        for vm in selected_vms:
            vm.update({
                'result': self.convert_nested_dictionary(self, vm.get('result', {}))
            })
            vm_status = vm.get('statuses', {}).get('code', {})  # Get Vm's Status

            if vm_status != 'PowerState/running':
                res = azure_vm_connector.start_vms(resource_group_name, vm_name)
                _LOGGER.debug(f'[start] instance res: {res}')
                print('start res')
        return {}

    def stop(self,  params):
        """
            Stop Virtual Machine,
            Args:
            params
              - options: list
              - secret_data: dict
              - schema: string
              - resource_data : dict
                  {
                    'data': {
                        'resource_id' : ,
                        'cloud_service_group' : <>,
                        'cloud_service_type' : <>,
                        'subscription_id' : <subscription_id>
                        'resource_group_name' : <rg_name>,
                        'vm_name' : <vm_name>,
                        'subscription_info' :
                            {
                                'subscription_id': subscription_info.subscription_id,
                                'subscription_name': subscription_info.display_name,
                                'tenant_id': subscription_info.tenant_id
                            }
                    }
                  }

        """
        azure_vm_connector: AzureVMConnector = self.locator.get_connector(self.connector_name)
        azure_vm_connector.get_connect(params['secret_data'])
        # self.set_connector(params['secret_data'])

        subscription_info = params['subscription_info']
        resource_data = params['resource_data']

        resource_id = resource_data.get('reference', '').get('resource_id', '')
        vm_name = resource_data.get('name', '')
        resource_group_name = resource_data.get('data', '').get('resource_group', '').get('resource_group_name')

        print(f'Compute VM |  Virtual Machine: {vm_name}, proceed to STOP!!')
        parameters: list = self.get_parameters(subscription_info['subscription_id'], resource_group_name, resource_id,
                                               vm_name)

        # Step 1 : Get instance from requested input params
        selected_vms = azure_vm_connector.get_selected_vms(parameters)

        # Step 2 : Stop instance by status
        for vm in selected_vms:
            vm.update({
                'result': self.convert_nested_dictionary(self, vm.get('result', {}))
            })
            vm_status = vm.get('statuses', {}).get('code', {})  # Get Vm's Status

            if vm_status != 'PowerState/deallocated':
                res = azure_vm_connector.deallocate_vms(resource_group_name, vm_name)
                _LOGGER.debug(f'[stop] instance res: {res}')

        return {}

    def reboot(self, params):
        """
        Restart Server
         : Hard reset the VM does not do a graceful shutdown.
        """
        azure_vm_connector: AzureVMConnector = self.locator.get_connector(self.connector_name)
        # azure_vm_connector.get_connect(params['secret_data'])
        self.set_connector(params['secret_data'])

        subscription_info = params['subscription_info']
        resource_data = params['resource_data']
        resource_id = resource_data.get('resource_id', '')
        vm_name = resource_data.get('vm_name', '')
        resource_group_name = resource_data.get('resource_group_name', '')

        print(f'Compute VM |  Instance: {vm_name}, proceed to REBOOT!!')
        parameters: list = self.get_parameters(subscription_info['subscription_id'], resource_group_name, resource_id, vm_name)

        # Step 1 : Get instance from requested input params
        selected_vms = azure_vm_connector.get_selected_vms(parameters)

        # Step 2 : Start instance by status
        for vm in selected_vms:
            vm.update({
                'result': self.convert_nested_dictionary(self, vm.get('result', {}))
            })
            vm_status = vm.get('statuses', {}).get('code', {})  # Get Vm's Status
            if vm_status == 'PowerState/running':
                res = azure_vm_connector.restart_vms(resource_group_name, vm_name)
                _LOGGER.debug(f'[stop] instance res: {res}')

        return {}


