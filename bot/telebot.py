import logging
import sys
import datetime
import configparser
import argparse
import inspect
import re
from mwt import MWT
from dbhelper import DBHelper
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ChatPermissions
from telegram.ext import MessageHandler, Filters, CommandHandler, Updater, CallbackQueryHandler
from telegram.ext.dispatcher import run_async

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

db = DBHelper()

parser = argparse.ArgumentParser(description='Bot for helping in administration in DevOps groups in TG')

parser.add_argument("-b","--bottoken", dest="bottoken", type=str,default="1231423",help="Bot token for TG API")
parser.add_argument("-e","--environment", dest="environment", type=str,default="config.ini",help="Environment for bot")

args = parser.parse_args()
bottoken = args.bottoken
environment = args.environment

config = configparser.ConfigParser()
# config.read('config.ini')
config.read(environment)

# bottoken= str(sys.argv[1])
updater = Updater(token=bottoken, use_context=True)
dispatcher = updater.dispatcher

# Get admins list
@MWT(timeout=60*60)
def get_admin_ids(context, chat_id):
    """Returns a list of admin IDs for a given chat. Results are cached for 1 hour."""
    return [admin.user.id for admin in context.bot.get_chat_administrators(chat_id)]


# User commands
## Send user test tasks
def tasks(update, context):
        section = str(update.message.chat.id)
        username = re.sub("[_]", "\_", update.message.from_user.username)
        in_section = section in config.sections()
        command_name = inspect.currentframe().f_code.co_name
        feature_flag = config.get(section, command_name) == 'on'
        github_url = config.get(section, 'github_url')
        user_id = update.message.from_user.id
        first_name = re.sub("[_]", "\_", update.message.from_user.first_name)
        first_name = re.sub("[*]", "\*", first_name)
        first_name = re.sub("[`]", "\`", first_name)
        first_name = re.sub("[[]", "\[", first_name)
        if in_section and feature_flag:
                try:
                        context.bot.send_message(chat_id=update.message.chat_id, text="@" +  username + \
                                " here is your " + "[DevOps tasks]" + "(" + github_url + ")" + "." \
                                        ,parse_mode='Markdown', disable_web_page_preview=True)
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
                except TypeError:
                        context.bot.send_message(chat_id=update.message.chat_id, text="[" + first_name + "](tg://user?id=" + user_id + ")" + \
                                " here is your " + "[DevOps tasks]" + "(" + github_url + ")" + "." \
                                        , parse_mode='Markdown', disable_web_page_preview=True)
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)

tasks_handler = CommandHandler('tasks', tasks, run_async=True)
dispatcher.add_handler(tasks_handler)

## Send user starter kit
def starter(update, context):
        section = str(update.message.chat.id)
        username = re.sub("[_]", "\_", update.message.from_user.username)
        in_section = section in config.sections()
        command_name = inspect.currentframe().f_code.co_name
        feature_flag = config.get(section, command_name) == 'on'
        root_url = config.get('shared','root_url')
        channel_specify = config.get(section, 'study')
        starter = config.get(section, 'starter_filename')
        url = root_url + channel_specify + "/" + starter
        user_id = update.message.from_user.id
        first_name = re.sub("[_]", "\_", update.message.from_user.first_name)
        first_name = re.sub("[*]", "\*", first_name)
        first_name = re.sub("[`]", "\`", first_name)
        first_name = re.sub("[[]", "\[", first_name)
        if in_section and feature_flag:
                if update.message.reply_to_message is not None:
                        context.bot.send_message(chat_id=update.message.chat_id,text= "We have " + "[starter kit for newbies]" + "(" + url + ")" + \
                                ". Also we have test tasks for SRE and list of various courses. You can find them in the same repository or via bot (see man for commands).", \
                                parse_mode='Markdown', reply_to_message_id=update.message.reply_to_message.message_id)
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
                else:
                        try:
                                context.bot.send_message(chat_id=update.message.chat_id, text="@" +  username + \
                                        " here is your " + "[starter kit]" + "(" + url + ")" + "." \
                                                ,parse_mode='Markdown', disable_web_page_preview=True)
                                context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
                        except TypeError:
                                context.bot.send_message(chat_id=update.message.chat_id, text="[" + first_name + "](tg://user?id=" + user_id + ")" + \
                                        " here is your " + "[starter kit]" + "(" + url + ")" + "." \
                                                , parse_mode='Markdown', disable_web_page_preview=True)
                                context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)

