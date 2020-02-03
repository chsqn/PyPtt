import re
try:
    from . import data_type
    from . import lib_util
    from . import i18n
    from . import ConnectCore
    from . import log
    from . import screens
    from . import exceptions
    from . import Command
except ModuleNotFoundError:
    import data_type
    import lib_util
    import i18n
    import ConnectCore
    import log
    import screens
    import exceptions
    import Command


def get_user(api, pttid) -> data_type.UserInfo:

    cmd_list = []
    cmd_list.append(Command.GoMainMenu)
    cmd_list.append('T')
    cmd_list.append(Command.Enter)
    cmd_list.append('Q')
    cmd_list.append(Command.Enter)
    cmd_list.append(pttid)
    cmd_list.append(Command.Enter)

    cmd = ''.join(cmd_list)

    target_list = [
        ConnectCore.TargetUnit(
            [
                i18n.GetUser,
                i18n.Success,
            ],
            screens.Target.AnyKey,
            break_detect=True,
        ),
        ConnectCore.TargetUnit(
            [
                i18n.GetUser,
                i18n.Fail,
            ],
            screens.Target.InTalk,
            break_detect=True,
        ),
    ]

    index = api.connect_core.send(
        cmd,
        target_list
    )
    ori_screen = api.connect_core.get_screen_queue()[-1]
    log.show_value(
        api.config,
        log.Level.DEBUG,
        'OriScreen',
        ori_screen
    )
    if index == 1:
        raise exceptions.NoSuchUser(pttid)
    # PTT1
    # 《ＩＤ暱稱》CodingMan (專業程式 BUG 製造機)《經濟狀況》小康 ($73866)
    # 《登入次數》1118 次 (同天內只計一次) 《有效文章》15 篇 (退:0)
    # 《目前動態》閱讀文章     《私人信箱》最近無新信件
    # 《上次上站》10/06/2019 17:29:49 Sun  《上次故鄉》111.251.231.184
    # 《 五子棋 》 0 勝  0 敗  0 和 《象棋戰績》 0 勝  0 敗  0 和

    # https://github.com/Truth0906/PTTLibrary

    # 強大的 PTT 函式庫
    # 提供您 快速 穩定 完整 的 PTT API

    # 提供專業的 PTT 機器人諮詢服務

    # PTT2
    # 《ＩＤ暱稱》CodingMan (專業程式 BUG 製造機)《經濟狀況》家徒四壁 ($0)
    # 《登入次數》8 次 (同天內只計一次)  《有效文章》0 篇
    # 《目前動態》看板列表     《私人信箱》最近無新信件
    # 《上次上站》10/06/2019 17:27:55 Sun  《上次故鄉》111.251.231.184
    # 《 五子棋 》 0 勝  0 敗  0 和 《象棋戰績》 0 勝  0 敗  0 和

    # 《個人名片》CodingMan 目前沒有名片

    data = lib_util.get_sub_string_list(ori_screen, '》', ['《', '\n'])
    if len(data) < 10:
        print('\n'.join(data))
        print(len(data))
        raise exceptions.ParseError(ori_screen)

    pttid = data[0]
    money = data[1]
    login_time = data[2]
    login_time = login_time[:login_time.find(' ')]
    login_time = int(login_time)

    temp = re.findall(r'\d+', data[3])
    legal_post = int(temp[0])

    # PTT2 沒有退文
    if api.config.host == data_type.host.PTT1:
        illegal_post = int(temp[1])
    else:
        illegal_post = -1

    state = data[4]
    mail = data[5]
    last_login = data[6]
    last_ip = data[7]
    five_chess = data[8]
    chess = data[9]

    signature_file = '\n'.join(ori_screen.split('\n')[6:-1])

    log.show_value(api.config, log.Level.DEBUG, 'pttid', pttid)
    log.show_value(api.config, log.Level.DEBUG, 'money', money)
    log.show_value(api.config, log.Level.DEBUG, 'login_time', login_time)
    log.show_value(api.config, log.Level.DEBUG, 'legal_post', legal_post)
    log.show_value(api.config, log.Level.DEBUG, 'illegal_post', illegal_post)
    log.show_value(api.config, log.Level.DEBUG, 'state', state)
    log.show_value(api.config, log.Level.DEBUG, 'mail', mail)
    log.show_value(api.config, log.Level.DEBUG, 'last_login', last_login)
    log.show_value(api.config, log.Level.DEBUG, 'last_ip', last_ip)
    log.show_value(api.config, log.Level.DEBUG, 'five_chess', five_chess)
    log.show_value(api.config, log.Level.DEBUG, 'chess', chess)
    log.show_value(api.config, log.Level.DEBUG,
                  'signature_file', signature_file)

    user = data_type.UserInfo(
        pttid,
        money,
        login_time,
        legal_post,
        illegal_post,
        state,
        mail,
        last_login,
        last_ip,
        five_chess,
        chess,
        signature_file
    )
    return user