# AzureResourceProvisioner
This is a Python repository that enables you to provision resources in Azure via the use of the azure-cli pip

## What Resources Can I Provision Using This Repository
At present, this repository allows you to provision Resource Groups and VNets

## Provisioning A New Resource Group
To provision a new resource group, you would need to execute the RG_Provisioner.py script. Note that the following arguments are mandatory:
* --prefix: The prefix to apply to the resource group name
* --resource-name: The name of the resource for which you are creating a resource group
* --subscription: The subscription in which to create the resource group
* --tag: A key/pair value to add to the tags of the resource

(Note that there is also an optional argument for --location , which enables you to specify which location you would like to provision the resource group in. Note that by default, this is set to UK South
