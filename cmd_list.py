from utils import (
    swipe_to_right,
    swipe_to_left,
    open_app,
    copy,
    paste,
    screenshot
)


CMD_MAP = {
    'app': lambda app, extra_script='': open_app(app, extra_script),

    'راست': swipe_to_right,
    'برو راست': swipe_to_right,
    'سمت راست': swipe_to_right,
    'برو سمت راست': swipe_to_right,

    'چپ': swipe_to_left,
    'برو چپ': swipe_to_left,
    'سمت چپ': swipe_to_left,
    'برو سمت چپ': swipe_to_left,

    'کپی': copy,

    'جایگذاری': paste,
    'پیس': paste,
    'پیست': paste,

    'شات': screenshot,
    'اسکرین': screenshot,
    'اسکرین شات': screenshot
}

APPS = {
    'فایرفاکس': 'firefox',
    'سرچ': 'firefox',
    'جستجو': 'firefox',
    'جست و جو': 'firefox',
    'آهنگ': 'spotify'
}
