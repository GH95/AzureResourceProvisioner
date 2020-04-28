from azure.cli.core import get_default_cli


def az_cli(args_str):
    cli = get_default_cli()
    cli.invoke(args_str)
    if cli.result.result:
        return cli.result.result
    elif cli.result.error:
        return cli.result.error