import argparse
from AZ_Helper import az_cli
from utils import execute_az_command


def parse_arguments():
    description = 'Arguments for creating a new resource group'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--primary-resource-group",
                        help="The name of the resource group in which the primary vnet resides",
                        dest="primary_resource_group",
                        required=True)
    parser.add_argument("--primary-vnet",
                        help="The VNet you wish to create the peering from",
                        dest="primary_vnet",
                        required=True)
    parser.add_argument("--secondary-resource-group",
                        help="The name of the resource group in which the secondary vnet resides",
                        dest="secondary_resource_group",
                        required=True)
    parser.add_argument("--secondary-vnet",
                        help="The VNet you wish to create the peering to",
                        dest="secondary_vnet",
                        required=True)
    parser.add_argument("--subscription",
                        help="The name of the subscription in which to create the resource",
                        dest="subscription",
                        required=True)
    return parser.parse_args()


def get_vnet_resource_id(resource_group, vnet_name):
    get_vnet_resource_id_command = ["network", "vnet", "show", "--resource-group", "{}".format(resource_group),
                                "--name", "{}".format(vnet_name)]
    vnet_resource_id = execute_az_command(command_to_execute=get_vnet_resource_id_command)
    return vnet_resource_id['id']


def check_if_vnet_peering_exists(resource_group, subscription, target_vnet, vnet):
    vnet_peering_list_command = ["network", "vnet", "peering", "list", "--resource-group",  "{}".format(resource_group),
                                 "--vnet-name",  "{}".format(vnet), "--subscription", "{}".format(subscription)]
    vnet_peerings = execute_az_command(command_to_execute=vnet_peering_list_command)
    if vnet_peerings:
        for vnet_peering in vnet_peerings:
            vnet_peering_name = vnet_peering['name']
            if vnet_peering_name == "{}To{}".format(vnet, target_vnet):
                raise Exception("VNet Peering {} already exists".format(vnet_peering_name))
    else:
        print("No VNet Peerings for {} found in {}".format(vnet, resource_group))
    print("The VNet Peering is ready to be created")


def create_vnet_peering(resource_group, subscription, target_vnet, target_vnet_resource_id, vnet):
    vnet_peering_command = ["network", "vnet", "peering", "create", "--name", "{}To{}".format(vnet, target_vnet),
                            "--remote-vnet", "{}".format(target_vnet_resource_id),
                            "--resource-group", "{}".format(resource_group), "--vnet-name", "{}".format(vnet),
                            "--subscription", "{}".format(subscription)]
    execute_az_command(command_to_execute=vnet_peering_command)


if __name__ == '__main__':
    args = parse_arguments()
    primary_resource_group = args.primary_resource_group
    primary_vnet = args.primary_vnet
    secondary_resource_group = args.secondary_resource_group
    secondary_vnet = args.secondary_vnet
    subscription = args.subscription

    # Get primary and secondary vnet resource IDs
    primary_vnet_resource_id = get_vnet_resource_id(resource_group=primary_resource_group, vnet_name=primary_vnet)
    secondary_vnet_resource_id = get_vnet_resource_id(resource_group=secondary_resource_group, vnet_name=secondary_vnet)

    # For both resources, first check if the vnet peering exists
    check_if_vnet_peering_exists(resource_group=primary_resource_group, subscription=subscription,
                                 target_vnet=secondary_vnet, vnet=primary_vnet)
    check_if_vnet_peering_exists(resource_group=secondary_resource_group, subscription=subscription,
                                 target_vnet=primary_vnet, vnet=secondary_vnet)

    # Once confirmed that neither peering exists, create both peerings
    create_vnet_peering(resource_group=primary_resource_group, subscription=subscription, target_vnet=secondary_vnet,
                        target_vnet_resource_id=secondary_vnet_resource_id, vnet=primary_vnet)
    create_vnet_peering(resource_group=secondary_resource_group, subscription=subscription, target_vnet=primary_vnet,
                        target_vnet_resource_id=primary_vnet_resource_id, vnet=secondary_vnet)
