import argparse
from AZ_Helper import az_cli
from utils import execute_az_command


def parse_arguments():
    description = 'Arguments for creating a new vnet'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--ipv4-range",
                        help="The ipv4 range to use (e.g. 10.0.0.0/16)",
                        dest="ipv4_range",
                        required=True)
    parser.add_argument("--location",
                        help="The location in which to create the vnet (default=uksouth)",
                        dest="location",
                        default="uksouth",
                        required=False)
    parser.add_argument("--prefix",
                        help="The prefix to add to the resource group name",
                        dest="prefix",
                        required=True)
    parser.add_argument("--resource-name",
                        help="The name of the resource you wish to create",
                        dest="resource_name",
                        required=True)
    parser.add_argument("--subnet-range",
                        help="The subnet range to use (e.g. 10.0.0.0/24)",
                        dest="subnet_range",
                        required=True)
    parser.add_argument("--service-endpoints",
                        help="The list of service endpoints to connect the VNet (must be comma separated)",
                        dest="service_endpoints",
                        default="Microsoft.AzureActiveDirectory",
                        type=str,
                        required=False)
    parser.add_argument("--subscription",
                        help="The name of the subscription in which to create the resource",
                        dest="subscription",
                        required=True)
    parser.add_argument("--tag",
                        help="Key/Pair values to add to tags (we require a tag for Component=Resource)",
                        dest="tag",
                        required=True)
    return parser.parse_args()


def check_if_vnet_exists(prefix, resource_name):
    vnet_list_command = ["network", "vnet", "list"]
    vnet_list = execute_az_command(command_to_execute=vnet_list_command)
    if vnet_list:
        for vnet_record in vnet_list:
            vnet_name = vnet_record['name']
            if vnet_name == "{}{}VNet".format(prefix, resource_name):
                raise Exception("VNET name {} already exists".format(vnet_name))
    else:
        print("No VNets found, continuing...")


def connect_vnet_to_service_endpoint(prefix, resource_name, service_endpoints, subscription):
    service_endpoint_connector_command = ["network", "vnet", "subnet", "update", "--resource-group",
                                          "{}{}RG".format(prefix, resource_name), "--name",
                                          "{}{}Subnet".format(prefix, resource_name), "--vnet-name",
                                          "{}{}".format(prefix, resource_name), "--subscription",
                                          "{}".format(subscription)]
    execute_az_command(command_to_execute=service_endpoint_connector_command)


def create_vnet(ipv4_range, location, prefix, resource_name, service_endpoints, subnet_range, subscription, tag):
    check_if_vnet_exists(prefix=prefix, resource_name=resource_name)
    create_vnet_command = ["network", "vnet", "create", "--name", "{}{}".format(prefix, resource_name),
                           "--resource-group", "{}{}RG".format(prefix, resource_name), "--location",
                           "{}".format(location), "--address-prefix", "{}".format(ipv4_range), "--subnet-name",
                           "{}{}Subnet".format(prefix, resource_name), "--subnet-prefix",
                           "{}".format(subnet_range), "--tags", "{}".format(tag), "--subscription",
                           "{}".format(subscription)]
    execute_az_command(command_to_execute=create_vnet_command)


if __name__ == '__main__':
    args = parse_arguments()
    ipv4_range = args.ipv4_range
    location = args.location
    prefix = args.prefix
    resource_name = args.resource_name
    service_endpoints = args.service_endpoints
    subnet_range = args.subnet_range
    subscription = args.subscription
    tag = args.tag
    create_vnet(ipv4_range=ipv4_range, location=location, prefix=prefix, resource_name=resource_name,
                service_endpoints=service_endpoints, subnet_range=subnet_range, subscription=subscription, tag=tag)
