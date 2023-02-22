def test_version_flag(cli_invoke):
    from hitfactorpy_graphql_server import __version__ as expected_version

    result = cli_invoke(["--version"])
    assert result.exit_code == 0
    assert result.stdout.strip() == expected_version
