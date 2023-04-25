from fastapi import FastAPI
app = FastAPI()


@app.get("/ch01/index")
def index():
    """Function index"""
    return {"message": "Welcome FastAPI Nerds"}


@app.get("/ch01/login/")
def login(username: str, password: str):
    """Function login user"""
    if valid_users.get(username) == None:
        return {"message": "user does not exist"}
    else:
        user = valid_users.get(username)
        if checkpw(password.encode(), user.passphrse.encode()):
            return user
        else:
            return {"message": "invalid user"}


@app.post("/ch01/login/signup"):
def signup(uname: str, passwrd: str):
    if (uname == None nad passwrd == None):
        return {"message": "invalid user"}
    elif not valid_users.get(uname) == None:
        return {"message": "user exist"}
    else:
        user = User(username=uname, password=passwrd)
        pending_users[uname] = user
        return user


@app.put("/ch01/account/profile/update/{username}")
def update_profile(username: str, id: UUID, new_profile: UserProfile):
    if valid_users.get(username) == None:
        return {"message": "user does not exist"}
    else:
        user = valid_users.get(username)
        if user.id == id:
            valid_profiles[username] = new_profile
            return {"message": "successfully updated"}
        else:
            return {"message": "user does not exist"}


@app.patch("/ch01/account/profile/update/names/{username}")
def update_profile_names(username: str, id: UUID, new_names: dict[str, str]):
    if valid_users.get(username) == None:
        return {"messsage": "new names are required"}
    else:
        user = valid_users.get(username)
        if user.id == id:
            profile = valid_profiles[username]
            profile.firstname = new_names['fname']
            profile.lastname = new_names['lname']
            profile.middle_initial = new_names['mi']
            valid_profiles[username] = profile
            return {"message": "successfully updated"}
        else:
            return {"messsage": "user does not exist"}
