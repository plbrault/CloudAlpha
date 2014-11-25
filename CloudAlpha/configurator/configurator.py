# =============================================================================
# Copyright (C) 2014 Pier-Luc Brault and Alex Cline
#
# This file is part of CloudAlpha.
#
# CloudAlpha is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CloudAlpha is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with CloudAlpha.  If not, see <http://www.gnu.org/licenses/>.
#
# http://github.com/plbrault/cloudalpha
# =============================================================================

from xml.etree import ElementTree
from xml.etree.ElementTree import ParseError
import inspect
from cloudalpha.account import Account
from cloudalpha.manager import Manager
from cloudalpha.settings import Settings
from cloudalpha.exceptions import InvalidNameSettingError, ValueParsingSettingError


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
        if children[0].tag == "services":
            if children[0][0].tag == "globalSettings":
                self._parse_service_settings(children[0][0])
            else:
                raise ConfiguratorError("Invalid configuration file: missing globalSettings element as the first child of services")
            if children[0][1].tag == "instances":
                self._generate_accounts(children[0][1])
            else:
                raise ConfiguratorError("Invalid configuration file: missing instances element as the second child of services")
        else:
            raise ConfiguratorError("Invalid configuration file: missing services element as the first child of the root")
        if children[1].tag == "managers":
            if children[1][0].tag == "globalSettings":
                self._parse_manager_settings(children[1][0])
            else:
                raise ConfiguratorError("Invalid configuration file: missing globalSettings element as the first child of managers")
            if children[1][1].tag == "instances":
                self._generate_managers(children[1][1])
            else:
                raise ConfiguratorError("Invalid configuration file: missing instances element as the second child of managers")
        else:
            raise ConfiguratorError("Invalid configuration file: missing managers element as the second child of the root")

    def _parse_service_settings(self, xml_settings):
        for xml_service in xml_settings:
            service_name = xml_service.get("name")
            if not service_name:
                raise ConfiguratorError("Invalid configuration file: missing name attribute of a service element")
            service_name = service_name.strip()

            if len(xml_service) > 0:
                settings_module_name = "cloudalpha.services." + service_name + ".settings"
                try:
                    settings_module = __import__(settings_module_name)
                    for component in settings_module_name.split(".")[1:]:
                        settings_module = getattr(settings_module, component)
                except Exception as e:
                    raise ConfiguratorError("Module " + settings_module_name + " could not be imported - " + str(e))

                settings_class = None
                for name, obj in inspect.getmembers(settings_module):
                    if inspect.getmodule(obj) == settings_module and inspect.isclass(obj) and issubclass(obj, Settings):
                        settings_class = obj
                        break
                if not settings_class:
                    raise ConfiguratorError("Module " + settings_module_name + " does not contain a class of subtype Settings")

                for xml_setting in xml_service:
                    setting_name = xml_setting.get("name")
                    if not setting_name:
                        raise ConfiguratorError("Invalid configuration file: missing name attribute of a setting element")
                    setting_name = setting_name.strip()

                    try:
                        settings_class.set(setting_name, xml_setting.text.strip())
                    except InvalidNameSettingError:
                        raise ConfiguratorError("The service " + service_name + " has no setting named " + setting_name)
                    except ValueParsingSettingError:
                        raise ConfiguratorError("The value of setting " + setting_name + " is invalid")

    def _parse_manager_settings(self, xml_settings):
        for xml_manager in xml_settings:
            manager_name = xml_manager.get("name")
            if not manager_name:
                raise ConfiguratorError("Invalid configuration file: missing name attribute of a manager element")
            manager_name = manager_name.strip()

            if len(xml_manager) > 0:
                settings_module_name = "cloudalpha.managers." + manager_name + ".settings"
                try:
                    settings_module = __import__(settings_module_name)
                    for component in settings_module_name.split(".")[1:]:
                        settings_module = getattr(settings_module, component)
                except Exception as e:
                    raise ConfiguratorError("Module " + settings_module_name + " could not be imported - " + str(e))

                settings_class = None
                for name, obj in inspect.getmembers(settings_module):
                    if inspect.getmodule(obj) == settings_module and inspect.isclass(obj) and issubclass(obj, Settings):
                        settings_class = obj
                        break
                if not settings_class:
                    raise ConfiguratorError("Module " + settings_module_name + " does not contain a class of subtype Settings")

                for xml_setting in xml_manager:
                    setting_name = xml_setting.get("name")
                    if not setting_name:
                        raise ConfiguratorError("Invalid configuration file: missing name attribute of a setting element")
                    setting_name = setting_name.strip()

                    try:
                        settings_class.set(setting_name, xml_setting.text.strip())
                    except InvalidNameSettingError:
                        raise ConfiguratorError("The manager " + manager_name + " has no setting named " + setting_name)
                    except ValueParsingSettingError:
                        raise ConfiguratorError("The value of setting " + setting_name + " is invalid")

    def _generate_accounts(self, xml_accounts):
        """Generate the accounts specified by the XML "instances" section."""
        for xml_account in xml_accounts:
            unique_id = xml_account.get("uniqueID")
            service = xml_account.get("service")
            xml_parameters = list(xml_account)
            parameters = {}

            if unique_id is None:
                raise ConfiguratorError("Invalid configuration file: missing unique_id attribute of an accountInstance element")
            if service is None:
                raise ConfiguratorError("Invalid configuration file: missing service attribute of an accountInstance element""")

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
            except Exception as e:
                raise ConfiguratorError("Module " + account_module_name + " could not be imported - " + str(e))

            account_class_name = None
            account_class = None
            for name, obj in inspect.getmembers(account_module):
                if inspect.getmodule(obj) == account_module and inspect.isclass(obj) and issubclass(obj, Account):
                    account_class_name = name
                    account_class = obj
                    break
            if not account_class:
                raise ConfiguratorError("Module " + account_module_name + " does not contain a class of subtype Account")

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
        """Generate the managers specified by XML "instances" section."""
        for xml_manager in xml_managers:
            unique_id = xml_manager.get("uniqueID")
            manager_type = xml_manager.get("type")
            account_name = xml_manager.get("account")
            xml_parameters = list(xml_manager)
            parameters = {}

            if unique_id is None:
                raise ConfiguratorError("Invalid configuration file: missing unique_id attribute of a managerInstance element")
            if manager_type is None:
                raise ConfiguratorError("Invalid configuration file: missing type attribute of a managerInstance element")
            if account_name is None:
                raise ConfiguratorError("Invalid configuration file: missing account attribute of a managerInstance element")

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
            except Exception as e:

                raise ConfiguratorError("Module " + manager_module_name + " could not be imported - " + str(e))

            manager_class_name = None
            manager_class = None
            for name, obj in inspect.getmembers(manager_module):
                if inspect.getmodule(obj) == manager_module and inspect.isclass(obj) and issubclass(obj, Manager):
                    manager_class_name = name
                    manager_class = obj
                    break
            if not manager_class:
                raise ConfiguratorError("Module " + manager_module_name + " does not contain a class of subtype Manager")

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
