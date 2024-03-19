import vk_api
import requests
import asyncio
import time
import pymysql
import sqlite3
import os
import json
import threading
import random
import datetime
from vk_api.longpoll import VkLongPoll, VkEventType
from threading import Thread
from config import host, user, password, db_name
from db import VKDB
VKDB = VKDB('list_groupsDB.db')
from massagePattern import msgPatr

##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  MYSQL  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#try:
#    connection = pymysql.connect(
#        host="127.0.0.1",
#        port=3306,
#        user="mysql",
#        password="mysql",
#        database="db_name",
#        cursorclass=pymysql.cursors.DictCursor
#    )
#    print("Successfully connected...")
#    print("#" * 20)
#
#    try:
#        #cursor = connection.cursor()
#        #create table
#        with connection.cursor() as cursor:
#            create_table_query = "CREATE TABLE 'users'(id int AUTO_INCREMENT," \
#                                  "name varchar(32)," \
#                                  "password varchar(32)," \
#                                  "email varchar(32)), PRIMARY KEY (id);"
#            cursor.execute(create_table_query)
#            print("Table created successfully")
#
#    finally:
#        connection.close()
#except Exception as ex:
#    print("Connection refused...")
#    print(ex)
#
#
##??????????????????????????????????  MYSQL  ?????????????????????????????????????????????????

try:
    conn = sqlite3.connect("list_groupsDB.db")
    cursor = conn.cursor()

    # Создаём пользователя с user_id = 1000
    cursor.execute("INSERT OR IGNORE INTO 'users' ('user_id') VALUES (?)", (1000,))

    #СЧИТЫВАЕМ ВСЕХ ПОЛЬЗОВАТЕЛЕЙ
    users = cursor.execute("SELECT * FROM 'users'")
    print(users.fetchall())

    #Подтверждаем изменения
    conn.commit()

except sqlite3.Error as error:
    print("Error", error)

finally:
    if(conn):
        conn.close()



#
IdChat_Name_S = 143
Chat_Send_Id = 2000000143
Day_Nedeli_Count: int = 6
NameGroupStr = "ИВТб–221"
access_token = "vk1.a.K0JCI9N8utAHXJ85DWhl8YLfjZ1jzTzTz8fJSQk5oyXaeU-WHZutV9iVJVObi1NgPpDDgeOWkIaW6_xBSIzgqZEio3QY1aAUApPYl3gweuo-Vv3STHCLiweMMShHu4cxdmpwWJ7yqSwVyWQ2kbqNYN0lISHoNEFchEC92lNhFnzwAVZeGn6Ti5rM_kvnd-VpZ8F2mxm-xWy4CvtzuZIO6A"
#мой
#access_token = "vk1.a.RXdjsD3_7g6OI8fBHhQyQzvkKtqlxafI3L0_HKJJhSZI2G8YJmkbrtjPuQJGaIJ5RAo2qz0uEoUosWWnf2sti3T8Srv77Sv5ucqeVcegeHkHzWWycvvnS74P4l70fq3a16FLSSxwJqgRkzzrlq72rnA6XcrAz7OSc1GSwP9w-ZCuA0b5x0WEsQjJ8k5EpAf7BEQ4fF8mXFuhpgWUnUZNMw"
vk_session = vk_api.VkApi(token=access_token)
# session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session) #, group_id=Chat_Send_Id

def send_message(_ids, _mes):
    api_url = 'https://api.vk.com/method/messages.send'
    params = {
        'peer_id': _ids,
        'message': _mes,
        'access_token': access_token,
        'random_id': 0,
        'v': '5.154'
    }
    response = requests.get(api_url, params=params)


def check_mes():
    print("CHECK MES START")

    while True:

        for event in longpoll.listen():
            print("NsED")
            if event.type == VkEventType.MESSAGE_NEW and event.from_chat:
                print("NEW MESSAGE DETECTED")
                if event.from_chat:
                    peer_id = event.peer_id
                    if peer_id == Chat_Send_Id:
                        messager = event.text.lower()
                        print("NEW MESSAGE DETECTED")

                        with open("otvets.txt", "r", encoding="utf-8") as file:
                            for line in file:

                                value1, value2 = line.strip().split("&")
                                print("Сообщение: "+value1+" Ответ: "+value2)
                                if value1 == messager:
                                    send_message(peer_id, value2)
                                    print("сообщение отправлено")
                                    break
                            time.sleep(1)

    print("CHECK MES END")




def editchatname(_ids, _mes):
    date_days = datetime.date.today()

    api_url = 'https://api.vk.com/method/messages.getChat'
    params = {
        'chat_id': _ids,
        'access_token': access_token,
        'v': '5.154'
    }

    api_url = 'https://api.vk.com/method/messages.getChat'
    params = {
        'chat_id': _ids,
        'access_token': access_token,
        'v': '5.154'
    }
    response = requests.get(api_url, params=params)
    data = response.json()

    if 'response' in data:
        chat = data['response']
        Current_NameBes = chat['title']
        print("Имя беседы:", Current_NameBes)
    else:
        print("Не удалось получить информацию о беседе")
        Current_NameBes = "ssss"



    if (date_days.weekday() == Day_Nedeli_Count):
        if _mes == "":
            _mes=NameGroupStr

        if "(Знаменатель)" in Current_NameBes:
            _mes = str(str(_mes) + " (Числитель)")
            print("Числитель")
        elif ("(Числитель)" in Current_NameBes):
            _mes = str(str(_mes) + " (Знаменатель)")
            print("Знаменатель")
        else:
            _mes = str(str(_mes) + " (Знаменатель)")
            print("Знаменатель2")

        api_url = 'https://api.vk.com/method/messages.editChat'
        params = {
            'chat_id': _ids,
            'title': _mes,
            'access_token': access_token,
            'v': '5.154'
        }
        response = requests.post(api_url, params=params)


def main():
    print("GOVNO")


    # vk.api.messages.editChat()

    t2 = Thread(target=editchatname(Chat_Send_Id,""))
    t2.start()
    t1 = Thread(target=check_mes)
    t1.start()

    # fullname=str(input("ENTER: "))
    # send_message(dryna_chat_send,fullname)

    input()


if __name__ == '__main__':
    main()