starter_handler = CommandHandler('starter', starter, run_async=True)
dispatcher.add_handler(starter_handler)

## Send user middle kit
def middle(update, context):
        section = str(update.message.chat.id)
        username = re.sub("[_]", "\_", update.message.from_user.username)
        in_section = section in config.sections()
        command_name = inspect.currentframe().f_code.co_name
        feature_flag = config.get(section, command_name) == 'on'
        root_url = config.get('shared','root_url')
        channel_specify = config.get(section, 'study')
        middle = config.get(section, 'middle_filename')
        url = root_url + channel_specify + "/" + middle
        user_id = update.message.from_user.id
        first_name = re.sub("[_]", "\_", update.message.from_user.first_name)
        first_name = re.sub("[*]", "\*", first_name)
        first_name = re.sub("[`]", "\`", first_name)
        first_name = re.sub("[[]", "\[", first_name)
        if in_section and feature_flag:
                try:
                        context.bot.send_message(chat_id=update.message.chat_id, text="@" + username + \
                                " here is your " + "[middle kit]" + "(" + url + ")" + "." \
                                        , parse_mode='Markdown', disable_web_page_preview=True)
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
                except TypeError:
                        context.bot.send_message(chat_id=update.message.chat_id, text="[" + first_name + "](tg://user?id=" + user_id + ")" + \
                                " here is your " + "[middle kit]" + "(" + url + ")" + "." \
                                        , parse_mode='Markdown', disable_web_page_preview=True)
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)

middle_handler = CommandHandler('middle', middle, run_async=True)
dispatcher.add_handler(middle_handler)

## Send user middle kit
def hrman(update, context):
        section = str(update.message.chat.id)
        username = re.sub("[_]", "\_", update.message.from_user.username)
        in_section = section in config.sections()
        command_name = inspect.currentframe().f_code.co_name
        feature_flag = config.get(section, command_name) == 'on'
        root_url = config.get('shared','root_url')
        hrman = config.get('shared', 'hrman_filename')
        url = root_url + hrman
        user_id = update.message.from_user.id
        first_name = re.sub("[_]", "\_", update.message.from_user.first_name)
        first_name = re.sub("[*]", "\*", first_name)
        first_name = re.sub("[`]", "\`", first_name)
        first_name = re.sub("[[]", "\[", first_name)
        if in_section and feature_flag:
                if update.message.reply_to_message is not None:
                        context.bot.send_message(chat_id=update.message.chat_id,text= "We have " + "[HR man]" + "(" + url + ")" + \
                                ". Please read it carefully.", \
                                parse_mode='Markdown', reply_to_message_id=update.message.reply_to_message.message_id, disable_web_page_preview=True)
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
                else:
                        try:
                                context.bot.send_message(chat_id=update.message.chat_id, text="@" + username + \
                                        " here is your " + "[HR man]" + "(" + url + ")" + "." \
                                                , parse_mode='Markdown', disable_web_page_preview=True)
                                context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
                        except TypeError:
                                context.bot.send_message(chat_id=update.message.chat_id, text="[" + first_name + "](tg://user?id=" + user_id + ")" + \
                                        " here is your " + "[HR man]" + "(" + url + ")" + "." \
                                                , parse_mode='Markdown', disable_web_page_preview=True)
                                context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)

hrman_handler = CommandHandler('hrman', hrman, run_async=True)
dispatcher.add_handler(hrman_handler)


