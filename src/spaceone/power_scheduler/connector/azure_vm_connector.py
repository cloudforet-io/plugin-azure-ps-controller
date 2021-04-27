__all__ = ["AzureVMConnector"]

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


class AzureVMConnector(AzureConnector):

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
        self.vm_compute_client = ComputeManagementClient(credential=credential, subscription_id=subscription_id, api_version='2020-12-01')
        self.network_client = NetworkManagementClient(credential=credential, subscription_id=subscription_id)
        self.resource_client = ResourceManagementClient(credential=credential, subscription_id=subscription_id)
        self.subscription_client: SubscriptionClient = SubscriptionClient(credential=credential)

    def start_vms(self, resource_group_name, vm_name):
        try:
            response = self.compute_client.virtual_machines.begin_start(resource_group_name=resource_group_name, vm_name=vm_name)
            _LOGGER.info(f'[AzureComputeConnector] Start vms : {response}')
            return response
        except Exception as e:
            _LOGGER.error(f'[AzureComputeConnector] start_vms error: {e}')
            raise e

    def stop_vms(self, resource_group_name, vm_name):
        try:
            response = self.compute_client.virtual_machines.begin_power_off(resource_group_name=resource_group_name, vm_name=vm_name)
            _LOGGER.info(f'[AzureComputeConnector] Power Off (Stop) vms : {response}')
            return response
        except Exception as e:
            _LOGGER.error(f'[AzureComputeConnector] stop_vms error: {e}')
            raise e

    def deallocate_vms(self, resource_group_name, vm_name):
        try:
            response = self.compute_client.virtual_machines.begin_deallocate(resource_group_name=resource_group_name, vm_name=vm_name)
            _LOGGER.info(f'[AzureComputeConnector] Deallocate vms : {response}')
            return response
        except Exception as e:
            _LOGGER.error(f'[AzureComputeConnector] Deallocate vms error: {e}')
            raise e

    def restart_vms(self, resource_group_name, vm_name):
        try:
            response = self.compute_client.virtual_machines.begin_restart(resource_group_name=resource_group_name, vm_name=vm_name)
            _LOGGER.info(f'[AzureComputeConnector] Restart vms : {response}')
            return response
        except Exception as e:
            _LOGGER.error(f'[AzureComputeConnector] Restart vms error: {e}')
            raise e

        return reboot_res

    def get_selected_vms(self, parameters):
        '''
        :param parameters:
            parameters = [
            {
                'subscription_id' : <>
                'resource_id': <>
                'resource_group_name': <>
                'vm_name' : <>
            }
        ]
        :return:
            results = [
                {
                    'subscription_id' : <>
                    'resource_id': <>
                    'resource_group_name': <>
                    'vm_name' : <>
                    'result': {result}
                }
        '''
        results = []

        for param in parameters:
            print("param in azure_vm_connector")
            print(param)
            resource_group_name = param.get('resource_group_name', '')
            vm_name = param.get('name', '')
            response = self.get_vm(resource_group_name=resource_group_name, vm_name=vm_name)
            param.update({'result': response})
            results.append(param)

        return results

    def get_vm(self, resource_group_name, vm_name):
        try:
            vm_obj = self.vm_compute_client.virtual_machines.get(resource_group_name=resource_group_name, vm_name=vm_name, expand='InstanceView')
        except Exception as e:
            _LOGGER.error(f'[AzureVmConnector] get_vm error: {e}')
            raise e
        return vm_obj

    def generate_query(self, zone, instance_id, **query):
        query.update({
            'project': self.project_id,
            'zone': zone,
            'instance': instance_id
        })
        return query
