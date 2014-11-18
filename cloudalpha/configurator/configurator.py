from xml.etree import ElementTree
from xml.etree.ElementTree import ParseError
import inspect
from cloudalpha.account import Account
from cloudalpha.manager import Manager


class ConfiguratorError(Exception):
    """This Exception subclass is used by the methods
    of Configurator to raise exceptions.
    """
    pass


class Configurator:
    """This class parses the specified configuration file and
    generates the proper Account and Manager subclass instances.
    """

    _accounts = {}
    _managers = {}

    def __init__(self, filename):
        """Initialize the instance and generate managers and accounts
        by parsing the file corresponding to the given filename, that
        must be a XML file formatted as specified by configurator.xsd.
        """
        try:
            xml_root = ElementTree.parse(filename).getroot()
        except FileNotFoundError:
            raise ConfiguratorError("File not found")
        except ParseError as e:
            raise ConfiguratorError(str(e))
        self._generate(xml_root)

    def _generate(self, xml_root):
        """Generate the accounts and managers specified by the XML file content."""
        children = list(xml_root)
        if children[0].tag == "accounts":
            self._generate_accounts(children[0])
        else:
            raise ConfiguratorError("Invalid configuration file: missing accounts element as the first child of the root")
        if children[1].tag == "managers":
            self._generate_managers(children[1])
        else:
            raise ConfiguratorError("Invalid configuration file: missing managers element as the first child of the root")

    def _generate_accounts(self, xml_accounts):
        """Generate the accounts specified by the XML "accounts" section."""
        for xml_account in xml_accounts:
            unique_id = xml_account.get("uniqueID")
            service = xml_account.get("service")
            xml_parameters = list(xml_account)
            parameters = {}

            if unique_id is None:
                raise ConfiguratorError("Invalid configuration file: missing unique_id attribute of an account element")
            if service is None:
                raise ConfiguratorError("Invalid configuration file: missing service attribute of an account element""")

            unique_id = unique_id.strip()
            service = service.strip()

            if unique_id in self._accounts:
                raise ConfiguratorError("Invalid configuration file: the unique_id `%0s` is not unique" % (unique_id))

            if xml_parameters:
                for xml_parameter in xml_parameters:
                    parameter_name = xml_parameter.get("name")
                    if parameter_name is not None:
                        parameter_name = parameter_name.strip()
                    else:
                        raise ConfiguratorError("Invalid configuration file: missing name attribute of a parameter element")
                    parameters[parameter_name] = xml_parameter.text.strip()

            account_module_name = "cloudalpha.services." + service + ".account"
            try:
                account_module = __import__(account_module_name)
                for component in account_module_name.split(".")[1:]:
                    account_module = getattr(account_module, component)
            except:
                raise ConfiguratorError("Module " + account_module_name + " does not exist")

            account_class_name = None
            account_class = None
            for name, obj in inspect.getmembers(account_module):
                if inspect.getmodule(obj) == account_module and inspect.isclass(obj):
                    account_class_name = name
                    account_class = obj
                    break
            if not account_class:
                raise ConfiguratorError("Module " + account_module_name + " does not contain a class")
            if Account not in inspect.getmro(account_class):
                raise ConfiguratorError("Class " + account_class_name + " is not a subtype of Account")

            constructor_signature = inspect.signature(account_class)
            for parameter in parameters:
                if parameter not in constructor_signature.parameters:
                    raise ConfiguratorError("Initializer of class " + account_class_name + " has no " + parameter + " argument")
            constructor_args = constructor_signature.bind(*[unique_id], **parameters)

            try:
                account = account_class(*constructor_args.args, **constructor_args.kwargs)
            except Exception as e:
                raise ConfiguratorError("Class " + account_class_name + " could not be instantiated : " + str(type(e)) + " " + str(e))

            self._accounts[unique_id] = account

    def _generate_managers(self, xml_managers):
        """Generate the managers specified by XML "managers" section."""
        for xml_manager in xml_managers:
            unique_id = xml_manager.get("uniqueID")
            manager_type = xml_manager.get("type")
            account_name = xml_manager.get("account")
            xml_parameters = list(xml_manager)
            parameters = {}

            if unique_id is None:
                raise ConfiguratorError("Invalid configuration file: missing unique_id attribute of a manager element")
            if manager_type is None:
                raise ConfiguratorError("Invalid configuration file: missing type attribute of a manager element")
            if account_name is None:
                raise ConfiguratorError("Invalid configuration file: missing account attribute of a manager element")

            unique_id = unique_id.strip()
            manager_type = manager_type.strip()
            account_name = account_name.strip()

            if unique_id in self._accounts or unique_id in self._managers:
                raise ConfiguratorError("Invalid configuration file: the unique_id `%0s` is not unique" % (unique_id))
            if account_name not in self._accounts:
                raise ConfiguratorError("Invalid configuration file: there is no account with uniqueID " + account_name)

            if xml_parameters:
                for xml_parameter in xml_parameters:
                    parameter_name = xml_parameter.get("name")
                    if parameter_name is not None:
                        parameter_name = parameter_name.strip()
                    else:
                        raise ConfiguratorError("Invalid configuration file: missing name attribute of a parameter element")
                    parameters[parameter_name] = xml_parameter.text.strip()

            manager_module_name = "cloudalpha.managers." + manager_type + ".manager"
            try:
                manager_module = __import__(manager_module_name)
                for component in manager_module_name.split(".")[1:]:
                    manager_module = getattr(manager_module, component)
            except:
                raise ConfiguratorError("Module " + manager_module_name + " does not exist")

            manager_class_name = None
            manager_class = None
            for name, obj in inspect.getmembers(manager_module):
                if inspect.getmodule(obj) == manager_module and inspect.isclass(obj):
                    manager_class_name = name
                    manager_class = obj
                    break
            if not manager_class:
                raise ConfiguratorError("Module " + manager_module_name + " does not contain a class")
            if Manager not in inspect.getmro(manager_class):
                raise ConfiguratorError("Class " + manager_class_name + " is not a subtype of Manager")

            constructor_signature = inspect.signature(manager_class)
            for parameter in parameters:
                if parameter not in constructor_signature.parameters:
                    raise ConfiguratorError("Initializer of class " + manager_class_name + " has no " + parameter + " argument")
            constructor_args = constructor_signature.bind(*[unique_id, self._accounts[account_name].file_system.get_new_view()], **parameters)

            try:
                manager = manager_class(*constructor_args.args, **constructor_args.kwargs)
            except Exception as e:
                raise ConfiguratorError("Class " + manager_class_name + " could not be instantiated : " + str(type(e)) + " " + str(e))

            self._managers[unique_id] = manager

    def get_accounts(self):
        """Return a list of the generated accounts."""
        return self._accounts.values()

    def get_managers(self):
        """Return a list of the generated managers."""
        return self._managers.values()
