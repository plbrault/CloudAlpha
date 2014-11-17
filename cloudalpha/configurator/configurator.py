from xml.etree import ElementTree
from xml.etree.ElementTree import ParseError
import inspect
from cloudalpha.account import Account
from cloudalpha.manager import Manager


class ConfiguratorError(Exception):
    pass


class Configurator:

    _accounts = {}
    _managers = {}

    def __init__(self, filename):
        try:
            xml_root = ElementTree.parse(filename).getroot()
        except FileNotFoundError:
            raise ConfiguratorError("File not found")
        except ParseError as e:
            raise ConfiguratorError(str(e))
        self._generate(xml_root)

    def _generate(self, xml_root):
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
        for xml_account in xml_accounts:
            unique_id = xml_account.get("uniqueID")
            service = xml_account.get("service")
            xml_parameters = list(xml_account)
            parameters = {}

            if unique_id is None:
                raise ConfiguratorError("Invalid configuration file: missing unique_id attribute of an account element")
            if unique_id in self._accounts:
                raise ConfiguratorError("Invalid configuration file: the unique_id `%0s` is not unique" % (unique_id))
            if service is None:
                raise ConfiguratorError("Invalid configuration file: missing service attribute of an account element""")

            unique_id = unique_id.strip()
            service = service.strip()

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

            account = account_class(*constructor_args.args, **constructor_args.kwargs)
            self._accounts[unique_id] = account

    def _generate_managers(self, xml_managers):
        pass

    def get_accounts(self):
        return self._accounts.values()

    def get_managers(self):
        return self._managers.values()
