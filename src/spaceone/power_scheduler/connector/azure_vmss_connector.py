__all__ = ["AzureVmScaleSetConnector"]

import logging
from spaceone.core import utils
from spaceone.core.error import *
from spaceone.core import utils
from spaceone.power_scheduler.libs.connector import AzureConnector

import sys
import os
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource import SubscriptionClient
from azure.identity import DefaultAzureCredential

_LOGGER = logging.getLogger(__name__)


class AzureVmScaleSetConnector(AzureConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.set_connect(kwargs.get('secret_data'))

    def get_connect(self, secret_data):
        subscription_id = secret_data['subscription_id']

        os.environ['AZURE_SUBSCRIPTION_ID'] = subscription_id
        os.environ['AZURE_TENANT_ID'] = secret_data['tenant_id']
        os.environ["AZURE_CLIENT_ID"] = secret_data['client_id']
        os.environ["AZURE_CLIENT_SECRET"] = secret_data['client_secret']

        credential = DefaultAzureCredential()

        self.compute_client = ComputeManagementClient(credential=credential, subscription_id=subscription_id)
        self.network_client = NetworkManagementClient(credential=credential, subscription_id=subscription_id)
        self.resource_client = ResourceManagementClient(credential=credential, subscription_id=subscription_id)
        self.subscription_client: SubscriptionClient = SubscriptionClient(credential=credential)

    def start(self, resource_group_name, vm_scale_set_name):
        try:
            response = self.compute_client.virtual_machine_scale_sets.begin_start(resource_group_name=resource_group_name, vm_scale_set_name=vm_scale_set_name)
            _LOGGER.info(f'[AzureVmScaleSetConnector] Start vmss : {response}')
            return response
        except Exception as e:
            _LOGGER.error(f'[AzureVmScaleSetConnector] start_vms error: {e}')
            raise e

    def stop(self, resource_group_name, vm_scale_set_name):
        try:
            response = self.compute_client.virtual_machine_scale_sets.begin_power_off(resource_group_name=resource_group_name, vm_scale_set_name=vm_scale_set_name)
            _LOGGER.info(f'[AzureVmScaleSetConnector] Power Off (Stop) vmss : {response}')
            return response
        except Exception as e:
            _LOGGER.error(f'[AzureVmScaleSetConnector] stop_vmss error: {e}')
            raise e

    def deallocate(self, resource_group_name, vm_scale_set_name):
        try:
            response = self.compute_client.virtual_machine_scale_sets.begin_deallocate(resource_group_name=resource_group_name, vm_scale_set_name=vm_scale_set_name)
            _LOGGER.info(f'[AzureVmScaleSetConnector] Deallocate vms : {response}')
            return response
        except Exception as e:
            _LOGGER.error(f'[AzureVmScaleSetConnector] Deallocate vms error: {e}')
            raise e

    def get_selected_vmss(self, parameters):
        '''
        :param parameters:
            parameters = [
            {
                'subscription_id' : <>
                'resource_id': <>
                'resource_group_name': <>
                'vm_scale_set_name' : <>
            }
        ]
        :return:
            results = [
                {
                    'subscription_id' : <>
                    'resource_id': <>
                    'resource_group_name': <>
                    'vm_scale_set_name' : <>
                    'result': {result}
                }
        '''
        results = []

        for param in parameters:
            response = self.get_vmss(param.get('resource_group_name', ''), param.get('vm_scale_set_name'))
            param.update({'result': response})
            results.append(param)

        return results

    def get_vmss(self, resource_group_name, vm_scale_set_name):
        try:
            vmss_obj = self.compute_client.virtual_machine_scale_sets.get(resource_group_name=resource_group_name, vm_scale_set_name=vm_scale_set_name)

        except Exception as e:
            _LOGGER.error(f'[AzureVmScaleSetConnector] get_vmss error: {e}')
            raise e
        return vmss_obj
