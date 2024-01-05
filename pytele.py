import os
from random import randint

import cv2
import telebot
from telebot import types
from os.path import exists
import os
from PIL import Image
from wand.image import Image as imW
from time import sleep
import ffmpeg

import logging

# log info or debug  level=logging.DEBUG , level=logging.INFO
logging.basicConfig(filename="./log/log.txt",
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s ', level=logging.DEBUG)
logger = logging.getLogger(__name__)
# logger=logging.error(__name__)


bot = telebot.TeleBot("1911169525:AAHfAOyjrvpcsAmOWeIdAfLAtbYevJHzgBc", parse_mode=None)

imageFile_Name = "./image.jpg"
videoFile_Name = "./video.mp4"


@bot.message_handler(commands=['start'])
def start(message):
    stiekcer = open("./bender/webp/file_105578982.webp", 'rb')
    bot.send_sticker(message.chat.id, stiekcer)
    stiekcer.close()
    bot.send_message(message.chat.id, "Start : /start \n Help : /help")


@bot.message_handler(commands=['help'])
def send_welcome(message):
    # bot.send_message(message.chat.id, """<b>Hello</b>
    #  </br>
    #   <b>How are you Doing? </b>
    #    </br>
    #    <b>For Use This Bot Write or Click Command : </b>
    #    </br>
    #    <b>/start</b>
    #    <b>/help</b>
    #    <b>/image</b>
    #     """,parse_mode='html')
    # bot.send

    bot.send_chat_action(message.chat.id, action="typing")
    bot.send_message(message.chat.id, """Hello \n
     
How are you ? 
        
For Use This Bot Write or Click Command 📲 : 
       \n
Start Bot : /start ✅
شروع

Help Bot : /help 
کمک

Process Image : /image 🏞 
پردازش عکس

Procces Video : /video 🎥 
پردازش ویدیو

Fun :  /fun 😂\n
Keyboard : /keyboard ⌨
کیبورد

keyboard 2 : /keyboard2 ⌨
کیبورد 2
\n 
Good Luck 
موفق باشید 
\n
        """)
    # markup = types.ForceReply(selective=False)
    # bot.send_message(message.chat.id, "Send me another word:", reply_markup=markup)


@bot.message_handler(commands=['image'])
def imagemsg(message):
    bot.send_chat_action(message.chat.id, action="typing")
    bot.reply_to(message, "Send To Me Image 🏞 \n عکسی برایم بفرست 🏞")


@bot.message_handler(content_types=['photo'])
def image(message):
    print('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)

    with open(imageFile_Name, 'wb') as new_file:
        new_file.write(downloaded_file)

    file_exists = exists(imageFile_Name)
    if file_exists:
        bot.send_chat_action(message.chat.id, action="typing")
        bot.reply_to(message, "Upload Image Done !✅ \n ✅!عکس با موفقیت اپلود شد")
        sleep(1.5)
        bot.send_chat_action(message.chat.id, action="typing")
        bot.send_message(message.chat.id,
                         "Help Tools Here : \n (640 x 640) : /small \n (720x720) : /medium \n "
                         "White And Black Image : /WhiteAndBlack \n Kuwahara: /kuwahara \n Blure : /blure \n Convert JPG To PNG : /convert")

    else:
        bot.send_chat_action(message.chat.id, action="typing")
        bot.reply_to(message, "Upload Image is Feild 🙁")


@bot.message_handler(commands=['video'])
def videoMsg(msg):
    bot.reply_to(msg, "Send To Me Video 🎥 \n 🎥 !ویدیویی برایم ارسال کن")


@bot.message_handler(content_types=['sticker'])
def send_sticker(message):
    bot.send_sticker(message.chat.id, Choose_Sticker())


@bot.message_handler(content_types=['video'])
def video(message):
    print('message.video =', message.video)
    fileID = message.video.file_id
    print('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(videoFile_Name, 'wb') as new_file:
        new_file.write(downloaded_file)
    file_exists = exists(videoFile_Name)
    if file_exists:
        bot.send_chat_action(message.chat.id, action="typing")
        bot.reply_to(message, "Upload Video Done !✅")
        sleep(1.5)
        bot.send_chat_action(message.chat.id, action="typing")
        bot.send_message(message.chat.id,
                         "Help Tools Here : \n Convert Format : /formatt \n Trim or Cut Video : /trimm  \n Compress : /compresss ")

    else:
        bot.send_chat_action(message.chat.id, action="typing")
        bot.reply_to(message, "Upload Video is Feild 🙁")


@bot.message_handler(commands=['WhiteAndBlack'])
def WhiteAndBlackImage(message):
    if exists(imageFile_Name):
        img = Image.open(imageFile_Name)
        imgGray = img.convert('L')
        imgGray.save('image_whiteBlack.jpg')
        file_exists = exists("image_whiteBlack.jpg")
        if file_exists:
            print('Sucesse Procces')
            bot.send_chat_action(message.chat.id, action="upload_photo")
            imgg = open("./image_whiteBlack.jpg", 'rb')
            bot.send_photo(message.chat.id, imgg, caption="White And Black")
            imgg.close()
            # os.remove("./image_whiteBlack.jpg")
            # os.remove("./image.jpg")
            # print('Sucess  remove')
        else:
            print('error Procces')
            bot.reply_to("Error Procces 🙁")
    else:
        bot.reply_to(message, "Cant Find Image Please Send Me Again 🙁")


@bot.message_handler(commands=['blure'])
def BluredImage(message):
    img2 = "./image_blured.jpg"
    if exists(imageFile_Name):

        img = cv2.imread(imageFile_Name)
        blur = cv2.blur(img, (5, 5))
        cv2.imwrite(img2, blur)
        if exists(img2):
            print('Sucess blured')
            bot.send_chat_action(message.chat.id, action="upload_photo")
            imgg = open(img2, 'rb')
            bot.send_photo(message.chat.id, imgg, caption="Blured")
            imgg.close()
        else:
            bot.send_chat_action(message.chat.id, action="typing")
            bot.reply_to(message, "Cant Run Process 🙁")
    else:
        bot.reply_to(message, "Cant Find Image Please Send Me Again 🙁")


@bot.message_handler(commands=['kuwahara'])
def Kuwahara(message):
    img2 = "./image_kuwahara.jpg"

    if exists(imageFile_Name):

        with imW(filename=imageFile_Name) as img:
            img.kuwahara(radius=7, sigma=2)
            img.save(filename=img2)

        if exists(img2):
            bot.send_chat_action(message.chat.id, action="upload_photo")
            imgg = open(img2, 'rb')
            bot.send_photo(message.chat.id, imgg, caption="Kuwahara")
            imgg.close()
        else:
            bot.reply_to(message, "Please Try Again Process End 🙁")
    else:
        bot.set_chat_action(message.chat.id, action="typing")
        bot.reply_to(message, "Give To Me Image 🏞")


@bot.message_handler(commands=['fun'])
def Sticker(message):
    try:
        status = extract_arg(message.text)
        print(status[0])
    except IndexError:
        pass
    bot.reply_to(message, Choose_Msg())
    st = open(Choose_Sticker(), 'rb')
    bot.send_chat_action(message.chat.id, action="typing")
    bot.send_sticker(message.chat.id, st)
    st.close()


# cropImage_medium
@bot.message_handler(commands=['medium'])
def cropImage_medium(message):
    bot.send_chat_action(message.chat.id, action="typing")
    bot.reply_to(message, "cropImage")
    # if exists(imageFile_Name):
    #     img2="./image_crop_medium.jpg"
    #     with imW(filename=imageFile_Name) as img:
    #         size=img.size
    #
    #     if size[0] >=640 | size[1] >=640:
    #         img.crop(640,640,640,640)
    #         img.save(filename=img2)
    #     else:
    #         bot.reply_to(message,"Image Is To Small ")
    #
    # else:
    #     pass


@bot.message_handler(commands=['convert'])
def Convert_msg(message):
    bot.send_chat_action(message.chat.id, action="typing")
    bot.reply_to(message, "what Format : \n  JPG TO PNG : /pj ")


# jpg_to_png
@bot.message_handler(commands=['pj'])
def Convert_jpg_to_png(message):
    img2 = "./imagepng.png"
    file_exists_jpg = exists("./image.jpg")
    file_exists_png = exists("./image.png")
    if file_exists_jpg | file_exists_png:
        # img = cv2.imread('./image.jpg')
        # cv2.imwrite(img2, img)
        img = Image.open(imageFile_Name)
        img.save(img2)
        bot.send_chat_action(message.chat.id, action="upload_photo")
        imgg = open(img2, 'rb')
        bot.send_photo(message.chat.id, imgg, caption="Convert ")
        imgg.close()
        # os.remove(img2)
        # os.remove(imageFile_Name)
    else:
        bot.reply_to(message, "Give Image To Me 🏞")
        print(f"Convert_jpg_to_png=> Give Image To Me")


@bot.message_handler(commands=['formatt'])
def format_msg(message):
    print(f"format_msg => {extract_arg(message.text)}")
    bot.reply_to(message, "Help \n/format (Your format (mkv,mp4,web , .... )) \nExample /format mkv ")


@bot.message_handler(commands=['format'])
# format
def ChangeFormatVideo(message):
    print(message)
    exten = extract_arg(message.text[0])

    outPut = "./outPut_chnageFormat" + exten
    inPath = videoFile_Name
    if exists(videoFile_Name):
        if exten == 'mp4' | exten == 'mkv':
            stream = ffmpeg.input(inPath)
            stream = ffmpeg.output(stream, outPut + exten)
            ffmpeg.run(stream)
            if exists(outPut):
                print('Sucess ChangeFormatVideo')
                bot.send_chat_action(message.chat.id, action="upload_video")
                vid = open(outPut, 'rb')
                bot.send_photo(message.chat.id, vid, caption=exten)
                vid.close()
            else:
                bot.send_chat_action(message.chat.id, action="typing")
                bot.reply_to(message, "Cant Run Process 🙁")
        else:
            exten = "mp4"
            stream = ffmpeg.input(inPath)
            stream = ffmpeg.output(stream, outPut + exten)
            ffmpeg.run(stream)
            if exists(outPut):
                print('Sucess ChangeFormatVideo')
                bot.send_chat_action(message.chat.id, action="upload_video")
                vid = open(outPut, 'rb')
                bot.send_photo(message.chat.id, vid, caption=exten)
                vid.close()
            else:
                bot.send_chat_action(message.chat.id, action="typing")
                bot.reply_to(message, "Cant Run Process 🙁")

    else:
        bot.reply_to(message, "Cant Find File Please Try Again 🙁")


@bot.message_handler(commands=['trimm'])
def trim_Msg(message):
    print(f'trim_Msg => message : {message} \n -------------------------------------')
    bot.reply_to(message,
                 "Help \n /trim (Start Minute . End Minute . if You Want Change Format 'mkv' , 'mp4')  \n Examples : "
                 "\n /trim 2.4 \n or \n /trim 2.4.mkv")


@bot.message_handler(commands=['trim'])
def Trim_Video(message):
    outPath = "./outPut_Trim."
    text_list = extract_arg(message.text)
    print(f'Trim_Video => text_list : {text_list}')
    if len(text_list) == 1:
        txt_l = text_list[0]

        splii = Split_text(txt_l)
        print(f'Trim_Video => sta : {splii}')

        if len(splii) > 2:

            sta = splii[0]
            en = splii[1]
            exten = splii[2]
            print(f'Trim_Video => sta : {sta}')
            print(f'Trim_Video => en : {en}')
            print(f'Trim_Video => exten : {exten}')
            if checkInt(sta) == True & checkInt(en) == True:
                if checkStr(exten) == True:
                    if exten.__eq__("mp4") | exten.__eq__("mkv"):
                        if exists(videoFile_Name):
                            stream = ffmpeg.input(videoFile_Name)
                            stream = ffmpeg.trim(stream, start=sta, end=en)
                            stream = ffmpeg.output(stream, outPath + exten)
                            ffmpeg.run(stream)
                            if exists(outPath + exten):
                                # print('Trim_Video=> Sucess Trim_Video')
                                print('Trim_Video => Sucess Trim_Video  ')
                                bot.send_message(message.chat.id, "Process Video is Done !✅")
                                # bot.send_chat_action(message.chat.id, action="video_upload")
                                vid = open(outPath + exten, 'rb')
                                bot.send_photo(message.chat.id, vid, caption=exten)
                                vid.close()
                                os.remove(outPath + exten)
                            else:
                                bot.send_message(message.chat.id, "Cant Process Try Agian 🙁")
                                print('Trim_Video => Cant Process Try Agian ')
                        # else:
                        #     bot.send_message(message.chat.id, "Cant Process Try Agian")
                        #     print('Trim_Video => Cant Process Try Agian  ')
                        # else:
                        #     bot.send_message(message.chat.id, "You Wrong Text To Me Try Again")
                        #     print('Trim_Video => You Wrong Text To Me Try Again ')
                        else:
                            bot.reply_to(message, "You Command Wrong Send To Me 🙁")
                    else:
                        bot.reply_to(message, "Wrong Format Send To Me 🙁")
                else:
                    bot.reply_to(message, "Wrong Format Send To Me 🙁")
            else:
                bot.reply_to(message, "Wrong Nmber and Format Send To Me 🙁")
        else:
            sta = splii[0]
            en = splii[1]
            exten = "mp4"
            print(f'Trim_Video => sta : {sta}')
            print(f'Trim_Video => en : {en}')
            print(f'Trim_Video => exten : {exten}')

            if checkInt(sta) == True & checkInt(en) == True:
                if exists(videoFile_Name):
                    stream = ffmpeg.input(videoFile_Name)
                    stream = ffmpeg.trim(stream, start=sta, end=en)
                    stream = ffmpeg.output(stream, outPath + exten)
                    ffmpeg.run(stream)
                    if exists(outPath + exten):
                        print('Sucess Trim_Video')
                        print('Trim_Video => Sucess Trim_Video  ')
                        bot.send_message(message.chat.id, "Process Video is Done !✅")
                        # bot.send_chat_action(message.chat.id, action="video_upload")
                        vid = open(outPath + exten, 'rb')
                        bot.send_photo(message.chat.id, vid, caption=exten)
                        vid.close()
                        os.remove(outPath + exten)
                    else:
                        bot.send_message(message.chat.id, "Cant Process Try Agian 🙁")
                        print('Trim_Video => Cant Process Try Agian ')
                    # else:
                    #     bot.send_message(message.chat.id, "Cant Process Try Agian")
                    #     print('Trim_Video => Cant Process Try Agian  ')
                    # else:
                    #     bot.send_message(message.chat.id, "You Wrong Text To Me Try Again")
                    #     print('Trim_Video => You Wrong Text To Me Try Again ')
                else:
                    bot.reply_to(message, "You Command Wrong Send To Me 😃")
            else:

                bot.reply_to(message, "Wrong Nmber Send To Me 😃")
    else:
        bot.reply_to(message, "You Command Wrong Send To Me  😃")
        print('Trim_Video => You Command Wrong Send To Me ')


@bot.message_handler(commands=['keyboard2'])
def msgjs(message):
    bot.send_chat_action(message.chat.id, action="typing")
    bot.send_message(message.chat.id, "Main Menu : ", reply_markup=iniline_keyboard_main())
    # bot.reply_to(message, "Send To Me Image")


def iniline_keyboard_main():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text="Start", callback_data='start'),
        types.InlineKeyboardButton(text="Help", callback_data='start')
    )
    return keyboard


def iniline_keyboard_2():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text="Process Image 🌄 ", callback_data='image'),
        types.InlineKeyboardButton(text="Process Video 📽", callback_data='video'),
        types.InlineKeyboardButton(text="Fun ", callback_data='fun'),
        types.InlineKeyboardButton(text="Back", callback_data='back')
    )
    return keyboard


