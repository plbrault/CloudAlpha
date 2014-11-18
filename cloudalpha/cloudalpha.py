from configurator.configurator import Configurator, ConfiguratorError

if __name__ == '__main__':
    """Generate the accounts and managers specified in config.xml, and launch them."""
    try:
        configurator = Configurator("config.xml")
        for account in configurator.get_accounts():
            account.authenticate()
        for manager in configurator.get_managers():
            manager.run()
    except ConfiguratorError as e:
        print(e)
