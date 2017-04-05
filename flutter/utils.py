class ErrorLogHelper:

    def __init__(self):
        self.name = "ErrorLog"

    @staticmethod
    def log_error(error_message, calling_function):
        try:
            error_log_model = apps.get_model(app_label='dashboard', model_name='ErrorLogModel')
            error_log = error_log_model()
            error_log.error_message = str(error_message)
            error_log.calling_function = str(calling_function) if calling_function is not None else None
            error_log.save()
        except Exception, e:
            print e