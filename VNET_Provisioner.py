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
    parser.add_argument("--resource-group",
                        help="The resource group in which to create the vnet",
                        dest="resource_group",
                        required=True)
    parser.add_argument("--subnet-range",
                        help="The subnet range to use (e.g. 10.0.0.0/24)",
                        dest="subnet_range",
                        required=True)
    parser.add_argument("--service-endpoint",
                        help="The service endpoint to connect the VNet",
                        dest="service_endpoint",
                        required=False)
    parser.add_argument("--subscription",
                        help="The name of the subscription in which to create the resource",
                        dest="subscription",
                        required=True)
    parser.add_argument("--vnet-name",
                        help="The name of the vnet you wish to create",
                        dest="vnet_name",
                        required=True)
    return parser.parse_args()


def create_vnet(ipv4_range, location, resource_group, service_endpoint, subnet_range, subscription, vnet_name):
    check_if_vnet_exists(vnet_name=vnet_name)
    create_vnet_command = ["network", "vnet", "create", "--name", "{}".format(vnet_name),
                           "--resource-group", "{}".format(resource_group), "--location",
                           "{}".format(location), "--address-prefix", "{}".format(ipv4_range), "--subnet-name",
                           "{}Subnet".format(vnet_name), "--subnet-prefix", "{}".format(subnet_range), "--tags",
                           "Component={}".format(vnet_name), "--subscription", "{}".format(subscription)]
    execute_az_command(command_to_execute=create_vnet_command)
    if service_endpoint:
        connect_vnet_to_service_endpoint(resource_group=resource_group, service_endpoint=service_endpoint,
                                         subscription=subscription, vnet_name=vnet_name)


def check_if_vnet_exists(vnet_name):
    vnet_list_command = ["network", "vnet", "list"]
    vnet_list = execute_az_command(command_to_execute=vnet_list_command)
    if vnet_list:
        for vnet_record in vnet_list:
            vnet_name_record = vnet_record['name']
            if vnet_name_record == "{}".format(vnet_name):
                raise Exception("VNET name {} already exists".format(vnet_name_record))
    else:
        print("No VNets found, continuing...")


def connect_vnet_to_service_endpoint(resource_group, service_endpoint, subscription, vnet_name):
    service_endpoint_connector_command = ["network", "vnet", "subnet", "update", "--resource-group",
                                          "{}".format(resource_group), "--name",
                                          "{}Subnet".format(vnet_name), "--vnet-name",
                                          "{}".format(vnet_name), "--subscription",
                                          "{}".format(subscription), "--service-endpoints",
                                          service_endpoint]
    print(service_endpoint_connector_command)
    execute_az_command(command_to_execute=service_endpoint_connector_command)


if __name__ == '__main__':
    args = parse_arguments()
    ipv4_range = args.ipv4_range
    location = args.location
    resource_group = args.resource_group
    service_endpoint = args.service_endpoint
    subnet_range = args.subnet_range
    subscription = args.subscription
    vnet_name = args.vnet_name
    create_vnet(ipv4_range=ipv4_range, location=location,  service_endpoint=service_endpoint,
                resource_group=resource_group, subnet_range=subnet_range, subscription=subscription,
                vnet_name=vnet_name)
