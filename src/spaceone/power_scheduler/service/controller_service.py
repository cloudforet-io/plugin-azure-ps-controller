import logging

from pprint import pprint
from spaceone.core.service import *
from spaceone.power_scheduler.error.azure import *
from spaceone.power_scheduler.manager import AzureVmManager
from spaceone.power_scheduler.manager import SubscriptionManager

_LOGGER = logging.getLogger(__name__)
SUPPORTED_RESOURCE_TYPE = ['power_scheduler.Server']
FILTER_FORMAT = []

MANAGER_MAP = {
    'VirtualMachine': 'AzureVmManager',
    'VmScaleSet': 'AzureVmScaleSetManager'
}

@authentication_handler
class ControllerService(BaseService):
    def __init__(self, metadata):
        super().__init__(metadata)

    @check_required(['options'])
    def init(self, params):
        print("init controller")
        """ init plugin by options
        """
        capability = {
            'filter_format': FILTER_FORMAT,
            # 'supported_resource_type': SUPPORTED_RESOURCE_TYPE
            'supported_resource_type': [
                'inventory.Server?provider=azure&cloud_service_group=Compute&cloud_service_type=VirtualMachine',
                'inventory.CloudService?provider=azure&cloud_service_group=Compute&cloud_service_type=VmScaleSet'
            ],
            'reference_keys': [
                {
                    'resource_type': 'inventory.Server?provider=azure&cloud_service_group=Compute&cloud_service_type=VirtualMachine',
                    'required_keys': ['reference.resource_id', 'cloud_service_group', 'cloud_service_type', 'data.subscription.subscription_id', 'data.resource_group', 'name']
                },
                {
                    'resource_type': 'inventory.CloudService?provider=azure&cloud_service_group=Compute&cloud_service_type=VmScaleSet',
                    'required_keys': ['reference.resource_id', 'cloud_service_group', 'cloud_service_type',
                                      'data.subscription_id', 'data.resource_group', 'data.name']
                }

            ]
        }
        _LOGGER.debug(f'[init_transaction] name: {params["options"]}')
        return {'metadata': capability}

    @transaction
    @check_required(['options', 'secret_data'])
    @append_query_filter(['schema'])
    def verify(self, params):
        """ verify options capability
        Args:
            params
              - options
              - secret_data
        Raises:
             ERROR_VERIFY_FAILED:
        """
        options = params.get('options', {})
        manager = self.locator.get_manager('CollectorManager')
        secret_data = params.get('secret_data', {})
        active = manager.verify(options, secret_data)

        return {}

    @transaction
    @check_required(['secret_data', 'resource_data'])
    @append_query_filter(['schema'])
    def start(self, params):
        """ verify options capability
        Args:
            params
              - options: list
              - secret_data: dict
              - schema: string
              - resource_data :
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

        Returns:
        """
        params.update({
            'subscription_info': self.get_subscription_info(self, params),
        })

        secret_data = params['secret_data']
        resource_data = params.get('resource_data')

        # self._print_params(secret_data, resource_id, resource_type, resource_data)
        controller_manager = self.call_manager(resource_data.get('cloud_service_type'))  # ex.cloud_service_type: VirtualMachine / manager : AzureVmManager

        info = controller_manager.start(params)

        return info

    @transaction
    @check_required(['secret_data', 'resource_data'])
    @append_query_filter(['schema'])
    def stop(self, params):

        """ verify options capability
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

        Returns:
        """
        params.update({
            'subscription_info': self.get_subscription_info(self, params)
        })
        resource_data = params.get('resource_data', {})

        #self._print_params(secret_data, resource_id, resource_type, resource_data)

        controller_manager = self.call_manager(resource_data.get('cloud_service_type'))  # ex.cloud_service_type: VirtualMachine / AzureVmManager
        info = controller_manager.stop(params)

        return info

    @transaction
    @check_required(['secret_data', 'resource_data'])
    @append_query_filter(['schema'])
    def reboot(self, params):
        """ verify options capability
        Args:
            params
              - options: list
              - secret_data: dict
              - resource_id: string
              - resource_type: string
              - resource_data: dict
              - schema: string

        Returns:
        """
        params.update({
            'subscription_info': self.get_subscription_info(self, params),
        })
        resource_data = params.get('resource_data', {})
        controller_manager = self.call_manager(resource_data.get('cloud_service_type'))  # ex.cloud_service_type: VirtualMachine / AzureVmManager
        info = controller_manager.reboot(params)

        return info

    def call_manager(self, resource_type):
        manager = MANAGER_MAP.get(resource_type)  # ex.AzureVmManager
        print("manager")
        print(manager)
        if not manager:
            raise ERROR_UNKNOWN_RESOURCE_TYPE(resource_type=resource_type)

        return self.locator.get_manager(manager)

    @staticmethod
    def get_subscription_info(self, params):
        subscription_manager: SubscriptionManager = self.locator.get_manager('SubscriptionManager')
        if subscription_manager:
            return subscription_manager.get_subscription_info(params['secret_data'])