## Send user tips for certifications
def cert(update, context):
        section = str(update.message.chat.id)
        username = re.sub("[_]", "\_", update.message.from_user.username)
        in_section = section in config.sections()
        command_name = inspect.currentframe().f_code.co_name
        feature_flag = config.get(section, command_name) == 'on'
        root_url = config.get('shared','root_url')
        channel_specify = config.get(section, 'study')
        certification = config.get(section, 'certification_filename')
        url = root_url + channel_specify + "/" + certification
        user_id = update.message.from_user.id
        first_name = re.sub("[_]", "\_", update.message.from_user.first_name)
        first_name = re.sub("[*]", "\*", first_name)
        first_name = re.sub("[`]", "\`", first_name)
        first_name = re.sub("[[]", "\[", first_name)
        if in_section and feature_flag:
                try:
                        context.bot.send_message(chat_id=update.message.chat_id, text="@" +  username + \
                                " here is your " + "[certification tips]" + "(" + url + ")" + "." \
                                        , parse_mode='Markdown', disable_web_page_preview=True)
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
                except TypeError:
                        context.bot.send_message(chat_id=update.message.chat_id, text="[" + first_name + "](tg://user?id=" + user_id + ")" + \
                                " here is your " + "[certification tips]" + "(" + url + ")" + "." \
                                        , parse_mode='Markdown', disable_web_page_preview=True)
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)

cert_handler = CommandHandler('cert', cert, run_async=True)
dispatcher.add_handler(cert_handler)

## Send user list of various courses
def course(update, context):
        section = str(update.message.chat.id)
        username = re.sub("[_]", "\_", update.message.from_user.username)
        in_section = section in config.sections()
        command_name = inspect.currentframe().f_code.co_name
        feature_flag = config.get(section, command_name) == 'on'
        root_url = config.get('shared','root_url')
        channel_specify = config.get('shared', 'course_folder')
        certification = config.get('shared', 'course_filename')
        url = root_url + channel_specify + "/" + certification
        user_id = update.message.from_user.id
        first_name = re.sub("[_]", "\_", update.message.from_user.first_name)
        first_name = re.sub("[*]", "\*", first_name)
        first_name = re.sub("[`]", "\`", first_name)
        first_name = re.sub("[[]", "\[", first_name)
        if in_section and feature_flag:
                try:
                        context.bot.send_message(chat_id=update.message.chat_id, text="@" + username + \
                               " here is your " + "[courses list]" + "(" + url + ")" + "." \
                                        , parse_mode='Markdown', disable_web_page_preview=True)
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
                except TypeError:
                        context.bot.send_message(chat_id=update.message.chat_id, text="[" + first_name + "](tg://user?id=" + user_id + ")" + \
                                " here is your " + "[courses list]" + "(" + url + ")" + "." \
                                        , parse_mode='Markdown', disable_web_page_preview=True)
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)

course_handler = CommandHandler('course', course, run_async=True)
dispatcher.add_handler(course_handler)

## Send user list of various relocate chats
def relocate(update, context):
        section = str(update.message.chat.id)
        username = re.sub("[_]", "\_", update.message.from_user.username)
        in_section = section in config.sections()
        command_name = inspect.currentframe().f_code.co_name
        feature_flag = config.get(section, command_name) == 'on'
        root_url = config.get('shared','root_url')
        relocate = config.get('shared', 'relocate_filename')
        url = root_url + relocate
        user_id = update.message.from_user.id
        first_name = re.sub("[_]", "_", update.message.from_user.first_name)
        first_name = re.sub("[*]", "\*", first_name)
        first_name = re.sub("[`]", "\`", first_name)
        first_name = re.sub("[[]", "\[", first_name)
        if in_section and feature_flag:
                try:
                        context.bot.send_message(chat_id=update.message.chat_id, text="@" +  username + \
                                " here is your " + "[relocate chats and channels]" + "(" + url + ")" + "." \
                                        , parse_mode='Markdown', disable_web_page_preview=True)
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
                except TypeError:
                        context.bot.send_message(chat_id=update.message.chat_id, text="[" + first_name + "](tg://user?id=" + user_id + ")" + \
                                " here is your " + "[relocate chats and channels]" + "(" + url + ")" + "." \
                                        , parse_mode='Markdown', disable_web_page_preview=True)
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)

relocate_handler = CommandHandler('relocate', relocate, run_async=True)
dispatcher.add_handler(relocate_handler)

