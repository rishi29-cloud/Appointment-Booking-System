# Appointment Booking System 

This is an application where a patient can book an appointment with the doctor on a particular day and at a particular time. 

# Tasks Accomplished: 
1) Patient can see the list of all the doctors to book the appointment.
2) Doctor's Profile has the profile picture, name and book appointment button.
3) A form is displayed when the patient clicks on book appointment with required inputs.
4) After the patient confirms to book an appointment, a calendar event is created using the GOOGLE CALENDAR API. 
5) After confirmation, the patient can see the respective appointment details.
6) GOOGLE CALENDAR API has been used for creating the events.

# Tech Stack Used:
Django Framework - Python (Backend)

HTML, CSS and Bootstrap, Javascript (Frontend)

MySQL (Database)


# Technical Requirements: 
Used Google Calendar API for creating the appointment events.

<img width="750" alt="image" src="https://user-images.githubusercontent.com/83284855/173996917-c49a2900-b881-417d-93a6-e0b5f6d1753e.png">


# Libraries that need to be installed: 
django: pip install django

mysqlclient: pip install mysqlclient

calendar API: pip install google-api-python-client 

# To start the server and view the website
Step 1: Run python manage.py runserver

Step 2: Go to the Browser and enter http://127.0.0.1:8000/


# Screenshots of the application:

1) Home Page: 

<img width="750" alt="image" src="https://user-images.githubusercontent.com/83284855/172517373-ca37a776-b66c-4782-9e87-5dcde5e2f118.png">

<br>
<br>
2) Page to select the doctor and book the appointment: 

This displays the list of all the doctors that are present for booking.

<img width="750" alt="image" src="https://user-images.githubusercontent.com/83284855/174001198-4d050adf-ca06-41b6-a220-67478a8433f8.png">

<br>
<br>

3) Form for booking the appointment: (User can enter the date and time when he/she wants the appointment)

<img width="750" alt="image" src="https://user-images.githubusercontent.com/83284855/174001401-6c680009-5762-4930-95e3-de16997bb2ed.png">

<br>
<br>

4) Page Showing all the appointments of the user: 

<img width="750" alt="image" src="https://user-images.githubusercontent.com/83284855/174001668-961418aa-1cb5-4506-abcc-8020e1115065.png">

