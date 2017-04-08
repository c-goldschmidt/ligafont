from PyQt5.QtCore import QSettings


def reload_settings():
    global settings
    if settings:
        del settings

    settings = QSettings('settings.ini', QSettings.IniFormat)
    settings.setFallbacksEnabled(False)


def set_setting(key, value):
    settings.setValue(key, value)
    reload_settings()


def get_setting(key, default_value=None, s_type=None):
    if not s_type:
        s_type = str

    val = settings.value(key, default_value, type=s_type)
    return val

settings = None
reload_settings()