## Send use Code of Conduct
def coc(update, context):
        section = str(update.message.chat.id)
        username = re.sub("[_]", "\_", update.message.from_user.username)
        in_section = section in config.sections()
        command_name = inspect.currentframe().f_code.co_name
        feature_flag = config.get(section, command_name) == 'on'
        root_url = config.get('shared','root_url')
        coc = config.get('shared', 'coc_filename')
        url = root_url + coc
        user_id = update.message.from_user.id
        first_name = re.sub("[_]", "\_", update.message.from_user.first_name)
        first_name = re.sub("[*]", "\*", first_name)
        first_name = re.sub("[`]", "\`", first_name)
        first_name = re.sub("[[]", "\[", first_name)
        if in_section and feature_flag:
                try:
                        context.bot.send_message(chat_id=update.message.chat_id, text="@" +  username + \
                                " here is your " + "[code of conduct]" + "(" + url + ")" + "." \
                                        , parse_mode='Markdown', disable_web_page_preview=True)
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
                except TypeError:
                        context.bot.send_message(chat_id=update.message.chat_id, text="[" + first_name + "](tg://user?id=" + user_id + ")" + \
                                " here is your " + "[code of conduct]" + "(" + url + ")" + "." \
                                        , parse_mode='Markdown', disable_web_page_preview=True)
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)


coc_handler = CommandHandler('coc', coc, run_async=True)
dispatcher.add_handler(coc_handler)

## Send user job opportunity and cv publish rules
def work(update, context):
        section = str(update.message.chat.id)
        username = re.sub("[_]", "\_", update.message.from_user.username)
        in_section = section in config.sections()
        command_name = inspect.currentframe().f_code.co_name
        feature_flag = config.get(section, command_name) == 'on'
        root_url = config.get('shared','root_url')
        coc = config.get('shared', 'jobs_filename')
        url = root_url + coc
        user_id = update.message.from_user.id
        first_name = re.sub("[_]", "\_", update.message.from_user.first_name)
        first_name = re.sub("[*]", "\*", first_name)
        first_name = re.sub("[`]", "\`", first_name)
        first_name = re.sub("[[]", "\[", first_name)
        if in_section and feature_flag:
                if update.message.reply_to_message is not None:
                        context.bot.send_message(chat_id=update.message.chat_id,text= "We have " + "[job opportunities and cv publish rules]" + "(" + url + ")" + \
                                ". Please read them carefully and follow them.", \
                                parse_mode='Markdown', reply_to_message_id=update.message.reply_to_message.message_id, disable_web_page_preview=True)
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
                else:
                        try:
                                context.bot.send_message(chat_id=update.message.chat_id, text="@" +  username + \
                                        " here is your " + "[job opportunities and cv publish rules]" + "(" + url + ")" + "." \
                                                , parse_mode='Markdown', disable_web_page_preview=True)
                                context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
                        except TypeError:
                                context.bot.send_message(chat_id=update.message.chat_id, text="[" + first_name + "](tg://user?id=" + user_id + ")" + \
                                        " here is your " + "[job opportunities and cv publish rules]" \
                                                + "(" + url + ")" + ".", parse_mode='Markdown', disable_web_page_preview=True)
                                context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)


work_handler = CommandHandler('work', work, run_async=True)
dispatcher.add_handler(work_handler)

## Send user advertising rules
def ad(update, context):
        section = str(update.message.chat.id)
        username = re.sub("[_]", "\_", update.message.from_user.username)
        in_section = section in config.sections()
        command_name = inspect.currentframe().f_code.co_name
        feature_flag = config.get(section, command_name) == 'on'
        root_url = config.get('shared','root_url')
        coc = config.get('shared', 'advertising_filename')
        url = root_url + coc
        user_id = update.message.from_user.id
        first_name = re.sub("[_]", "\_", update.message.from_user.first_name)
        first_name = re.sub("[*]", "\*", first_name)
        first_name = re.sub("[`]", "\`", first_name)
        first_name = re.sub("[[]", "\[", first_name)
        if in_section and feature_flag:
                try:
                        context.bot.send_message(chat_id=update.message.chat_id, text="@" +  username + \
                                " here is your " + "[advertising publish rules]" + "(" + url + ")" + "." \
                                        , parse_mode='Markdown', disable_web_page_preview=True)
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
                except TypeError:
                        context.bot.send_message(chat_id=update.message.chat_id, text="[" + first_name + "](tg://user?id=" + user_id + ")" + \
                                " here is your " + "[advertising publish rules]" \
                                        + "(" + url + ")" + ".", parse_mode='Markdown', disable_web_page_preview=True)
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)


