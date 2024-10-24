_LANGUAGES = ['English', '繁體中文', '简体中文', '日本語']
_TRANSLATIONS = {
    'English': {
        'clock_in': 'Clock In',
    'fix_time': 'Correct Time',
    'not_clock_in': 'You have not clocked in',
    'clock_in_countdown': 'Clock In Countdown',
    'go_home_clock_in': 'Clock Out',
    'is_time_to_go_home': 'It\'s Time to Clock Out',
    'go_home_time': 'Clock Out Time',
    'today_go_home_time': 'Today\'s Clock Out Time:',
    'fix_go_home_time': 'Correct Clock Out Time',
    'fix_today_go_home_time': 'Correct Today\'s Clock Out Time:',
    'fix_clock_in_time': 'Correct Clock In Time (Format: HH:MM:SS)',
    'confirm': 'Confirm',
    'close': 'Close',
    'close_confirm': 'Are you sure you want to close?',
    'remaining_time': 'Remaining Time:',
    'format_error': 'Format Error',
    },
    '繁體中文': {
        'clock_in': '上班打卡',
        'fix_time': '更正時間',
'not_clock_in':'尚未打卡',
        'clock_in_countdown': '打卡倒數',
        'go_home_clock_in': '下班打卡',
        'is_time_to_go_home': '是時候打下班卡了',
        'go_home_time': '下班時間',
        'today_go_home_time': '今日下班時間:',
        'fix_go_home_time': '更正下班時間',
        'fix_today_go_home_time': '更正今日下班時間:',
        'fix_clock_in_time': '更新打卡時間(格式：HH:MM:SS)',
        'confirm': '確認',
        'close': '關閉',
'close_confirm': '你確定要關閉嗎？',
        'remaining_time': '剩餘時間:',
        'format_error': '格式有誤',
    },
    '简体中文': {
        'clock_in': '上班打卡',
    'fix_time': '更正时间',
    'not_clock_in': '尚未打卡',
    'clock_in_countdown': '打卡倒计时',
    'go_home_clock_in': '下班打卡',
    'is_time_to_go_home': '是时候打下班卡了',
    'go_home_time': '下班时间',
    'today_go_home_time': '今日下班时间:',
    'fix_go_home_time': '更正下班时间',
    'fix_today_go_home_time': '更正今日下班时间:',
    'fix_clock_in_time': '更新打卡时间（格式：HH:MM:SS）',
    'confirm': '确认',
    'close': '关闭',
    'close_confirm': '你确定要关闭吗？',
    'remaining_time': '剩余时间:',
    'format_error': '格式有误',
    },
    '日本語': {
        'clock_in': '出社打刻',
    'fix_time': '時間を修正',
    'not_clock_in': 'まだ打刻していません',
    'clock_in_countdown': '打刻カウントダウン',
    'go_home_clock_in': '退社打刻',
    'is_time_to_go_home': '退社打刻の時間です',
    'go_home_time': '退社時間',
    'today_go_home_time': '今日の退社時間:',
    'fix_go_home_time': '退社時間を修正',
    'fix_today_go_home_time': '今日の退社時間を修正:',
    'fix_clock_in_time': '打刻時間を更新（フォーマット：HH:MM:SS）',
    'confirm': '確認',
    'close': '閉じる',
    'close_confirm': '閉じてもよろしいですか？',
    'remaining_time': '残り時間:',
    'format_error': 'フォーマットエラー',
    }
}

def get_languages():
    return _LANGUAGES

def get_translations(language, key):
    return _TRANSLATIONS[language][key]
