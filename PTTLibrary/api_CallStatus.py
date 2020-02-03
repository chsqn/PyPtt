try:
    from . import data_type
    from . import i18n
    from . import ConnectCore
    from . import log
    from . import screens
    from . import exceptions
    from . import Command
except ModuleNotFoundError:
    import data_type
    import i18n
    import ConnectCore
    import log
    import screens
    import exceptions
    import Command


def get_callstatus(api) -> None:

    cmd_list = []
    cmd_list.append(Command.GoMainMenu)
    cmd_list.append('A')
    cmd_list.append(Command.Right)
    cmd_list.append(Command.Left)

    cmd = ''.join(cmd_list)

    target_list = [
        ConnectCore.TargetUnit(
            [
                i18n.GetCallStatus,
                i18n.Success,
            ],
            '[呼叫器]打開',
            break_detect=True,
            log_level=log.Level.DEBUG
        ),
        ConnectCore.TargetUnit(
            [
                i18n.GetCallStatus,
                i18n.Success,
            ],
            '[呼叫器]拔掉',
            break_detect=True,
            log_level=log.Level.DEBUG
        ),
        ConnectCore.TargetUnit(
            [
                i18n.GetCallStatus,
                i18n.Success,
            ],
            '[呼叫器]防水',
            break_detect=True,
            log_level=log.Level.DEBUG
        ),
        ConnectCore.TargetUnit(
            [
                i18n.GetCallStatus,
                i18n.Success,
            ],
            '[呼叫器]好友',
            break_detect=True,
            log_level=log.Level.DEBUG
        ),
        ConnectCore.TargetUnit(
            [
                i18n.GetCallStatus,
                i18n.Success,
            ],
            '[呼叫器]關閉',
            break_detect=True,
            log_level=log.Level.DEBUG
        ),
        ConnectCore.TargetUnit(
            [
                i18n.GetCallStatus,
            ],
            '★',
            response=cmd,
            log_level=log.Level.DEBUG
        ),
    ]

    for i in range(2):
        index = api.connect_core.send(cmd, target_list)
        if index < 0:
            if i == 0:
                continue
            ori_screen = api.connect_core.get_screen_queue()[-1]
            raise exceptions.UnknownError(ori_screen)

    if index == 0:
        return data_type.CallStatus.On
    if index == 1:
        return data_type.CallStatus.Unplug
    if index == 2:
        return data_type.CallStatus.Waterproof
    if index == 3:
        return data_type.CallStatus.Friend
    if index == 4:
        return data_type.CallStatus.Off

    ori_screen = api.connect_core.get_screen_queue()[-1]
    raise exceptions.UnknownError(ori_screen)


def set_callstatus(api, callstatus) -> None:
    # 打開 -> 拔掉 -> 防水 -> 好友 -> 關閉

    current_call_status = api._get_callstatus()

    cmd_list = []
    cmd_list.append(Command.GoMainMenu)
    cmd_list.append(Command.Ctrl_U)
    cmd_list.append('p')

    cmd = ''.join(cmd_list)

    target_list = [
        ConnectCore.TargetUnit(
            [
                i18n.SetCallStatus,
                i18n.Success
            ],
            screens.Target.InUserList,
            break_detect=True
        )
    ]

    while current_call_status != callstatus:
        api.connect_core.send(
            cmd,
            target_list,
            screen_timeout=api.config.screen_long_timeout
        )

        current_call_status = api._get_callstatus()