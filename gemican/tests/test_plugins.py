import os
from contextlib import contextmanager

import gemican.tests.dummy_plugins.normal_plugin.normal_plugin as normal_plugin
from gemican.plugins._utils import (get_namespace_plugins, get_plugin_name,
                                    load_plugins)
from gemican.tests.support import unittest


@contextmanager
def tmp_namespace_path(path):
    '''Context manager for temporarily appending namespace plugin packages

    path: path containing the `gemican` folder

    This modifies the `gemican.__path__` and lets the `gemican.plugins`
    namespace package resolve it from that.
    '''
    # This avoids calls to internal `gemican.plugins.__path__._recalculate()`
    # as it should not be necessary
    import gemican

    old_path = gemican.__path__[:]
    try:
        gemican.__path__.append(os.path.join(path, 'gemican'))
        yield
    finally:
        gemican.__path__ = old_path


class PluginTest(unittest.TestCase):
    _PLUGIN_FOLDER = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'dummy_plugins')
    _NS_PLUGIN_FOLDER = os.path.join(_PLUGIN_FOLDER, 'namespace_plugin')
    _NORMAL_PLUGIN_FOLDER = os.path.join(_PLUGIN_FOLDER, 'normal_plugin')

    def test_namespace_path_modification(self):
        import gemican
        import gemican.plugins
        old_path = gemican.__path__[:]

        # not existing path
        path = os.path.join(self._PLUGIN_FOLDER, 'foo')
        with tmp_namespace_path(path):
            self.assertIn(
                os.path.join(path, 'gemican'),
                gemican.__path__)
            # foo/gemican does not exist, so it won't propagate
            self.assertNotIn(
                os.path.join(path, 'gemican', 'plugins'),
                gemican.plugins.__path__)
        # verify that we restored path back
        self.assertEqual(gemican.__path__, old_path)

        # existing path
        with tmp_namespace_path(self._NS_PLUGIN_FOLDER):
            self.assertIn(
                os.path.join(self._NS_PLUGIN_FOLDER, 'gemican'),
                gemican.__path__)
            # /namespace_plugin/gemican exists, so it should be in
            self.assertIn(
                os.path.join(self._NS_PLUGIN_FOLDER, 'gemican', 'plugins'),
                gemican.plugins.__path__)
        self.assertEqual(gemican.__path__, old_path)

    def test_get_namespace_plugins(self):
        # existing namespace plugins
        existing_ns_plugins = get_namespace_plugins()

        # with plugin
        with tmp_namespace_path(self._NS_PLUGIN_FOLDER):
            ns_plugins = get_namespace_plugins()
            self.assertEqual(len(ns_plugins), len(existing_ns_plugins)+1)
            self.assertIn('gemican.plugins.ns_plugin', ns_plugins)
            self.assertEqual(
                ns_plugins['gemican.plugins.ns_plugin'].NAME,
                'namespace plugin')

        # should be back to existing namespace plugins outside `with`
        ns_plugins = get_namespace_plugins()
        self.assertEqual(ns_plugins, existing_ns_plugins)

    def test_load_plugins(self):
        def get_plugin_names(plugins):
            return {get_plugin_name(p) for p in plugins}

        # existing namespace plugins
        existing_ns_plugins = load_plugins({})

        with tmp_namespace_path(self._NS_PLUGIN_FOLDER):
            # with no `PLUGINS` setting, load namespace plugins
            plugins = load_plugins({})
            self.assertEqual(len(plugins), len(existing_ns_plugins)+1, plugins)
            self.assertEqual(
                {'gemican.plugins.ns_plugin'} | get_plugin_names(existing_ns_plugins),
                get_plugin_names(plugins))

            # disable namespace plugins with `PLUGINS = []`
            SETTINGS = {
                'PLUGINS': []
            }
            plugins = load_plugins(SETTINGS)
            self.assertEqual(len(plugins), 0, plugins)

            # with `PLUGINS`, load only specified plugins

            # normal plugin
            SETTINGS = {
                'PLUGINS': ['normal_plugin'],
                'PLUGIN_PATHS': [self._NORMAL_PLUGIN_FOLDER]
            }
            plugins = load_plugins(SETTINGS)
            self.assertEqual(len(plugins), 1, plugins)
            self.assertEqual(
                {'normal_plugin'},
                get_plugin_names(plugins))

            # normal submodule/subpackage plugins
            SETTINGS = {
                'PLUGINS': [
                    'normal_submodule_plugin.subplugin',
                    'normal_submodule_plugin.subpackage.subpackage',
                ],
                'PLUGIN_PATHS': [self._NORMAL_PLUGIN_FOLDER]
            }
            plugins = load_plugins(SETTINGS)
            self.assertEqual(len(plugins), 2, plugins)
            self.assertEqual(
                {'normal_submodule_plugin.subplugin',
                 'normal_submodule_plugin.subpackage.subpackage'},
                get_plugin_names(plugins))

            # ensure normal plugins are loaded only once
            SETTINGS = {
                'PLUGINS': ['normal_plugin'],
                'PLUGIN_PATHS': [self._NORMAL_PLUGIN_FOLDER],
            }
            plugins = load_plugins(SETTINGS)
            for plugin in load_plugins(SETTINGS):
                # The second load_plugins() should return the same plugin
                # objects as the first one
                self.assertIn(plugin, plugins)

            # namespace plugin short
            SETTINGS = {
                'PLUGINS': ['ns_plugin']
            }
            plugins = load_plugins(SETTINGS)
            self.assertEqual(len(plugins), 1, plugins)
            self.assertEqual(
                {'gemican.plugins.ns_plugin'},
                get_plugin_names(plugins))

            # namespace plugin long
            SETTINGS = {
                'PLUGINS': ['gemican.plugins.ns_plugin']
            }
            plugins = load_plugins(SETTINGS)
            self.assertEqual(len(plugins), 1, plugins)
            self.assertEqual(
                {'gemican.plugins.ns_plugin'},
                get_plugin_names(plugins))

            # normal and namespace plugin
            SETTINGS = {
                'PLUGINS': ['normal_plugin', 'ns_plugin'],
                'PLUGIN_PATHS': [self._NORMAL_PLUGIN_FOLDER]
            }
            plugins = load_plugins(SETTINGS)
            self.assertEqual(len(plugins), 2, plugins)
            self.assertEqual(
                {'normal_plugin', 'gemican.plugins.ns_plugin'},
                get_plugin_names(plugins))

    def test_get_plugin_name(self):
        self.assertEqual(
            get_plugin_name(normal_plugin),
            'gemican.tests.dummy_plugins.normal_plugin.normal_plugin',
        )

        class NoopPlugin:
            def register(self):
                pass

        self.assertEqual(
            get_plugin_name(NoopPlugin),
            'PluginTest.test_get_plugin_name.<locals>.NoopPlugin')
        self.assertEqual(
            get_plugin_name(NoopPlugin()),
            'PluginTest.test_get_plugin_name.<locals>.NoopPlugin')
