from django.test import TestCase
from djangoautoconf.cmd_handler_base.msg_process_cmd_base import DjangoCmdBase
from obj_sys.models_ufs_obj import UfsObj
from system_monitor.decorators import report_exception


class ExceptionResult(object):
    def __init__(self, result_value):
        super(ExceptionResult, self).__init__()
        self.result_value = result_value


SUCCESS_VALUE_IN_EXCEPTION_HANDLER = 1
SUCCESS_RETURN_VALUE = 2
FAILURE_VALUE_IN_EXCEPTION_HANDLER = 0
FAILRE_RETURN_VALUE = 3


class DecoratorTesterForSuccess(DjangoCmdBase):
    obj, is_created = UfsObj.objects.get_or_create(ufs_url="ufs://handler_class_stub")

    @report_exception(exception_owner_object=obj,
                      notifying_email="richardwangwang@gmail.com",
                      exception=Exception,
                      recover_email_subject="Recovered",
                      failure_email_subject="Failed",
                      is_notification_needed=True,
                      exception_result=ExceptionResult(SUCCESS_VALUE_IN_EXCEPTION_HANDLER),
                      exception_callback=None,
                      )
    def msg_loop(self):
        return ExceptionResult(SUCCESS_RETURN_VALUE)


class DecoratorTesterForFailure(DjangoCmdBase):
    obj, is_created = UfsObj.objects.get_or_create(ufs_url="ufs://handler_class_stub")

    @report_exception(exception_owner_object=obj,
                      notifying_email="richardwangwang@gmail.com",
                      exception=Exception,
                      recover_email_subject="Recovered",
                      failure_email_subject="Failed",
                      is_notification_needed=True,
                      exception_result=ExceptionResult(FAILURE_VALUE_IN_EXCEPTION_HANDLER),
                      exception_callback=None,
                      )
    def msg_loop(self):
        raise IOError
        return FAILRE_RETURN_VALUE


# noinspection PyMethodMayBeStatic
class MailHandlerExceptionTestCase(TestCase):
    def setUp(self):
        pass

    def test_exception_handling(self):
        t = DecoratorTesterForFailure()
        r = t.msg_loop()
        assert r.result_value == FAILURE_VALUE_IN_EXCEPTION_HANDLER

    def test_normal_operation(self):
        t = DecoratorTesterForSuccess()
        r = t.msg_loop()
        assert r.result_value == SUCCESS_RETURN_VALUE
