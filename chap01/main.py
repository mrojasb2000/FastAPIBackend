from typing import Optional, List, Dict
from uuid import UUID
from random import Random
from bcrypt import hashpw, gensalt, checkpw

from fastapi import FastAPI

app = FastAPI()


@app.get("/ch01/index")
def index():
    """Function index"""
    return {"message": "Welcome FastAPI Nerds"}


@app.get("/ch01/login/")
def login(username: str, password: str):
    """Function login user"""
    if valid_users.get(username) is None:
        return {"message": "user does not exist"}
    else:
        user = valid_users.get(username)
        if checkpw(password.encode(), user.passphrse.encode()):
            return user
        else:
            return {"message": "invalid user"}


@app.post("/ch01/login/signup")
def signup(uname: str, passwrd: str):
    """Function signup user"""
    if uname is None and passwrd is None:
        return {"message": "invalid user"}
    elif not valid_users.get(uname) is None:
        return {"message": "user exist"}
    else:
        user = User(username=uname, password=passwrd)
        pending_users[uname] = user
        return user


@app.put("/ch01/account/profile/update/{username}")
def update_profile(username: str, id: UUID, new_profile: UserProfile):
    """Function update profile user"""
    if valid_users.get(username) is None:
        return {"message": "user does not exist"}
    else:
        user = valid_users.get(username)
        if user.id == id:
            valid_profiles[username] = new_profile
            return {"message": "successfully updated"}
        else:
            return {"message": "user does not exist"}


@app.delete("/ch01/login/remove/all")
def delete_users(usernames: List[str]):
    """Function delete all users"""
    for user in usernames:
        del valid_users[user]
    return {"message": "deleted users"}


@app.patch("/ch01/account/profile/update/names/{username}")
def update_profile_names(username: str, id: UUID, new_names: dict[str, str]):
    """Function patch profile user"""
    if valid_users.get(username) is None:
        return {"messsage": "user does not exxist"}
    elif new_names is None:
        return {"messsage": "new names are required"}
    else:
        user = valid_users.get(username)
        if user.id == id:
            profile = valid_profiles[username]
            profile.firstname = new_names["fname"]
            profile.lastname = new_names["lname"]
            profile.middle_initial = new_names["mi"]
            valid_profiles[username] = profile
            return {"message": "successfully updated"}
        else:
            return {"messsage": "user does not exist"}


@app.delete("/ch01/discussion/posts/remove/{username}")
def delete_discussion(username: str, id: UUID):
    """Function update delete post by user"""
    if valid_users.get(username) is None:
        return {"message": "user does not exist"}
    elif discussion_posts.get(id) is None:
        return {"message": "post does not exist"}
    else:
        del discussion_posts[id]
        return {"message": "main post deleted"}


@app.delete("/ch01/login/remove/{username}")
def delete_user(username: str):
    """Function delete user"""
    if username is None:
        return {"message": "invalid user"}
    else:
        del valid_users[username]
        return {"message": "deleted user"}


@app.get("/ch01/login/details/info")
def login_info():
    """Function login info"""
    return {"message": "username and password are needed"}


@app.get("ch01/login/{username}/{password}")
def login_with_token(username: str, password: str, id: UUID):
    """Function login with token"""
    if valid_users.get(username) is None:
        return {"message": "user does not exis"}
    else:
        user = valid_users[username]
        if user.id == id and checkpw(password.encode(), user.passphrse):
            return user
        else:
            return {"message": "invalid user"}


@app.get("/ch01/delete/users/pending")
def delete_pending_users(accounts: List[str] = []):
    """Function delete pending users"""
    for user in accounts:
        del pending_users[user]
    return {"message": "delete pending users"}


@app.get("/ch01/login/password/change")
def change_password(username: str, old_passwd: str = "", new_passwd: str = ""):
    passwd_len = 8
    r = Random()
    if valid_users.get(username) is None:
        return {"message": "user does not exis"}
    elif old_passwd == "" or new_passwd == "":
        characters = ascii_lowercase
        temporary_passwd = "".join(r.choice(characters) for i in range(passwd_len))
        user = valid_users.get(username)
        user.password = temporary_passwd
        user.passphrse = hashpw(temporary_passwd.encode(), gensalt())
        return user
    else:
        user = valid_users.get(username)
        if user.password == old_passwd:
            user.password = new_passwd
            user.passphrse = hashpw(new_passwd.encode(), gensalt())
            return user
        else:
            return {"message": "invalid user"}


@app.post("/ch01/login/username/unlock")
def unlock_username(id: Opetional[UUID] = None):
    if id is None:
        return {"message": "token needed"}
    else:
        for key, val in valid_users.items():
            if val.id == id:
                return {"username": "val.username"}
        return {"message": "user does not exist"}


@app.ppost("/ch01/login/password/unlock")
def unlock_password(username: Optional[str] = None, id: Optional[UUID] = None):
    if username is None:
        return {"message": "username is required"}
    elif valid_users.get(username) is None:
        return {"message": "user does not exist"}
    else:
        if id is None:
            return {"message": "token needed"}
        else:
            user = valid_users.get(username)
            if user.id == id:
                return {"password": "user.password"}
            else:
                return {"message": "invalid token"}
