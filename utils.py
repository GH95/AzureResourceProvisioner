from AZ_Helper import az_cli


def execute_az_command(command_to_execute):
    try:
        response = az_cli(args_str=command_to_execute)
        print(response)
    except Exception as execution_exception:
        raise Exception("Received {} response when executing: {}".format(execution_exception, command_to_execute))
    return response


def update_resource(update_resource_command):
    try:
        update_resource = az_cli(update_resource_command)
    except Exception as update_resource_exception:
        raise Exception


def create_resource_group(location, resource_name, subscription, tag):
    create_resouce_group_command = ["group", "create", "-l", "{}".format(location), "-n",
                                    "PmaMg{}RG".format(resource_name), "--tags", "{}".format(tag),
                                    "--subscription", "{}".format(subscription)]
    try:
        create_rg_response = az_cli(args_str=create_resouce_group_command)
        print(create_rg_response)
    except Exception as create_resource_group_exception:
        raise Exception("Failed to execute command to create resource group: {}".format(create_resource_group_exception))


def create_vnet(ipv4_range, location, resource_name, service_endpoints, subnet_range, subscription, tag):
    create_vnet_command = ["network", "vnet", "create", "--name", "PmaMg{}VNet".format(resource_name),
                            "--resource-group", "PmaMg{}RG".format(resource_name), "--location", "{}".format(location),
                            "--address-prefix", "{}".format(ipv4_range), "--subnet-name",
                            "PmaMg{}VNetSubnet".format(resource_name), "--subnet-prefix", "{}".format(subnet_range),
                            "--tags", "{}".format(tag), "--subscription", "{}".format(subscription)]
    try:
        az_cli(args_str=create_vnet_command)
    except Exception as create_vnet_exception:
        raise Exception("Failed to create vnet: {}".format(create_vnet_exception))


def connect_vnet_to_service_endpoint(resource_name, service_endpoints, subscription):
    service_endpoint_connector_command = ["network", "vnet", "subnet", "update", "--resource-group",
                                          "PmaMg{}RG".format(resource_name), "--name",
                                          "PmaMg{}VNetSubnet".format(resource_name), "--vnet-name",
                                          "PmaMg{}VNet".format(resource_name), "--subscription",
                                          "{}".format(subscription), "--service-endpoints",
                                          "{}".format(service_endpoints)]
    print(service_endpoint_connector_command)
    try:
        az_cli(args_str=service_endpoint_connector_command)
    except Exception as service_endpoint_connector_exception:
        raise Exception("Failed to connect vnet to service endpoint: {}".format(service_endpoint_connector_exception))