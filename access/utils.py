from django.contrib.auth.models import User


def process_account_request(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password_check = request.POST['password_check']

    # check that all fields have been filled out
    if (username == '' or email == '' or password == '' or \
        passwordcheck == ''):    
        errors.append('Please fill out all fields.\n')
    
    # check that password and password_check match
    if password != password_check: 
        errors.append('The passwords you supplied did not match.\n')        
    
    # check that username is not already in use
    usernames = []
    users = User.objects.all()
    for user in users:
        usernames.append(user.username)
    if username in usernames:
        errors.append('That username is already in use. Please choose a different username.\n')
    
    # check that username is valid
        
    # check that email address is in a valid format
        
#    errors.append('Invalid email address. Please re-enter.\n'
    
    # check that password is long enough
        
#    errors.append('You password was not long enough. Please use a password at least 10 characters long.\n'
    
       
       
        
    if errors == '':
        create_user(username, email, password)
        return 'success'
    else:
        return errors
