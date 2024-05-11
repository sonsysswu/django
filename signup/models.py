from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
#장고에서 기본적으로 제공해주는 유저 커스텀해서 만드는거

class UserManager(BaseUserManager):

    def create_user(self, id, name, email, major, nickname, phone_number ,password=None):

        if not id:
            raise ValueError('아이디좀 입력해주세요')
        user = self.model(
            id=id,
            name=name,
            email=self.normalize_email(email),
            major=major,
            nickname=nickname,
            phone_number = phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

#슈퍼유저 만드는거
    def create_superuser(self, id, name, email, major, nickname, phone_number, password):
        user = self.create_user(
            id=id,
            name=name,
            email=self.normalize_email(email),
            major=major,
            nickname=nickname,
            password=password,
            phone_number = phone_number,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    user_number = models.AutoField(primary_key=True)
    id = models.CharField(max_length=15, unique=True, null=False, blank=False)
    #중복방지 primary_key=True
    name = models.CharField(max_length=30)
    email = models.EmailField(default='', max_length=100, null=False, blank=False, unique=True)
    major = models.CharField(max_length=30)
    nickname = models.CharField(max_length=10, unique=True)
    phone_number = models.CharField(max_length=13)
    #아래 두개는 필수 필드라고 합니다!
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True)
    hobby = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)
    objects = UserManager() #위에서 정의한 헬퍼 클래스 불러와서 

    USERNAME_FIELD = 'id'
    #필수로 작성해야하는 필드 명시
    REQUIRED_FIELDS = ['email','nickname','name','phone_number']

    def __str__(self):
        return self.id

#admin페이지에서 오류 잡는 용도입니다
    @property
    def is_staff(self):
        return self.is_admin
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
class GuestbookEntry(models.Model):
    name= models.CharField(max_length=100)
    message= models.TextField()
    guest_password= models.CharField(max_length=15,default='admin')
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}-{self.created_at}'
    
class Todo(models.Model):
    # date=models.DateTimeField(auto_now=False, auto_now_add=False)
    text=models.TextField()
    completed = models.BooleanField(default=False)