# 'Back 🔙':'back2'
list_image_menu = {'Blure': 'blure', 'White And Black ': 'whiteAndBlack', 'Kuwahara': 'kuwahara'}


def iniline_keyboard_image():
    keyboard = types.InlineKeyboardMarkup()
    for keys, values in list_image_menu.items():
        keyboard.add(
            types.InlineKeyboardButton(text=keys, callback_data=values),
        )
    return keyboard


list_video_menu = {'Format': 'formatt', 'Trim or Cut Video': 'trimm', 'Compress': 'compresss'}


def inline_keyboard_video():
    keyboard = types.InlineKeyboardMarkup()
    for keys, values in list_video_menu.items():
        keyboard.add(
            types.InlineKeyboardButton(text=keys, callback_data=values)
        )
    return keyboard


##################################################################################################################################
list_key = ['Start ✅', 'Help', 'Fun 😂', 'Image 🏞', 'Video 🎥', "Back 🔙", 'Remove Menu']


@bot.message_handler(commands=['keyboard'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(list_key[0])
    item2 = types.KeyboardButton(list_key[6])
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Main Menu ", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def key_board(msg):
    if msg.chat.type == 'private':
        print(f"msg.text => {msg.text}")
        print(f"msg.text => {msg}")
        # bot.forward_message(msg.chat.id, "")
        if msg.text == list_key[0]:
            print(f'Click {list_key[0]}')
            # bot.send_message(msg.chat.id, "start")

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item2 = types.KeyboardButton(list_key[1])
            item3 = types.KeyboardButton(list_key[2])
            item4 = types.KeyboardButton(list_key[3])
            item5 = types.KeyboardButton(list_key[4])
            item6 = types.KeyboardButton(list_key[5])
            markup.add(item2, item3, item4, item5, item6)
            bot.send_message(msg.chat.id, "Main Menu", reply_markup=markup)
            send_welcome(msg)

        elif msg.text == list_key[6]:
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(msg.chat.id, "Main Keyboard is Removed. \n Show Again /keyboard", reply_markup=markup)
        # back
        elif msg.text == list_key[5]:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton(list_key[0])
            item6 = types.KeyboardButton(list_key[6])
            markup.add(item1, item6)
            bot.send_message(msg.chat.id, "KeyBoard ⌨", reply_markup=markup)
        # help
        elif msg.text == list_key[1]:
            bot.reply_to(msg, "" + list_key[1])
            bot.send_message(msg.chat.id, """Hello \n

            How are you Doing? 

            For Use This Bot Write or Click Command 📲 :
                   \n
            Start Bot : /start ✅\n
            Help Bot : /help \n
            Process Image : /image 🏞 \n 
            Procces Video : /video 🎥 \n
            Fun :  /fun 😂\n
            Keyboard : /keyboard ⌨\n
            keyboard 2 : /keyboard2 ⌨\n 
            Good Luck 
                    """)
        # fun
        elif msg.text == list_key[2]:
            bot.send_chat_action(msg.chat.id, action="typing")
            sti=open(Choose_Sticker(),'rb')
            bot.send_sticker(msg.chat.id, sti)
            sti.close()
        # image
        elif msg.text == list_key[3]:
            bot.reply_to(msg, "" + list_key[3])
            bot.send_message(msg.chat.id, "Image Menu : ", reply_markup=iniline_keyboard_image())

        # video
        elif msg.text == list_key[4]:
            bot.reply_to(msg, "" + list_key[4])
            bot.send_message(msg.chat.id, "Video Menu : ", reply_markup=inline_keyboard_video())


###############################################################################################
@bot.callback_query_handler(func=lambda message: True)
def handle_query(message):
    print(message)
    msgData = message.data
    if msgData == 'start':
        # bot.reply_to(message, "start")
        # send_welcome(message)
        bot.send_chat_action(message.from_user.id, action="typing")
        bot.send_message(message.from_user.id, """Hello \n
     
How are you Doing? 
        
For Use This Bot Write or Click Command 📲 :
       \n
Start Bot : /start ✅\n
Help Bot : /help \n
Process Image : /image 🏞 \n 
Procces Video : /video 🎥 \n
Fun :  /fun 😂\n
Keyboard : /keyboard ⌨\n
keyboard 2 : /keyboard2 ⌨\n 
Good Luck 
        """)
    elif msgData == 'back':
        # bot.send_chat_action(message.chat.id, action="typing")
        bot.send_chat_action(message.from_user.id, action="typing")
        bot.send_message(message.from_user.id, "keyboard_main ⌨ \n کیبورد اصلی ⌨", reply_markup=iniline_keyboard_main())
    elif msgData == 'back2':
        # bot.send_chat_action(message.chat.id, action="typing")
        bot.send_chat_action(message.from_user.id, action="typing")
        bot.send_message(message.from_user.id, "Send To Me Image 🏞 ", reply_markup=iniline_keyboard_2())
    elif msgData == 'image':
        bot.send_chat_action(message.from_user.id, action="typing")
        bot.send_message(message.from_user.id, "Send To Me Image 🏞 \n عکسی برایم بفرست 🏞")
    elif msgData == 'video':
        bot.send_chat_action(message.from_user.id, action="typing")
        bot.send_message(message.from_user.id, "Send To Me Video 🎥 \n 🎥 !ویدیویی برایم ارسال کن")
    elif msgData == 'fun':
        bot.send_chat_action(message.from_user.id, action="typing")
        sti = open(Choose_Sticker(), 'rb')
        bot.send_sticker(message.from_user.id, sti)
        sti.close()

    elif msgData == get_values(list_image_menu, 0):
        # bot.reply_to(message,"/blure")
        bot.send_chat_action(message.from_user.id, action="typing")
        bot.send_message(message.from_user.id, "Blure")

    elif msgData == get_values(list_image_menu, 1):
        bot.send_chat_action(message.from_user.id, action="typing")
        bot.send_message(message.from_user.id, "whiteAndBlack")

    elif msgData == get_values(list_image_menu, 2):
        bot.send_chat_action(message.from_user.id, action="typing")
        bot.send_message(message.from_user.id, "kuwahara")

    elif msgData == get_values(list_video_menu, 0):
        bot.send_chat_action(message.from_user.id, action="typing")
        bot.send_message(message.from_user.id, "format")

    elif msgData == get_values(list_video_menu, 1):
        bot.send_chat_action(message.from_user.id, action="typing")
        bot.send_message(message.from_user.id, "Trim")

    elif msgData == get_values(list_video_menu, 2):
        bot.send_chat_action(message.from_user.id, action="typing")
        bot.send_message(message.from_user.id, "Compress")
        # bot.forward_message(message.chat.id,"")


@bot.chosen_inline_handler(func=lambda chosen_inline_result: True)
def test_chosen(chosen_inline_result):
    print(chosen_inline_result)


# @bot.inline_handler(lambda query: query.query == 'text')
@bot.inline_handler(func=lambda chosen_inline_result: True)
def query_text(inline_query):
    print(f'inline_query => {inline_query.id}')
    try:
        r = types.InlineQueryResultArticle('1', 'Result', types.InputTextMessageContent('Result message.'))
        r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('Result message2.'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)


@bot.message_handler(commands=['compress_help'])
def compress_help(message):
    bot.reply_to(message, "Send To Me a Video 🎥!")


@bot.message_handler(commands=['compress'])
def Compress_():
    outPut = "./video_compress.mp4"

    if exists(videoFile_Name):
        stream = ffmpeg.input(videoFile_Name)
        stream = ffmpeg.output(stream, outPut, **{'c:v': 'libx264', 'f': 'mp4'})
        ffmpeg.run(stream)
    else:
        pass


# FUNCTIONS
def extract_arg(arg):
    return arg.split()[1:]


def Get_ext(file_name):
    return os.path.splitext(file_name)


def Choose_Sticker():
    f = []
    for (dirpath, dirnames, filenames) in os.walk("./webp"):
        f.extend(filenames)
        break
    e = randint(0, len(f))
    return "./webp/" + f[e]


#
def Choose_Msg():
    msg = ['عه راست میگی! ', 'نه بابا ', ' خب دیگه چی ؟ ', 'برو بخواب دیگه ', 'نمیخواد پیام بدی ', 'بشین سر جات',
           'چی میگی؟', "Whats up ? "]

    msg1 = ["👀", "🤓", "🥶", "🎃", "👻", "🥵", "😂", "🥸", "🙃", "😎"]

    msg.extend(msg1)
    ra = randint(0, len(msg) - 1)
    return msg[ra]


def Split_text(txt):
    return txt.split(".")


def Search_in_folder():
    for (r, d, f) in os.walk('E:\\python\Bot'):
        # print(r)
        # print(d)
        # print(f)
        for d in f:
            pass
            # finaem=r+'\\'+d
            # if Path(d).stem == "aaaaaa":
            # return d


def get_keys(glList, index):
    return list(glList.keys())[index]


def get_values(gList, index):
    return list(gList.values())[index]


def checkInt(str):
    try:
        int(str)
        return True
    except ValueError:
        return False


def checkStr(strr):
    try:
        str(strr)
        return True
    except ValueError:
        return False

# for use zip you shuold begin file is type : start_zip
# for rnd zip file : end_zip
#please send me multi file

# RUN BOT
if __name__ == '__main__':
    bot.infinity_polling()