ad_handler = CommandHandler('ad', ad, run_async=True)
dispatcher.add_handler(ad_handler)

## Send user list of friendly chats
def chats(update, context):
        section = str(update.message.chat.id)
        username = re.sub("[_]", "\_", update.message.from_user.username)
        in_section = section in config.sections()
        command_name = inspect.currentframe().f_code.co_name
        feature_flag = config.get(section, command_name) == 'on'
        root_url = config.get('shared','root_url')
        coc = config.get('shared', 'othet_chats')
        url = root_url + coc
        user_id = update.message.from_user.id
        first_name = re.sub("[_]", "\_", update.message.from_user.first_name)
        first_name = re.sub("[*]", "\*", first_name)
        first_name = re.sub("[`]", "\`", first_name)
        first_name = re.sub("[[]", "\[", first_name)
        if in_section and feature_flag:
                try:
                        context.bot.send_message(chat_id=update.message.chat_id, text="@" +  username + \
                                " here is your " + "[friendly chats list]" + "(" + url + ")" + "." \
                                        , parse_mode='Markdown', disable_web_page_preview=True)
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
                except TypeError:
                        context.bot.send_message(chat_id=update.message.chat_id, text="[" + first_name + "](tg://user?id=" + user_id + ")" + \
                                " here is your " + "[friendly chats list]" \
                                        + "(" + url + ")" + ".", parse_mode='Markdown', disable_web_page_preview=True)
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)


chats_handler = CommandHandler('chats', chats, run_async=True)
dispatcher.add_handler(chats_handler)

## Send user events rules
def events(update, context):
        section = str(update.message.chat.id)
        username = re.sub("[_]", "\_", update.message.from_user.username)
        in_section = section in config.sections()
        command_name = inspect.currentframe().f_code.co_name
        feature_flag = config.get(section, command_name) == 'on'
        root_url = config.get('shared','root_url')
        coc = config.get('shared', 'events_list')
        url = root_url + coc
        user_id = update.message.from_user.id
        first_name = re.sub("[_]", "\_", update.message.from_user.first_name)
        first_name = re.sub("[*]", "\*", first_name)
        first_name = re.sub("[`]", "\`", first_name)
        first_name = re.sub("[[]", "\[", first_name)
        if in_section and feature_flag:
                try:
                        context.bot.send_message(chat_id=update.message.chat_id, text="@" +  username + \
                                " here is your " + "[events list]" + "(" + url + ")" + "." \
                                        , parse_mode='Markdown', disable_web_page_preview=True)
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
                except TypeError:
                        context.bot.send_message(chat_id=update.message.chat_id, text="[" + first_name + "](tg://user?id=" + user_id + ")" + \
                                " here is your " + "[events list]" \
                                        + "(" + url + ")" + ".", parse_mode='Markdown', disable_web_page_preview=True)
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)


events_handler = CommandHandler('events', events, run_async=True)
dispatcher.add_handler(events_handler)

