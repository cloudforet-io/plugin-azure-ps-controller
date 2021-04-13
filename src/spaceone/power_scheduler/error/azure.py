from spaceone.core.error import *


class ERROR_UNKNOWN_RESOURCE_TYPE(ERROR_BASE):
    _message = 'Unknown resource type (resource_type = {resource_type})'


class ERROR_INVALID_CREDENTIALS(ERROR_INVALID_ARGUMENT):
    _message = 'Azure credentials is invalid.'

class ERROR_REQUIRED_PARAMETERS(ERROR_BASE):
    _message = 'zone is required. (key = {key}}).'

class ERROR_NOT_SUPPORT_RESOURCE_ID(ERROR_INVALID_ARGUMENT):
    _message = 'Resource ID is not supported by Azure Power Scheduler. (resource = {resource_id})'

class ERROR_REQUIRED_PARAMETERS(ERROR_BASE):
    _message = 'resource_id is required. (resource = {resource_type})'

class ERROR_NOT_SUPPERTED_TYPE_INT(ERROR_BASE):
    _message = 'only Int type is acceptable (target = {target})'

class ERROR_NOT_SUPPORT_INSTANCE_GROUP_TYPE(ERROR_INVALID_ARGUMENT):
    _message = 'This is not supported by Azure Power Scheduler. (resource = {resource_type})'

class ERROR_NOT_SUPPORT_RESOURCE(ERROR_INVALID_ARGUMENT):
    _message = 'This Resource is not supported by Azure Power Scheduler. (resource = {resource})'

class ERROR_NOT_SUPPORT_ALIGN(ERROR_INVALID_ARGUMENT):
    _message = 'Aligner is invalid with given Power Schedulaer type (metric_type = {type})'

