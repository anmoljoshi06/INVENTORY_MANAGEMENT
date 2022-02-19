# Zenatix-Assignment
Test assignment for zenatix
STEPS FOR STARTING THE APP-
1.) Download the project From git
2.) After Downloading go to ZENATIX.zanatix folder and open cmd there
3.) Also Open Settings.py file on ZENATIX/zenatix folder in an editor. Search Key word "DATABASES" and enter the database details according to your systems MYSQL database (all details are intuitive)
4.) Save settings.py and again come to the previously opened cmd
5.) Type command "python manage.py makemigrations"
6.) Type command "python manage.py migrate"
7.) Type command "python manage.py createsuperuser". You will be asked few details enter them by pressing enter at after each entry("username" , "email","password")
Note- The above step is to create an admin
8.) Now finally type the command "python manage.py runserver" to start the app . In your browser got to "http://127.0.0.1:8000.doc" to refer for api Documentation to start using APIS

