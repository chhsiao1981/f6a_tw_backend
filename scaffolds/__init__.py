# API
from pyramid.scaffolds import PyramidTemplate
import os


def _underscore_to_upper_camel_case(the_str):
    return ''.join([w.capitalize() for w in the_str.split('_')])


class MyTemplate(PyramidTemplate):
    def pre(self, command, output_dir, vars):
        the_args = command.args

        module_name = the_args[1] if len(the_args) >= 2 else ''
        self._setup_module(vars, module_name)

        return PyramidTemplate.pre(self, command, output_dir, vars)

    def _setup_module(self, vars, full_module_name):
        full_module_path = full_module_name.replace('.', os.path.sep)

        module_name = os.path.basename(full_module_path)
        class_name = _underscore_to_upper_camel_case(module_name)

        sub_pkg_dir = os.path.dirname(full_module_path)
        sub_pkg_name = sub_pkg_dir.replace(os.path.sep, '.')

        test_name = '' if not module_name else 'test_' + module_name
        sub_pkg_dir_list = [] if not sub_pkg_dir else sub_pkg_dir.split(os.path.sep)
        test_dir_list = ['test_' + each_pkg for each_pkg in sub_pkg_dir_list]
        test_dir = os.path.sep.join(test_dir_list)

        vars['module_name'] = module_name
        vars['class_name'] = class_name
        vars['sub_pkg_name'] = sub_pkg_name
        vars['sub_pkg_dir'] = sub_pkg_dir
        vars['test_name'] = test_name
        vars['test_dir'] = test_dir


class ModuleProjectTemplate(MyTemplate):
    _template_dir = 'module'
    summary = 'module'


class ClassProjectTemplate(MyTemplate):
    _template_dir = 'class'
    summary = 'class'


class DjangoProjectTemplate(MyTemplate):
    _template_dir = 'django'
    summary = 'starting django project'


class DevStarterProjectTemplate(MyTemplate):
    _template_dir = 'dev_starter'
    summary = 'starting dev project'


class InitStarterProjectTemplate(MyTemplate):
    _template_dir = 'init_starter'
    summary = 'starting project'


class PkgProjectTemplate(MyTemplate):
    _template_dir = 'pkg'
    summary = 'pkg'
