from requests import request
import os


url = "http://127.0.0.1:8000/"

while True:
    username = input("User Name: ")
    password = input("PassWord: ")

    login_res = request (
        method="POST",
        url= url+"users/login",
        headers= {},
        json= {"name":f"{username}","password":f"{password}"},
    )
    if login_res.status_code != 200:
        print("Login Failed Try Again")
    else:
        break

access_token = login_res.json().get("access_token")
# print(access_token)

me = request(
    method="get",
    url = url + "/users/me",
    headers={"Authorization": f"Bearer {access_token}"}
)


userInfo = me.json().get("user")
#print(userInfo)



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

    c = input("Chosse Action: ")

    if c == '2': 
        inputId = int(input("Entar you friend ID: "))
        verifyUser = request(method='get', url = url + f"/users/user/{inputId}")
        while verifyUser.json().get('id') != inputId:
            print("No Users Try Again")
            inputId = input("Entar you friend ID: ")
            verifyUser = request(method='get', url = url + f"/users/user/{inputId}")
        
        newChat = request(
            method="post",
            url = url + "/chats/create",
            headers={"Authorization": f"Bearer {access_token}"},
            json = {
                "user1_id": userInfo['id'],
                "user2_id": inputId
            }
        )
        if newChat.json():
            print("New Frined ", verifyUser.json().get('name'))
        else:
            print("No Such User or Already Friend")

    if c == '1':
        chatsReq = request(
            method="get",
            url = url + f"/chats/all/{userInfo['id']}",
            headers={},
        )
        chats = chatsReq.json()
        i = 1
        rUser = 0
        for chat in chats:
            if userInfo['id'] == chat['user1_id']:
                chatuser = request(method="get",url=url+ f"/users/user/{chat['user2_id']}",headers={"Authorization": f"Bearer {access_token}"})
            elif userInfo['id'] == chat['user2_id']:
                chatuser = request(method="get",url=url+ f"/users/user/{chat['user1_id']}",headers={"Authorization": f"Bearer {access_token}"})
            rUser = chatuser.json()
            chatuser = chatuser.json().get('name')
            print(f"                {i} ->   {chatuser}")
            i += 1
        num = int(input("Chosse Chat to Start: "))

        while num > i or num < 0:
            print("Invaild input !!\n")
            num = int(input("Chosse Chat to Start: "))

        while True:

            chosenChat = request(
                method='get',
                url= url + f"/messages/{chats[num-1]['id']}",
                headers={"Authorization": f"Bearer {access_token}"},
            )

            finalChat = chosenChat.json()

            for message in finalChat:
                chatuser = request(method="get",url=url+ f"/users/user/{message['sender']}",headers={"Authorization": f"Bearer {access_token}"})
                print(f"{message['body']} ---> {chatuser.json().get('name')}")


            m = input("Entar a Massage: ")
            send = request(
                method='POST',
                url= url + f"/messages/create",
                headers={"Authorization": f"Bearer {access_token}"},
                json= {
                    "chat_id": chats[num-1]['id'],
                    "sender": userInfo['id'],
                    "receiver": rUser['id'],
                    "body": f"{m}"
                }
            )
            os.system('cls')

