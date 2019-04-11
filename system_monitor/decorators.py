import logging

from error_reporter import EventReporter
from ufs_tools.short_decorator.ignore_exception import ignore_exc_with_result
import traceback


def report_exception(exception_owner_object=None,
                     notifying_email=None,
                     exception=Exception,
                     recover_email_subject=None,
                     failure_email_subject=None,
                     is_notification_needed=False,
                     exception_result=None,
                     exception_callback=None,
                     ):
    """
    :param exception_owner_object:
    :param notifying_email:
    :param exception:
    :param recover_email_subject:
    :param failure_email_subject:
    :param is_notification_needed:
    :param exception_result:
    :param exception_callback:
    :return:
    """
    # Ref: http://wklken.me/posts/2012/10/27/python-base-decorator.html
    def exc_wrapper(func):
        # print "executing--------------"

        def wrap_with_exc(*args):
            reporter = EventReporter(exception_owner_object, notifying_email)
            try:
                # print "executing!!!!!!!!!!!!!!!!"
                result = func(*args)
                reporter.report_success(recover_email_subject)
                return result
            except exception as e:
                if is_notification_needed:
                    logging.error("ignored the following exception:______________________________________________")
                    traceback.print_exc()
                elif exception_callback:
                    exception_callback(e)
                reporter.report_error(failure_email_subject, e.message + traceback.format_exc())
                return exception_result

        return wrap_with_exc

    return exc_wrapper
