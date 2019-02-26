from django.test import TestCase

from system_monitor.cmd_handler_with_alarm_report import CmdHandlerWithAlarmReport


class HandlerClassBaseStub(object):
    def get_task_object_ufs_url(self):
        return "ufs://handler_class_stub"

    def get_subject_for_error(self):
        return "test subject for error"

    def get_subject_for_success(self):
        return "test subject for success"


class HandlerClassStubEndsNormally(HandlerClassBaseStub):
    def msg_loop(self):
        return


class HandlerClassStubRaisingException(HandlerClassBaseStub):
    def msg_loop(self):
        raise IOError


class NormalCmdHandlerTestClass(CmdHandlerWithAlarmReport):
    handler_class = HandlerClassStubEndsNormally


class CmdHandlerRaisingExceptionTestClass(CmdHandlerWithAlarmReport):
    handler_class = HandlerClassStubRaisingException


# noinspection PyMethodMayBeStatic
class MailHandlerExceptionTestCase(TestCase):
    def setUp(self):
        pass

    def test_exception_handling(self):
        t = CmdHandlerRaisingExceptionTestClass()
        t.msg_loop()

    def test_normal_operation(self):
        t = NormalCmdHandlerTestClass()
        t.msg_loop()
