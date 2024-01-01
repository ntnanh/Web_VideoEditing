# from django import forms
# import re
# from .models import Users
# class SignupForm(forms.Form):
#     def clean_username(self):
#         username = self.cleaned_data['username']
#         if not re.search(r'^\w+&', username):
#             raise forms.ValidationError("Tên tài khoản có kí tự đặc biệt")
#         try:
#             Users.objects.get(username=username)
#         except Users.DoesNotExist:
#             return username
#         raise forms.ValidationError("Tài khoản đã tồn tại")
#     def save(self):
#         Users.objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'],
#         password=self.cleaned_data['password'])

