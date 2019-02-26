from django.test import TestCase

from system_monitor.cmd_handler_with_alarm_report import CmdHandlerWithAlarmReport


class HandlerClassStub(object):
    def msg_loop(self):
        raise IOError

    def get_task_object_ufs_url(self):
        return "ufs://handler_class_stub"

    def get_subject_for_error(self):
        return "test subject for error"


class CmdHandlerTestClass(CmdHandlerWithAlarmReport):
    handler_class = HandlerClassStub


class MailHandlerExceptionTestCase(TestCase):
    def setUp(self):
        pass

    def test_mail_handler_exception(self):
        t = CmdHandlerTestClass()
        t.msg_loop()
