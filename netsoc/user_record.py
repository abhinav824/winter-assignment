from . import models
from openpyxl import Workbook

def create(queryset):
    book=Workbook()
    sheet=book.active

    rows=[]
    rows+=[('Username','First Name','Last Name','Gender','Email','D.O.B')]
    for user in queryset:
        profile=user.profile_user
        rows+=[(profile.user.username,profile.user.first_name,profile.user.last_name,profile.gender,profile.user.email,profile.date_of_birth)]

    for row in rows:
        sheet.append(row)

    book.save('netsoc/userdata/UserDATA.xlsx')

    with open('netsoc/userdata/UserDATA.xlsx','rb') as f:
        data=f.read()

    return data
