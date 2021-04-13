import logging
from spaceone.core.manager import BaseManager

__all__ = ['ControllerManager']
_LOGGER = logging.getLogger(__name__)


class ControllerManager(BaseManager):
    azure_connector = None
    connector_name = None

    def __init__(self, transaction):
        super().__init__(transaction)

    def verify(self, options, secret_data):
        """
            Check connection
        """
        self.azure_connector = self.locator.get_connector('AzureVMConnector')
        r = self.azure_connector.verify(options, secret_data)
        # ACTIVE/UNKNOWN
        return r

    def set_connector(self, secret_data):
        print("controller manager class")
        if self.azure_connector is None:
            self.azure_connector = self.locator.get_connector(self.connector_name)
            print("after")
            print(self.azure_connector)
            self.azure_connector.get_connect(secret_data)

    def start(self, secret_data, resource_type, resource_id, resource_data):
        pass

    def stop(self, secret_data, resource_type, resource_id, resource_data):
        pass

    def reboot(self, secret_data, resource_type, resource_id, resource_data):
        pass

    @staticmethod
    def _get_parameters(resource_id, region, zone):

        '''
        Multi actions for future use
        '''

        # parameters = []
        # if isinstance(resource_ids, list):
        #     param_ov = {}
        #     for idx, resource_id in enumerate(resource_ids):
        #         param_ov.update({
        #             'resource_id': resource_id,
        #             'region_name': region_names[idx] if isinstance(region_names, list) else region_names,
        #             'zone': zone[idx] if isinstance(zone, list) else zone,
        #         })
        #         parameters.append(param_ov)
        # else:
        #     parameters.append({'resource_id': resource_ids, 'region_name': region_names, 'zone': zone})
        #
        # return parameters

        params = {'resource_id': resource_id, 'region': region}
        if zone is not None:
            params.update({'zone': zone})
        return [params]

    @staticmethod
    def _parsing_self_link(self_link):
        resource_id = self_link[self_link.rfind('/') + 1:]
        parsed = self_link[self_link.find('/zones/') + 7:]
        zone = parsed[:parsed.find('/')]
        return {'zone': zone,
                'region': zone[:-2],
                'resource_id': resource_id}

    @staticmethod
    def _parsing_region_self_link(self_link):
        resource_id = self_link[self_link.rfind('/') + 1:]
        parsed = self_link[self_link.find('/regions/') + 9:]
        region = parsed[:parsed.find('/')]
        return {'region': region, 'resource_id': resource_id}

    @staticmethod
    def _check_valid_self_link(self_link_vo):
        is_invalid = False
        if self_link_vo.get('resource_id') is None:
            is_invalid = True
        if self_link_vo.get('region') is None:
            is_invalid = True
        if self_link_vo.get('zone') is None:
            is_invalid = True
        return is_invalid

    @staticmethod
    def _check_valid_region_self_link(self_link_vo):
        is_invalid = False
        if self_link_vo.get('resource_id') is None:
            is_invalid = True
        if self_link_vo.get('region') is None:
            is_invalid = True
        return is_invalid