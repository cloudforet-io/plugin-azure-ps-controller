# plugin-azure-cloud-power-controller
![Microsoft Azure Cloud Services](https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/azure-cloud-services.svg)
**Plugin to control ```Start / Deallocate``` state and virtual machine scale sets for Azure Cloud Services; Virtual Machine, Virtual Machine Scale Sets**

Control ```Start / Deallocate``` State and autoscaling policies with reserved schedule from Azure Platform. 


Find us also at [Dockerhub](https://hub.docker.com/repository/docker/spaceone/google-cloud-power-controller)
> Latest stable version : 1.0

Please contact us if you need any further information. (<support@spaceone.dev>)

---
## Contents

* Table of Contents
    * [Authentication Overview](#authentication-overview)
        * [Virtual Machines](#virtual-machines)
        * [Virtual Machine Scale Sets](#Virtual-machine-scale-sets)
     * [Running State Overview](#running-state-overview)
        * [Virtual Machines](#virtual-machines)
            * ['OFF' state Condition](#off-state-condition)
            * [Default Schema](#default-schema)
        * [Virtual Machine Scale Sets](#virtual-machine-scale-sets)
            * ['OFF' state Condition](#off-state-condition)
            * [Default Schema](#default-schema)
       
---

### Authentication Overview
Registered service account on SpaceONE must have certain permissions to proceed action control 
Please, set authentication privilege for followings:


#### Virtual Machines

- ##### [Virtual Machines](https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines)
    - Scopes
        - https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/list
        - https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/poweroff
        - https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/start
        - https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/get
        - https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/deallocate
        
    - Actions
        - Microsoft.Compute/virtualMachines/read	
        - Microsoft.Compute/virtualMachines/write	
        - Microsoft.Compute/virtualMachines/start/action	
        - Microsoft.Compute/virtualMachines/powerOff/action	
        - Microsoft.Compute/virtualMachines/restart/action
        - Microsoft.Compute/virtualMachines/deallocate/action	
        - Microsoft.Compute/virtualMachines/instanceView/read
        - Microsoft.Compute/virtualMachines/extensions/read		
        
- ##### [Virtual Machine Scale Sets](https://docs.microsoft.com/en-us/rest/api/compute/virtualmachinescalesets)
    - Scopes
        - https://docs.microsoft.com/en-us/rest/api/compute/virtualmachinescalesets/list
        - https://docs.microsoft.com/en-us/rest/api/compute/virtualmachinescalesets/deallocate
        - https://docs.microsoft.com/en-us/rest/api/compute/virtualmachinescalesets/poweroff
        - https://docs.microsoft.com/en-us/rest/api/compute/virtualmachinescalesets/start
      
    - Actions
        - Microsoft.Compute/virtualMachineScaleSets/read	
        - Microsoft.Compute/virtualMachineScaleSets/start/action	
        - Microsoft.Compute/virtualMachineScaleSets/powerOff/action
        - Microsoft.Compute/virtualMachineScaleSets/restart/action	
        - Microsoft.Compute/virtualMachineScaleSets/deallocate/action
        - Microsoft.Compute/virtualMachineScaleSets/virtualMachines/read
        - Microsoft.Compute/virtualMachineScaleSets/virtualMachines/start/action
        - Microsoft.Compute/virtualMachineScaleSets/virtualMachines/powerOff/action	
        - Microsoft.Compute/virtualMachineScaleSets/virtualMachines/restart/action	
        - Microsoft.Compute/virtualMachineScaleSets/virtualMachines/deallocate/action				

### Running State Overview     

Plugin for Azure to Check Running status
- Collecting Virtual Machines State
- Collecting Virtual Machine Scale Sets State


#### Virtual Machines
- cloud_service_group: Compute
- cloud_service_type: VirtualMachines
- provider: azure

###### 'OFF' state Condition:
- data.power_state.status = 'STOPPED'
###### Default Schema
~~~
"reference": {
   "external_link":  "https://portal.azure.com/#@.onmicrosoft.com/resource/subscriptions/SUBSCRIPTION_ID/resourceGroups/RESOURCE_GROUP/providers/Microsoft.Compute/virtualMachineScaleSets/RESOURCE_NAME/overview"
   "power_state":{
      "status":"STOPPED"
   }
}
~~~
---
#### Virtual Machine Scale Sets 
- cloud_service_group: Compute
- cloud_service_type: VmScaleSets
- provider: azure
###### 'OFF' state Condition: 
 - data.instances.statuses.code = 'PowerState/deallocated'
###### Default Schema
~~~
"data": {
   "virtual_machine_scale_set_power_state":[
      "profiles": {
         "rules" : {
               "metric_trigger" : <dict>
               "scale_action" : <dict> 
          }
       }
   ],
   "reference":{
      "external_link":"https://portal.azure.com/#@.onmicrosoft.com/resource/subscriptions/SUBSCRIPTION_ID/resourceGroups/RESOURCE_GROUP_NAME/providers/Microsoft.Compute/virtualMachineScaleSets/VM_SCALE_SET_NAME/overview"
   },
   "instance_count": 2,
   "vm_instances":[
        "vm_instance_status_profile" : {
             "statuses" : [
                 {
                    "code" : "PowerState/deallocated"
                 }
             ]
        }
    ],
}
~~~
