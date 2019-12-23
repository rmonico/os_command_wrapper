import os
import subprocess


class OSCommandWrapper(object):

    def __init__(self, command, switches=[], final_switch='run'):
        self._command_binary = self._get_command_binary(command)
        self._switches = switches
        self._final_switch = final_switch

    @staticmethod
    def _get_command_binary(command):
        p = subprocess.run(
            ['which', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if p.returncode != 0:
            raise OSCommandWrapperException(
                command + ' binary not found in PATH')

        output = p.stdout.decode().split('\n')

        return output[0]

    def __getattribute__(self, attribute_name):
        if attribute_name.startswith('_'):
            return object.__getattribute__(self, attribute_name)

        if OSCommandWrapper._is_switch(self, attribute_name):
            # FIXME: pass explictly the callback when final_switch is called, just a improvement in readability
            return _WrappedCommandArgumentFactory(self, attribute_name)

        def __sub_command_wrapper__(*args, **kwargs):
            if attribute_name == self._final_switch:
                return self._run_binary(*args, **kwargs)
            else:
                command = attribute_name

                args = args[1:]

                return self._run_binary(command, *args, **kwargs)

        return __sub_command_wrapper__

    @staticmethod
    def _is_switch(self, attribute_name):
        return attribute_name in self._switches or attribute_name == self._final_switch

    def _run_binary(self, *args):
        process = subprocess.run(
            [self._command_binary] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return process

    def _argument_builder_done(self, switches):
        command_line = ()

        for switch, values in switches.items():
            # FIXME: When a switch contains a "_" should replace with a "-"
            command_line += '--{}'.format(switch),
            command_line += values

        return self._run_binary(*command_line)


class _WrappedCommandArgumentFactory:
    """
    Internal use only. Class returned when a switch is called.
    """

    def __init__(self, command_wrapper, initial_switch):
        self._command_wrapper = command_wrapper
        self._initial_switch = initial_switch

    def __call__(self, *args):
        # FIXME: when final switch is called first will not call OSCommandWrapper._argument_builder_done
        self._switches = {self._initial_switch: args}

        return self

    def __getattribute__(self, attribute_name):
        if attribute_name.startswith('_'):
            return object.__getattribute__(self, attribute_name)

        def __long_switch_wrapper__(*args):
            self._switches[attribute_name] = args

            if attribute_name == self._command_wrapper._final_switch:
                return self._command_wrapper._argument_builder_done(self._switches)
            else:
                return self

        return __long_switch_wrapper__


class OSCommandWrapperException(Exception):
    pass
