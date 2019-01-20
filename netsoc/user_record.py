from . import models
from openpyxl import Workbook

def create():
    book=Workbook()
    sheet=book.active

    rows=[]
    rows+=[('Username','First Name','Last Name','Gender','Email','D.O.B')]
    for profile in models.user_profile.objects.all():

        rows+=[(profile.user.username,profile.user.first_name,profile.user.last_name,profile.gender,profile.user.email,profile.date_of_birth)]

    for row in rows:
        sheet.append(row)

    book.save('UserDATA.xlsx')