## User send report message to admins
def report(update, context):
        section = str(update.message.chat.id)
        in_section = section in config.sections()
        command_name = inspect.currentframe().f_code.co_name
        feature_flag = config.get(section, command_name) == 'on'
        chat_id = str(update.message.chat_id)
        user_id = str(update.message.reply_to_message.from_user.id)
        message_id = str(update.message.reply_to_message.message_id)
        keyboard = [
                [InlineKeyboardButton('burn spam', callback_data='spam ' + chat_id + ' ' + user_id + ' ' + message_id)]
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if in_section and feature_flag:
                try:
                        context.bot.send_message(chat_id=update.message.chat_id, text="Report on [spam message]("+ "https://t.me/" + str(update.message.chat.username) + "/" \
                                + str(update.message.reply_to_message.message_id) + ")" + " was send to admins. Please be patient.", \
                                disable_web_page_preview=True, parse_mode='Markdown')
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
                        context.bot.forward_message(chat_id=config.get(section, 'admin_chat'), from_chat_id=update.message.chat_id, message_id=update.message.reply_to_message.message_id)
                        context.bot.send_message(chat_id=config.get(section, 'admin_chat'), text="User think it's spam: " + "https://t.me/"+ str(update.message.chat.username)+"/" \
                                + str(update.message.reply_to_message.message_id), disable_web_page_preview=True, reply_markup=reply_markup)
                except AttributeError:
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
                        context.bot.send_message(chat_id=update.message.chat_id, text="Report command works on replied messages only.")

report_handler = CommandHandler('report', report)
dispatcher.add_handler(report_handler)

## User summon some HRs in thread
def summon(update, context):
        section = str(update.message.chat.id)
        in_section = section in config.sections()
        command_name = inspect.currentframe().f_code.co_name
        feature_flag = config.get(section, command_name) == 'on'
        if in_section and feature_flag:
                try:
                        context.bot.send_message(chat_id=update.message.chat_id, text= "I'm DevOps Bot and i summon you HR for answer: " + \
                                config.get(section, 'summon_list') + " and the question is: " + str(update.message.reply_to_message.text), \
                                        reply_to_message_id=update.message.message_id)
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
                except AttributeError:
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
                        context.bot.send_message(chat_id=update.message.chat_id, text="Summon command works on replied messages only.")

summon_handler = CommandHandler('summon', summon, run_async=True)
dispatcher.add_handler(summon_handler)

## Send user bots man
def man(update, context):
        section = str(update.message.chat.id)
        username = re.sub("[_]", "\_", update.message.from_user.username)
        in_section = section in config.sections()
        command_name = inspect.currentframe().f_code.co_name
        feature_flag = config.get(section, command_name) == 'on'
        user_id = update.message.from_user.id
        first_name = re.sub("[_]", "\_", update.message.from_user.first_name)
        first_name = re.sub("[*]", "\*", first_name)
        first_name = re.sub("[`]", "\`", first_name)
        first_name = re.sub("[[]", "\[", first_name)
        if in_section and feature_flag:
                try:
                        f = open("helps/" + config.get(section, 'commands_list') + "/commands.txt", "r")
                        context.bot.send_message(chat_id=update.message.chat_id, text="@" + username + " here it is. " \
                        + "\n" + f.read(), parse_mode='Markdown', disable_web_page_preview=True)
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
                except TypeError:
                        f = open("helps/" + config.get(section, 'commands_list') + "/commands.txt", "r")
                        context.bot.send_message(chat_id=update.message.chat_id, text="[" + first_name + "](tg://user?id=" + user_id + ")" + \
                        + "\n" + f.read(), parse_mode='Markdown', disable_web_page_preview=True)
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)

man_handler = CommandHandler('man', man, run_async=True)
dispatcher.add_handler(man_handler)

# Administrator commands

## Mute some user
def mute(update, context):
        section = str(update.message.chat.id)
        in_section = section in config.sections()
        command_name = inspect.currentframe().f_code.co_name
        feature_flag = config.get(section, command_name) == 'on'
        admins = update.message.from_user.id in get_admin_ids(context, update.message.chat_id)
        date = int()
        restrict = ChatPermissions(can_send_messages=False, can_send_media_messages=False, can_send_other_messages=False, can_add_web_page_previews=False)
        if in_section and feature_flag and admins:
                try:
                        if len(sys.argv) < 1:
                                date = int(' '.join(context.args))
                        else:
                                date = int(1)
                        context.bot.restrict_chat_member(chat_id=update.message.chat_id, user_id=update.message.reply_to_message.from_user.id, \
                                until_date=datetime.datetime.now() + datetime.timedelta(days=date), permissions = restrict)
                        context.bot.send_message(chat_id=update.message.chat_id, text="User " + "@" + str(update.message.reply_to_message.from_user.username) + " banned.", \
                                reply_to_message_id=update.message.message_id)
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
                except TypeError:
                        if len(sys.argv) < 1:
                                date = int(' '.join(context.args))
                        else:
                                date = int(1)
                        context.bot.restrict_chat_member(chat_id=update.message.chat_id, user_id=update.message.reply_to_message.from_user.id, \
                                until_date=datetime.datetime.now() + datetime.timedelta(days=date), permissions = restrict)
                        context.bot.send_message(chat_id=update.message.chat_id, text="User" + " banned", \
                                reply_to_message_id=update.message.message_id)
                        context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)

