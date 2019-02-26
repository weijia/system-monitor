import traceback

from djangoautoconf.cmd_handler_base.msg_process_cmd_base import DjangoCmdBase
from obj_sys.models_ufs_obj import UfsObj
from system_monitor.error_reporter import EventReporter


class CmdHandlerWithAlarmReport(DjangoCmdBase):
    handler_class = None
    notifying_mail = ""

    def msg_loop(self):
        handler = self.handler_class()
        task_object, is_created = UfsObj.objects.get_or_create(ufs_url=handler.get_task_object_ufs_url())
        event_reporter = EventReporter(task_object,
                                       self.notifying_mail)
        try:
            handler.msg_loop()
            event_reporter.report_success(handler.get_subject_for_success())
        except Exception as e:
            traceback.print_exc()
            event_reporter.report_error(handler.get_subject_for_error(),
                                        e.message + traceback.format_exc())


