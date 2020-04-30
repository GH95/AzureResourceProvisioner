import argparse
from AZ_Helper import az_cli
from utils import execute_az_command


def parse_arguments():
    description = 'Arguments for creating a new resource group'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--primary-resource-group",
                        help="The name of the resource group in which the primary vnet resides (for when the two vnets"
                             "reside in two different resource groups)",
                        dest="primary_resource_group",
                        required=False)
    parser.add_argument("--primary-vnet",
                        help="The VNet you wish to create the peering from",
                        dest="primary_vnet",
                        required=True)
    parser.add_argument("--resource-group",
                        help="The name of the resource group in which both vnets reside (both vnets must exist here)",
                        dest="resource_group",
                        required=False)
    parser.add_argument("--secondary-resource-group",
                        help="The name of the resource group in which the secondary vnet resides (for when the two vnets"
                             "reside in two different resource groups)",
                        dest="secondary_resource_group",
                        required=False)
    parser.add_argument("--secondary-vnet",
                        help="The VNet you wish to create the peering to",
                        dest="secondary_vnet",
                        required=True)
    parser.add_argument("--subscription",
                        help="The name of the subscription in which to create the resource",
                        dest="subscription",
                        required=True)
    parser.add_argument("--vnets-in-same-rg",
                        help="True if vnets exist in same resource groups, false if not",
                        choices=["True", "False"],
                        default="False",
                        dest="vnets_in_same_rg",
                        required=False)
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


def vnet_peering_connector_handler(primary_vnet, primary_vnet_resource_id, resource_group_a, resource_group_b,
                                   secondary_vnet, secondary_vnet_resource_id, subscription):
    # For both resources, first check if the vnet peering exists
    check_if_vnet_peering_exists(resource_group=resource_group_a, subscription=subscription,
                                 target_vnet=secondary_vnet, vnet=primary_vnet)
    check_if_vnet_peering_exists(resource_group=resource_group_b, subscription=subscription,
                                 target_vnet=primary_vnet, vnet=secondary_vnet)

    # Once confirmed that neither peering exists, create both peerings
    create_vnet_peering(resource_group=resource_group_a, subscription=subscription, target_vnet=secondary_vnet,
                        target_vnet_resource_id=secondary_vnet_resource_id, vnet=primary_vnet)
    create_vnet_peering(resource_group=resource_group_b, subscription=subscription, target_vnet=primary_vnet,
                        target_vnet_resource_id=primary_vnet_resource_id, vnet=secondary_vnet)


if __name__ == '__main__':
    args = parse_arguments()
    primary_vnet = args.primary_vnet
    secondary_vnet = args.secondary_vnet
    subscription = args.subscription
    vnets_in_same_rg = args.vnets_in_same_rg
    vnets_in_same_rg_response = False
    if vnets_in_same_rg == "True":
        vnets_in_same_rg_response = True

    if not vnets_in_same_rg_response:
        primary_resource_group = args.primary_resource_group
        if not primary_resource_group:
            raise Exception("Primary group argument must be supplied if vnets are in separate RGs")

        secondary_resource_group = args.secondary_resource_group
        if not secondary_resource_group:
            raise Exception("Secondary group argument must be supplied if vnets are in separate RGs")

        primary_vnet_resource_id = get_vnet_resource_id(resource_group=primary_resource_group, vnet_name=primary_vnet)
        secondary_vnet_resource_id = get_vnet_resource_id(resource_group=secondary_resource_group,
                                                          vnet_name=secondary_vnet)
        vnet_peering_connector_handler(primary_vnet=primary_vnet,
                                       primary_vnet_resource_id=primary_vnet_resource_id,
                                       resource_group_a=primary_resource_group,
                                       resource_group_b=secondary_resource_group,
                                       secondary_vnet=secondary_vnet,
                                       secondary_vnet_resource_id=secondary_vnet_resource_id,
                                       subscription=subscription)
    else:
        try:
            resource_group = args.resource_group
        except AttributeError:
            raise Exception("Resource group argument must be supplied if vnets are in the same RG")
        vnet_peering_connector_handler(primary_vnet=primary_vnet,
                                       primary_vnet_resource_id=primary_vnet,
                                       resource_group_a=resource_group,
                                       resource_group_b=resource_group,
                                       secondary_vnet=secondary_vnet,
                                       secondary_vnet_resource_id=secondary_vnet,
                                       subscription=subscription)
