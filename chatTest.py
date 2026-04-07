from requests import request, RequestException
import os
import time
import threading
import sys
from queue import Queue

url = "http://127.0.0.1:8000/"
chosenChat = None

# دالة لجلب الرسائل
def fetch_chats(chats, num, result_queue):
    """
    Makes a GET request to the given URL every second.
    :param chats: The list of chats.
    :param num: The index of the chat to fetch.
    :param result_queue: The queue to pass the result to the main thread.
    """
    global chosenChat
    start_time = time.time()
    last_time = start_time

    while True:
        current_time = time.time()
        if current_time - last_time >= 1:
            try:
                response = request(
                    method='get',
                    url=url + f"/messages/{chats[num-1]['id']}",
                    headers={}
                )
                chosenChat = response.json()  # تحديث المتغير global chosenChat
                result_queue.put(chosenChat)  # وضع النتيجة في الـ Queue
                #print(f"Status Code: {response.status_code}, Response: {response.text[:100]}")
            except RequestException as e:
                print(f"Request failed: {e}")
            last_time = current_time
        if chosenChat:  # إذا تم استلام البيانات، نخرج من الحلقة
            break

# دالة لإرسال الرسالة
def send_msg():
    m = input("Enter a message: ")
    request(
        method='POST',
        url=url + f"/messages/create",
        headers={},
        json={
            "chat_id": chats[num-1]['id'],
            "sender": userInfo['id'],
            "receiver": rUser['id'],
            "body": f"{m}"
        }
    )

# ملف تعريف المستخدم والمحادثات
while True:
    username = "muatz"
    password = "1111"
    login_res = request(
        method="POST",
        url=url + "users/login",
        headers={},
        json={"name": f"{username}", "password": f"{password}"},
    )
    if login_res.status_code != 200:
        print("Login Failed. Try Again")
    else:
        break

access_token = login_res.json().get("access_token")
me = request(
    method="get",
    url=url + "/users/me",
    headers={"Authorization": f"Bearer {access_token}"}
)

userInfo = me.json().get("user")

print(f"""
    Welcome in The Best App Chat Ever :)
                User ID: {userInfo['id']}
                User Name: {userInfo['name']}
                User Chats:
""")

while True:
    print("""
                Actions: 
        1: Message Friend
        2: Add Friend
        """)

    c = input("Choose Action: ")

    if c == '2':
        inputId = int(input("Enter your friend ID: "))
        verifyUser = request(method='get', url=url + f"/users/user/{inputId}")
        while verifyUser.json().get('id') != inputId:
            print("No Users. Try Again")
            inputId = input("Enter your friend ID: ")
            verifyUser = request(method='get', url=url + f"/users/user/{inputId}")

        newChat = request(
            method="post",
            url=url + "/chats/create",
            json={
                "user1_id": userInfo['id'],
                "user2_id": inputId
            }
        )
        if newChat.json():
            print("New Friend ", verifyUser.json().get('name'))
        else:
            print("No Such User or Already Friend")

    if c == '1':
        chatsReq = request(
            method="get",
            url=url + f"/chats/all/{userInfo['id']}",
            headers={},
        )
        chats = chatsReq.json()
        i = 1
        rUser = 0
        for chat in chats:
            if userInfo['id'] == chat['user1_id']:
                chatuser = request(method="get", url=url + f"/users/user/{chat['user2_id']}")
            elif userInfo['id'] == chat['user2_id']:
                chatuser = request(method="get", url=url + f"/users/user/{chat['user1_id']}")
            rUser = chatuser.json()
            chatuser = chatuser.json().get('name')
            print(f"                {i} ->   {chatuser}")
            i += 1
        num = int(input("Choose Chat to Start: "))

        while num > i or num < 0:
            print("Invalid input!!\n")
            num = int(input("Choose Chat to Start: "))

        while True:
            # إنشاء Queue لمشاركة البيانات بين الخيوط
            result_queue = Queue()

            # بدء الخيط الأول لجلب الرسائل
            t1 = threading.Thread(target=fetch_chats, args=(chats, num, result_queue))
            t1.start()

            # بدء الخيط الثاني لإرسال الرسالة
            t2 = threading.Thread(target=send_msg)
            t2.start()

            # انتظار حتى تنتهي عملية جلب الرسائل وتحديث chosenChat
            t1.join()

            # الحصول على البيانات من الـ Queue
            chosenChat = result_queue.get()

            # معالجة الرسائل
            finalChat = chosenChat
            for message in finalChat:
                chatuser = request(method="get", url=url + f"/users/user/{message['sender']}")
                print(f"{message['body']} ---> {chatuser.json().get('name')}")

            # انتظار الخيط الثاني لإرسال الرسالة
            t2.join()
            os.system('cls')
