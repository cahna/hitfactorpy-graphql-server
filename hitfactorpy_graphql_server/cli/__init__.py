import typer

CLI_NAME = "hitfactorpy_graphql_server"


cli = typer.Typer()


def version_callback(value: bool):
    from .. import __version__ as pkg_version

    if value:
        typer.echo(pkg_version)
        raise typer.Exit()


@cli.callback()
def main(
    version: bool = typer.Option(
        None, "--version", callback=version_callback, is_eager=True, help="Show program version and exit"
    ),
):
    pass


@cli.command()
def run(host: str = "127.0.0.1", port: int = 8000):
    """run the app server"""
    import uvicorn

    uvicorn.run("hitfactorpy_graphql_server.app:make_app", factory=True, host=host, port=port)


if __name__ == "__main__":
    cli()
