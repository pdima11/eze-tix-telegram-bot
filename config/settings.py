import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))


APP_PORT = int(os.environ.get('PORT', 5000))
APP_HOST = os.environ.get(
    key='APP_HOST',
    default='https://define.me/'
)
TELEGRAM_TOKEN = os.environ.get(
    key='TELEGRAM_BOT_TOKEN',
    default='TOKEN'
)
JOB_INTERVAL = 60  # seconds


TRANSPORTERS_CONFIG = {
    '9911.by': {
        'site': '9911.by',
        'url': "https://route.by/local/components/route/user.order/templates/.default/ajax.php",
        'locations': {
            'Rechitsa': 152,
            'Gomel': 20
        },
        'date_format': '%d.%m.%Y'
    }
}


LOCAL_SETTINGS = os.path.join(PROJECT_ROOT, "local_settings.py")
if os.path.exists(LOCAL_SETTINGS):
    with open(LOCAL_SETTINGS) as f:
        local_settings_content = f.read()

    local_settings = {}
    exec(compile(local_settings_content, LOCAL_SETTINGS, "exec"), local_settings)

    for key, value in local_settings.items():
        globals()[key] = value

