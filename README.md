# University of Helsinki Cyber Security MOOC Course Project 1
This is a repository for Cyber Security Project 1. The project is based on the example Django project as described in [Django documentation](https://docs.djangoproject.com/en/5.1/intro/tutorial01/)

It contains an example Django app with four flaws from [OWASP TOP10 2017 list](https://owasp.org/www-project-top-ten/2017/Top_10) as well as a CSRF flaw (as per course instructions).

## Installing and running the app
These instructions assume that you have Python3, Django etc. installed and that your python executable in the PATH-variable is named python. 
If, for some reason, you need to access the Django Admin panel you can use `admin:admin` as the username and password

1. Clone the repository
2. Read through the documentation describing the flaws and their fixes. Most of the flaws also have a example for testing out the flaw.
3. The repo contains a barebones SQLite db with the necessary data for testing. If for some reason this does not work run the following commands:
`python manage.py makemigrations`
`python manage.py migrate`
5. Run the app with `python manage.py runserver`
6. Navigate to `http://127.0.0.1:8000/polls/` to test the app.
7. Profit/enjoy
   
&nbsp;

# Security Flaws

## Flaw #1: Cross-Site Request Forgery (CSRF)
This is a single flaw, but is located in two files:
[views.py](https://github.com/Tharmat/hy-cybersecurity-project/blob/master/polls/views.py#L37)
[detail.html](https://github.com/Tharmat/hy-cybersecurity-project/blob/master/polls/templates/polls/detail.html#L6)

Cross-Site Request Forgery is an attack that tricks the users web browser to use existing user priviledges to execute a malicious request. In this attack, the user is already authenticated to a site A. 
He then visits compromised site B while still being logged in service A. The compromised site B contains code that makes the user's web browser to make a request to site A. As the user is already 
authenticated to the site A, it is considered legitimate - and the site cannot distinguish it from an illegimate request. In this way the malicious site can "force" the user to make a request, for example,
to change the email address.

More throughout description of CSRF attack can be found in OWASP [website](https://owasp.org/www-community/attacks/csrf).

Django contain's [built-in CSRF mitigations](https://docs.djangoproject.com/en/5.1/howto/csrf/) and they're enabled by default. The only thing required is to use  the tag `{% csrf_token %}` in any forms that
need CSRF protection.

In this software the [vote view](https://github.com/Tharmat/hy-cybersecurity-project/blob/master/polls/views.py#L37) is not protected by Django's CSRF protection as the [detail.html](https://github.com/Tharmat/hy-cybersecurity-project/blob/master/polls/templates/polls/detail.html#L6) is missing the `{% csrf_token %}` and the view is explicitly moved outside Django's default CSRF protections. This is a real flaw, but requires _explicitly making 
the software less secure_ so this is not very _realistic_. The problem can be fixed by inlcuding the csrf_token in the detail.html by uncommenting the [relevant part](https://github.com/Tharmat/hy-cybersecurity-project/blob/master/polls/templates/polls/detail.html#L8) and re-enabling the CSRF protection by commenting the `@csrf_exempt` [line](https://github.com/Tharmat/hy-cybersecurity-project/blob/master/polls/views.py#L42).

## Flaw #2: Injection
## Flaw #3: Security Misconfiguration
## Flaw #4: Security Logging and Monitoring Failures
## Flaw #5: Cross-Site Scripting (XSS)


