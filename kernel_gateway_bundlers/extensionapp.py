# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import errno
import os.path
import sys

from notebook.services.config import ConfigManager
from notebook.nbextensions import (EnableNBExtensionApp,
    DisableNBExtensionApp, flags, aliases)
from traitlets.config.application import catch_config_error
from traitlets.config.application import Application

# Make copies to reuse flags and aliases
INSTALL_FLAGS = {}
INSTALL_FLAGS.update(flags)

INSTALL_ALIASES = {}
INSTALL_ALIASES.update(aliases)
del INSTALL_ALIASES['destination']

def makedirs(path):
    '''
    mkdir -p and ignore existence errors compatible with Py2/3.
    '''
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

class ExtensionActivateApp(EnableNBExtensionApp):
    '''Subclass that activates this particular extension.'''
    name = u'jupyter-kernel-gateway-bundlers-extension-activate'
    description = u'Activate the jupyter_kernel_gateway_bundlers extension'

    flags = {}
    aliases = {}

    examples = """
        jupyter kernel_gateway_bundlers activate
    """

    def _classes_default(self):
        return [ExtensionActivateApp, EnableNBExtensionApp]

    def start(self):
        self.log.info("Activating jupyter_kernel_gateway_bundlers JS notebook extensions")
        cm = ConfigManager(parent=self, config=self.config)
        cm.update('notebook', {
            'jupyter_cms_bundlers': {
                'microservice_dockerfile_download': {
                    'label': 'Microservice Docker bundle (.zip)',
                    'module_name': 'kernel_gateway_bundlers.dockerfile_download',
                    'group': 'download'
                }
            }
        })
        self.log.info("Done.")

class ExtensionDeactivateApp(DisableNBExtensionApp):
    '''Subclass that deactivates this particular extension.'''
    name = u'jupyter-kernel-gateway-bundlers-extension-deactivate'
    description = u'Deactivate the jupyter_kernel_gateway_bundlers extension'

    flags = {}
    aliases = {}

    examples = """
        jupyter kernel_gateway_bundlers deactivate
    """

    def _classes_default(self):
        return [ExtensionDeactivateApp, DisableNBExtensionApp]

    def start(self):
        self.log.info("Deactivating jupyter_kernel_gateway_bundlers notebook extension")
        cm = ConfigManager(parent=self, config=self.config)
        cm.update('notebook', {
            'jupyter_cms_bundlers': {
                'microservice_dockerfile_download' : None
            }
        })
        self.log.info("Done.")

class ExtensionApp(Application):
    '''CLI for extension management.'''
    name = u'jupyter_kernel_gateway_bundlers extension'
    description = u'Utilities for managing the jupyter_kernel_gateway_bundlers extension'
    examples = ""

    subcommands = dict(
        activate=(
            ExtensionActivateApp,
            "Activate the extension."
        ),
        deactivate=(
            ExtensionDeactivateApp,
            "Deactivate the extension."
        )
    )

    def _classes_default(self):
        classes = super(ExtensionApp, self)._classes_default()

        # include all the apps that have configurable options
        for appname, (app, help) in self.subcommands.items():
            if len(app.class_traits(config=True)) > 0:
                classes.append(app)

    @catch_config_error
    def initialize(self, argv=None):
        super(ExtensionApp, self).initialize(argv)

    def start(self):
        # check: is there a subapp given?
        if self.subapp is None:
            self.print_help()
            sys.exit(1)

        # This starts subapps
        super(ExtensionApp, self).start()

def main():
    ExtensionApp.launch_instance()
