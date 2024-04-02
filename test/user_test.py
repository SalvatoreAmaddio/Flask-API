from app.routes.user import register, login


new_user = {
"email":"salvatore@gmail.com",
"password": "ciao_salvo"
}

#print(register(new_user))


login_dict = {
"email": "guest@xandertalent.com",
"password": "Welcome_to_this_assessment01"
}

#print(login(login_dict))
