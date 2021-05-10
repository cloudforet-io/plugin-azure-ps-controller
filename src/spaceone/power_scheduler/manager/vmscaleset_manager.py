__all__ = ['AzureVmScaleSetManager']

import logging
from spaceone.power_scheduler.libs.manager import AzureManager
from spaceone.power_scheduler.connector.azure_vmss_connector import AzureVmScaleSetConnector
_LOGGER = logging.getLogger(__name__)


class AzureVmScaleSetManager(AzureManager):
    connector_name = 'AzureVmScaleSetConnector'

    def __init__(self, azure_vm_connector=None, **kwargs):
        super().__init__(**kwargs)
        # self.azure_vm_connector: AzureVmScaleSetConnector

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
        update_info = {}
        data = {}
        '''
        # update info (1)
        update_info = {
          'action': 'update_cloud_service',
            'data': {
                'power_state': {
                    'status': "RUNNING"
                }
            }
        }
        '''

        azure_vmss_connector: AzureVmScaleSetConnector = self.locator.get_connector(self.connector_name)
        azure_vmss_connector.get_connect(params['secret_data'])
        # self.set_connector(params['secret_data'])

        subscription_info = params['subscription_info']
        resource_data = params['resource_data']
        resource_id = resource_data.get('reference', '').get('resource_id')
        vm_scale_set_name = resource_data.get('data', '').get('name', '')
        resource_group_name = resource_data.get('data', '').get('resource_group', '')

        print(f'Compute VM |  Virtual Machine Scale Set: {vm_scale_set_name}, proceed to START!!')
        parameters: list = self.get_parameters(subscription_info['subscription_id'], resource_group_name, resource_id, vm_scale_set_name)

        # Step 1 : Get vm_scale_set from requested input params
        selected_vmss = azure_vmss_connector.get_selected_vmss(parameters)

        # Step 2 : Start instance by status
        for vm_scale_set in selected_vmss:
            vm_scale_set.update({
                'result': self.convert_nested_dictionary(self, vm_scale_set.get('result', {}))
            })

            vm_status = vm_scale_set.get('statuses', {}).get('code', {})  # Get Vmss Status

            if vm_status != 'PowerState/running':
                res = azure_vmss_connector.start(resource_group_name, vm_scale_set_name)
                _LOGGER.debug(f'[start] instance res: {res}')

        update_info = {
            'data': {},
            'action': 'update_cloud_service'
        }
        return update_info

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
                        'name' : <vm_scale_set_name>,
                        'subscription_info' :
                            {
                                'subscription_id': subscription_info.subscription_id,
                                'subscription_name': subscription_info.display_name,
                                'tenant_id': subscription_info.tenant_id
                            }
                    }
                  }

        """
        azure_vm_connector: AzureVmScaleSetConnector = self.locator.get_connector(self.connector_name)
        azure_vm_connector.get_connect(params['secret_data'])
        # self.set_connector(params['secret_data'])

        subscription_info = params['subscription_info']
        resource_data = params['resource_data']
        resource_id = resource_data.get('reference', '').get('resource_id')
        vm_scale_set_name = resource_data.get('data', '').get('name', '')
        resource_group_name = resource_data.get('data', '').get('resource_group', '')
        print(f'Compute VM |  Virtual Machine Scale Set: {vm_scale_set_name}, proceed to STOP!!')
        parameters: list = self.get_parameters(subscription_info['subscription_id'], resource_group_name, resource_id,
                                               vm_scale_set_name)

        # Step 1 : Get instance from requested input params
        selected_vms = azure_vm_connector.get_selected_vmss(parameters)

        # Step 2 : Stop instance by status
        for vm in selected_vms:
            vm.update({
                'result': self.convert_nested_dictionary(self, vm.get('result', {}))
            })
            vm_status = vm.get('statuses', {}).get('code', {})  # Get Vm's Status

            if vm_status != 'PowerState/deallocated':
                res = azure_vm_connector.deallocate(resource_group_name, vm_scale_set_name)
                _LOGGER.debug(f'[deallocate] instance res: {res}')

        update_info = {
            'data': {},
            'action': 'update_cloud_service'
        }

        return update_info

