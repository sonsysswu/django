from django import forms
from .models import CustomUser,Todo,GuestbookEntry, Post


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password check', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('id','name','email','major','nickname','phone_number')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserProfileUpdateForm(forms.ModelForm):
   class Meta:
        model = CustomUser
        fields = [ 'nickname','major', 'profile_pic','hobby', 'address']
        widgets = {
            'profile_pic': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class GuestbookForm(forms.ModelForm):
    class Meta:
        model= GuestbookEntry
        fields=['name','message','guest_password']

class TodoForm(forms.ModelForm):
    class Meta:
        model= Todo
        fields=['text']
        widgets={
            'completed':forms.CheckboxInput()
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields=['title', 'content'] 
        widgets={
            'secret': forms.CheckboxInput(),
            # 'secret': forms.CheckboxInput(attrs={'id': 'secret_checkbox'}),
            # 'password': forms.PasswordInput(attrs={'style': 'display:none;', 'id': 'password_input'})
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PostForm, self).__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['nickname'] = forms.CharField(max_length=10, widget=forms.HiddenInput, initial=user.nickname)
        # self.fields['password'].label = '비밀번호'
        