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

When a new resource is provisioned, it will be created within the specified subscription, and be given a name that follows the convention of
`[prefix][resource-name]RG` (e.g. for example if the prefix was `foo` and the resource-name was `bar`, this would create a new resource group
named `FooBarRG`) - it will also be tagged with the key/pair value you provide under the tag argument (e.g. `Component=Bar`)

### Example Usage

`python RG_Provisioner.py --prefix Foo --resource-name Bar --subscription 'My Subscription' --tag Component=Bar`

The above command will create a new resource group under 'My subscription' named `FooBarRG`, and add a tag of `Component=Bar`. This resource group
will be provisioned in the default region (UK South)

To change the location where the resource group is provisioned, simply provide a `--location` argument (e.g. `--location ukwest`) would provision the
resource group in the UK West region

## Provisioning A New VNet
To provision a new VNet, you would need to execute the VNET_Provisioner.py script. Note that the following arguments are mandatory:
* --ipv4-range: The ipv4 range to apply to this VNet (e.g. 10.0.0.0/16)
* --prefix: The prefix to apply to the resource group name
* --resource-name: The name of the resource for which you are creating a VNet
* --subnet-range: The subnet range to use (e.g. 10.0.0.0/24)
* --subscription: The subscription in which to create the VNet
* --tag: A key/pair value to add to the tags of the resource

Note that there are also the following optional arguments that can be provided to the script:
* --location: The location in which to provision the VNet (defaults to UK South)
* --service-endpoints: The list of service endpoints to connect the VNet (must be comma separated, defaults to Microsoft.AzureActiveDirectory)

Also note that this script assumes that the resource group in which to create this VNet follows the convention of `[prefix][resource-name]RG` that
is used in the RG_Provisioner.py script. If this resource group does not exist, the script will fail to provision a VNet.

When a new VNet is provisioned, it will be provisioned under the specified subscription, and be given a name that follows the convention of 
`[prefix][resource-name]VNet` (e.g. for example if the prefix was foo and the resource-name was bar, this would create a new VNet named FooBarVNet) - 
it will also be tagged with the key/pair value you provide under the tag argument (e.g. Component=Bar).

Moreover the IPv4 Address range for the VNet will be equal to the `ipv4-range` you specify, whilst the Subnet range will be equal to the specified `subnet-range`

### Example Usage

`python VNet_Provisioner.py --ipv4-range 10.0.0.0/16 --prefix Foo --resource-name Bar --subnet-range 10.0.0.0/24 --subscription 'My Subscription' --tag Component=Bar`

The above command will create a new VNet under 'My Subscription' named `FooBarVNet`, which will exist in the `FooBarRG` resource group and have a tag of 
`Component=Bar`. This VNet will have an ipv4-range of 10.0.0.0/16 and a subnet range of 10.0.0.0/24. This will also be provisioned in the default region (UK South) and
have a service endpoint configures for Microsoft.AzureActiveDirectory

To change the location where the resource group is provisioned, simply provide a `--location` argument (e.g. `--location ukwest`) would provision the
resource group in the UK West region. To add or change service endpoints for this VNet, simply provide a comma seperated list of the service endpoints that
you wish to connect to