def test_lib_export_version():
    import hitfactorpy_graphql_server

    assert hitfactorpy_graphql_server.__version__


def test_lib_export_module_root():
    import hitfactorpy_graphql_server

    assert hitfactorpy_graphql_server.MODULE_ROOT
