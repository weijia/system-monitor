from django.test import TestCase
from djangoautoconf.cmd_handler_base.msg_process_cmd_base import DjangoCmdBase
from obj_sys.models_ufs_obj import UfsObj
from system_monitor.decorators import report_exception


class DecoratorTesterForSuccess(DjangoCmdBase):
    obj, is_created = UfsObj.objects.get_or_create(ufs_url="ufs://handler_class_stub")

    @report_exception(exception_owner_object=obj,
                      notifying_email="richardwangwang@gmail.com",
                      exception=Exception,
                      recover_email_subject="Recovered",
                      failure_email_subject="Failed",
                      is_notification_needed=True,
                      exception_result=None,
                      exception_callback=None,
                      )
    def msg_loop(self):
        pass


class DecoratorTesterForFailure(DjangoCmdBase):
    obj, is_created = UfsObj.objects.get_or_create(ufs_url="ufs://handler_class_stub")

    @report_exception(exception_owner_object=obj,
                      notifying_email="richardwangwang@gmail.com",
                      exception=Exception,
                      recover_email_subject="Recovered",
                      failure_email_subject="Failed",
                      is_notification_needed=True,
                      exception_result=None,
                      exception_callback=None,
                      )
    def msg_loop(self):
        raise IOError


# noinspection PyMethodMayBeStatic
class MailHandlerExceptionTestCase(TestCase):
    def setUp(self):
        pass

    def test_exception_handling(self):
        t = DecoratorTesterForFailure()
        t.msg_loop()

    def test_normal_operation(self):
        t = DecoratorTesterForSuccess()
        t.msg_loop()
