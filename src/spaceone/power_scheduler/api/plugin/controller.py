import logging

from spaceone.api.power_scheduler.plugin import controller_pb2, controller_pb2_grpc
from spaceone.core.pygrpc import BaseAPI
from spaceone.core.pygrpc.message_type import *

_LOGGER = logging.getLogger(__name__)


class Controller(BaseAPI, controller_pb2_grpc.ControllerServicer):

    pb2 = controller_pb2
    pb2_grpc = controller_pb2_grpc

    def init(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('ControllerService', metadata) as controller_svc:
            data = controller_svc.init(params)
            return self.locator.get_info('PluginInfo', data)

    def verify(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('ControllerService', metadata) as controller_svc:
            controller_svc.verify(params)
            return self.locator.get_info('EmptyInfo')

    def start(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('ControllerService', metadata) as controller_svc:
            info = controller_svc.start(params)
            return self.locator.get_info('UpdateInfo', info)

    def stop(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('ControllerService', metadata) as controller_svc:
            info = controller_svc.stop(params)
            return self.locator.get_info('UpdateInfo', info)

    def reboot(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('ControllerService', metadata) as controller_svc:
            controller_svc.reboot(params)
            return self.locator.get_info('EmptyInfo')