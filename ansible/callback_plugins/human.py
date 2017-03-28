from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.callback import CallbackBase

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class CallbackModule(CallbackBase):

    '''
    This is the default callback interface, which simply prints messages
    to stdout when new callback events are received.
    '''

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'deploy'
    FIELDS = ['cmd', 'command', 'start', 'end', 'delta', 'msg', 'stdout', 'stderr']

    def show(self, task, host, result, caption):
        
	if caption == "OK" and result.get('changed', '') == True:
		buf = "{0} | {1} | {2} | rc={3} >>\n".format(task, host, 'CHANGED', result.get('rc', 'n/a'))
        	buf += result.get('cmd', '') + "\n"
        	buf += result.get('msg', '') + "\n"
        	buf += result.get('stdout', '') + "\n"
	        print(bcolors.WARNING + buf + bcolors.ENDC)
	elif caption == "OK":
		buf = "{0} | {1} | {2} | rc={3} >>\n".format(task, host, caption, result.get('rc', 'n/a'))
        	buf += result.get('cmd', '')
        	buf += result.get('msg', '')
        	buf += result.get('stdout', '')
        	print(bcolors.OKGREEN + buf + bcolors.ENDC + "\n")
	elif caption == "SKIPPED":
                buf = "{0} | {1} | {2} | rc={3} >>\n".format(task, host, caption, result.get('rc', 'n/a'))
                buf += result.get('skip_reason', '')
                print(bcolors.OKBLUE + buf + bcolors.ENDC + "\n")

	else:
		buf = "{0} | {1} | {2} | rc={3} >>\n".format(task, host, caption, result.get('rc', 'n/a'))
		buf += result.get('stdout', '')
                buf += result.get('stderr', '')
		print(bcolors.FAIL + buf + bcolors.ENDC)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.show(result._task, result._host.get_name(), result._result, "FAILED")

    def v2_runner_on_ok(self, result):
        self.show(result._task, result._host.get_name(), result._result, "OK")

    def v2_runner_on_skipped(self, result):
        self.show(result._task, result._host.get_name(), result._result, "SKIPPED")

    def v2_runner_on_unreachable(self, result):
        self.show(result._task, result._host.get_name(), result._result, "UNREACHABLE")