mute_handler = CommandHandler('mute', mute, pass_args=True, run_async=True)
dispatcher.add_handler(mute_handler)

## Warn some user
def warn(update, context, args):
        user_id = update.message.reply_to_message.from_user.id
        user_username = update.message.reply_to_message.from_user.username
        admin_username = re.sub("[_]", "\_", update.message.from_user.username)
        warn = int(0)
        section = str(update.message.chat.id)
        in_section = section in config.sections()
        command_name = inspect.currentframe().f_code.co_name
        feature_flag = config.get(section, command_name) == 'on'
        admins = update.message.from_user.id in get_admin_ids(context, update.message.chat_id)
        if in_section and feature_flag and admins:
                db.add_user(user_id, user_username, warn)
                db.add_warn(user_id, user_username, warn)
                warn_text = db.count_warn(user_id)
                reason = str(' '.join(args))
                context.bot.send_message(chat_id=update.message.chat_id, text="@"+ str(user_username) + \
                        " your warn count: " + str(warn_text) + str("/3.") + "If you get 3 warns you will be banned for 3 days." + "\n" +
                        "Admin: @" + admin_username + "\n" + "Reason: " + reason, reply_to_message_id=update.message.message_id)
                context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
        if warn_text >= 3:
                db.delete_warn(user_id, user_username, warn)
                context.bot.restrict_chat_member(chat_id=update.message.chat_id, user_id=update.message.reply_to_message.from_user.id, \
                        can_send_messages=False, can_send_media_messages=False, can_send_other_messages=False, \
                        can_add_web_page_previews=False, until_date=datetime.datetime.now() + datetime.timedelta(days=3))

warn_handler = CommandHandler('warn', warn, pass_args=True, run_async=True)
dispatcher.add_handler(warn_handler)

## Unwarn user
def unwarn(update, context):
        user_id = update.message.reply_to_message.from_user.id
        user_username = update.message.reply_to_message.from_user.username
        warn = int(0)
        section = str(update.message.chat.id)
        in_section = section in config.sections()
        command_name = inspect.currentframe().f_code.co_name
        feature_flag = config.get(section, command_name) == 'on'
        admins = update.message.from_user.id in get_admin_ids(context, update.message.chat_id)
        if in_section and feature_flag and admins:
                db.unwarn(user_id, user_username, warn)
                warn_text = db.count_warn(user_id)
                context.bot.send_message(chat_id=update.message.chat_id, text="@"+ str(update.message.reply_to_message.from_user.username) + \
                        " your warn count: " + str(warn_text) + str("/3.") + "If you get 3 warns you will be banned for 3 days.", \
                         reply_to_message_id=update.message.message_id)
                context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)

unwarn_handler = CommandHandler('unwarn', unwarn, run_async=True)
dispatcher.add_handler(unwarn_handler)

## Move message from one chat to another
def move(update, context):
        section = str(update.message.chat.id)
        in_section = section in config.sections()
        command_name = inspect.currentframe().f_code.co_name
        feature_flag = config.get(section, command_name) == 'on'
        admins = update.message.from_user.id in get_admin_ids(context, update.message.chat_id)
        if in_section and feature_flag and admins:
                if update.message.reply_to_message.photo:
                        try:
                                context.bot.send_message(chat_id=config.get(section, 'move_from_id'), text="Your photo " + "@" + str(update.message.reply_to_message.from_user.username) \
                                        +  " was moved to " + config.get(section, 'move_to_name'))
                                context.bot.forward_message(chat_id=config.get(section, 'move_to_id'), from_chat_id=update.message.chat_id, message_id=update.message.reply_to_message.message_id)
                                context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
                                context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.reply_to_message.message_id)
                        except TypeError:
                                context.bot.send_message(chat_id=config.get(section, 'move_from_id'), text="Your photo " + \
                                        " was moved to " + config.get(section, 'move_to_name'))
                                context.bot.forward_message(chat_id=config.get(section, 'move_to_id'), from_chat_id=update.message.chat_id, message_id=update.message.reply_to_message.message_id)
                                context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
                                context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.reply_to_message.message_id)
                else:
                        try:
                                context.bot.send_message(chat_id=config.get(section, 'move_from_id'), text="Your post " + "@" + str(update.message.reply_to_message.from_user.username) \
                                        +  " was moved to " + config.get(section, 'move_to_name'))
                                context.bot.send_message(chat_id=config.get(section, 'move_to_id'), text="Message was forwarded from: " + "@" + str(update.message.chat.username) + "\n" + \
                                        "Author: " + "@" + str(update.message.reply_to_message.from_user.username) + "\n" +  \
                                        "Message: " + str(update.message.reply_to_message.text))
                                context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
                                context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.reply_to_message.message_id)
                        except TypeError:
                                context.bot.send_message(chat_id=config.get(section, 'move_from_id'), text="Your post " + \
                                        " was moved to " + config.get(section, 'move_to_name'))
                                context.bot.send_message(chat_id=config.get(section, 'move_to_id'), text="Message was forwarded from: " + "@" + str(update.message.chat.username) + "\n" + \
                                        "Author: " + str(update.message.reply_to_message.from_user.first_name) + "\n" +  \
                                        "Message: " + str(update.message.reply_to_message.text))
                                context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
                                context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.reply_to_message.message_id)


