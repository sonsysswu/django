from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class IdBackend(ModelBackend):
    def authenticate(self, request, id, password, **kwargs):
        user_model = get_user_model()
        #print(user_model)
        if id is None:
            id = kwargs.get(user_model.USERNAME_FIELD)
            
        try:
            #print(id)
            #print(password)
            user = user_model.objects.get(id = id)
            #print(user)
            #print(user.check_password(password))
            if user.check_password(password):
                print(user)
                return user  
        except user_model.DoesNotExist:
            print('None')
            return None