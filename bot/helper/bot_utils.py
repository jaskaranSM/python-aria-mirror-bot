from bot import download_dict
from bot.helper.download_status import DownloadStatus

PROGRESS_MAX_SIZE = 100 // 8
PROGRESS_INCOMPLETE = ['▏', '▎', '▍', '▌', '▋', '▊', '▉']
SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']


def get_readable_file_size(size_in_bytes) -> str:
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f'{size_in_bytes} {SIZE_UNITS[index]}'
    except IndexError:
        return 'File too large'


def get_download(message_id):
    return download_dict[message_id].download()


def get_download_status_list():
    return list(download_dict.values())


def get_progress_bar_string(status: DownloadStatus):
    completed = status.download().completed_length/8
    total = status.download().total_length/8
    if total == 0:
        p = 0
    else:
        p = round(completed * 100 / total)
    p = min(max(p, 0), 100)
    cFull = p // 8
    cPart = p % 8 - 1
    p_str = '█'*cFull
    if cPart >= 0:
      p_str += PROGRESS_INCOMPLETE[cPart]
    p_str += ' '*(PROGRESS_MAX_SIZE - cFull)
    p_str = f"[{p_str}]"
    return p_str


def get_download_index(_list, gid, uid=None):
    index = 0
    if gid is not None:
        search = gid
        for i in _list:
            if i.download().gid == search:
                return index
            index += 1
    elif uid is not None:
        for i in _list:
            if i.uid == uid:
                return index
            index += 1
    else:
        return -1


def get_download_str():
    result = ""
    for status in list(download_dict.values()):
        result += (status.progress() + status.speed() + status.status())
    return result


def get_readable_message(progress_list: list = download_dict.values()):
    msg = ''
    for status in progress_list:
        msg += f'<b>Name:</b> {status.name()}\n' \
               f'<b>status:</b> {status.status()}\n'

        if status.status() == DownloadStatus.STATUS_DOWNLOADING:
            msg += f'<code>{get_progress_bar_string(status)}</code> {status.progress()} of {status.size()}\n' \
                   f'<b>Speed:</b> {status.speed()}\n' \
                   f'<b>ETA:</b> {status.eta()}\n'
        msg += '\n'
    return msg


# Custom Exception class for killing thread as soon as they aren't needed
class KillThreadException(Exception):
    def __init__(self, message, error=None):
        super().__init__(message)
        self.error = error