move_handler = CommandHandler('move', move, run_async=True)
dispatcher.add_handler(move_handler)

## Post job opportunity into channel
def job(update, context):
        section = str(update.message.chat.id)
        in_section = section in config.sections()
        command_name = inspect.currentframe().f_code.co_name
        feature_flag = config.get(section, command_name) == 'on'
        admins = update.message.from_user.id in get_admin_ids(context, update.message.chat_id)
        if in_section and feature_flag and admins:
                context.bot.forward_message(chat_id=config.get(section, 'post_to_name'), from_chat_id=update.message.chat_id, \
                        message_id=update.message.reply_to_message.message_id,  disable_notification=False)
                context.bot.send_message(chat_id=config.get(section, 'post_from_id'), reply_to_message_id=update.message.reply_to_message.message_id, \
                        text="Your post was posted in " + config.get(section, 'post_to_name'))
                context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)

job_handler = CommandHandler('job', job, run_async=True)
dispatcher.add_handler(job_handler)

## Get chat number
def idnumber(update, context):
        admins = update.message.from_user.id in get_admin_ids(context, update.message.chat_id)
        if admins:
                context.bot.send_message(chat_id=update.message.chat_id, text=update.message.chat_id)
                context.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)

idnumber_handler = CommandHandler('idnumber', idnumber, run_async=True)
dispatcher.add_handler(idnumber_handler)

## Delete service messages
def delete_service_message(update, context):
        section = str(update.message.chat.id)
        in_section = section in config.sections()
        command_name = inspect.currentframe().f_code.co_name
        feature_flag = config.get(section, command_name) == 'on'
        msg = update.effective_message
        if in_section and feature_flag:
                context.bot.delete_message(chat_id=msg.chat.id,message_id=msg.message_id)

dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, delete_service_message, run_async=True))
dispatcher.add_handler(MessageHandler(Filters.status_update.left_chat_member, delete_service_message, run_async=True))

## Delete spam message and Ban spamer with admin button
def delete_ban_button(update, context):
        query = update.callback_query
        query.answer()
        callback_data = query.message.reply_markup.inline_keyboard[0][0].callback_data
        chat_id = int(callback_data.split()[1])
        user_id = int(callback_data.split()[2])
        message_id = int(callback_data.split()[3])
        admin_username = query.from_user.username
### i see no reason to double check
#        section = str(chat_id)
#        in_section = section in config.sections()
#        command_name = inspect.currentframe().f_code.co_name
#        feature_flag = config.get(section, command_name) == 'on'
#        if in_section and feature_flag:
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        context.bot.kick_chat_member(chat_id=chat_id, user_id=user_id)
        query.edit_message_text(text="Approved by @"+admin_username)

button_spam_handler = CallbackQueryHandler(delete_ban_button, pattern='spam[\s\S]+', run_async=True)
dispatcher.add_handler(button_spam_handler)


def main():
        db.setup()

if __name__ == '__main__':
    main()
updater.start_polling()
