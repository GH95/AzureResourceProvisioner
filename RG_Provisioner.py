import argparse
from utils import execute_az_command


def parse_arguments():
    description = 'Arguments for creating a new resource group'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--location",
                        help="The location in which to create the resource group (default=uksouth)",
                        dest="location",
                        default="uksouth",
                        required=False)
    parser.add_argument("--resource-name",
                        help="The name of the resource you wish to create",
                        dest="resource_name",
                        required=True)
    parser.add_argument("--subscription",
                        help="The name of the subscription in which to create the resource",
                        dest="subscription",
                        required=True)
    return parser.parse_args()


def check_if_resource_group_exists(resource_name):
    check_if_resource_group_exists_command = ["group", "exists", "-n", "{}RG".format(resource_name)]
    resource_group_exists = execute_az_command(command_to_execute=check_if_resource_group_exists_command)

    if resource_group_exists:
        raise Exception("Resource Group {}RG Already Exists, Exiting...".format(resource_name))


def create_resource_group(location, resource_name, subscription):
    check_if_resource_group_exists(resource_name=resource_name)
    create_resouce_group_command = ["group", "create", "-l", "{}".format(location), "-n",
                                    "{}RG".format(resource_name), "--tags", "Component={}".format(resource_name),
                                    "--subscription", "{}".format(subscription)]
    execute_az_command(command_to_execute=create_resouce_group_command)


if __name__ == '__main__':
    args = parse_arguments()
    location = args.location
    resource_name = args.resource_name
    subscription = args.subscription
    create_resource_group(location=location, resource_name=resource_name, subscription=subscription)
