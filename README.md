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
This is a single flaw but is located in two files:
[urls.py](https://github.com/Tharmat/hy-cybersecurity-project/blob/master/polls/urls.py#L12)
[views.py](https://github.com/Tharmat/hy-cybersecurity-project/blob/master/polls/views.py#L80)

Injection flaws and attacks can be defined as cases where untrusted (user) data is processed unsanitized as part of a request/command/query by an interpreter of some sort. The classic example of this is SQL injections. In SQL injection, user input is processed unsanitised or as non-parametrized raw sql. In the worst case, the SQL is then executed with the system's priviledges leading to credential compromise, data loss or worse. 

For example, this application contains a search box that allows the user to search for specific text in all the existing polls. Instead of using the Django's safe default implementation SearchResultView for search, it has a custom view that uses string concatenation along with raw sql query to do the same thing. This flaw can be tested by pasting the following  search string (asdf' union select password from Users where admin like '%1) in to the search text box. If DEBUG = True in settings.py, it shows that it tries to process the search term as an unsanitized SQL statement, but ends in an error because no table Users exists. If the debug mode is disabled, the server reports 500 error which can indicate to the attacker that the program is subject to an SQL injection.

This problem can be fixed by using Django's SearchResultView implementation that uses parametrized sql. To fix this application [urls.py](https://github.com/Tharmat/hy-cybersecurity-project/blob/master/polls/urls.py#L12) needs to be modified by commenting line 19 and uncommenting line 20. This makes the application use the safe implementation instead of the insecure custom one. 

## Flaw #3: Security Misconfiguration
The flaw is located in [settings.py](https://github.com/Tharmat/hy-cybersecurity-project/blob/master/mysite/settings.py#L22)

Security misconfigurations can be described as any configuration that decreases the overall security of an application. Most software like Django come with sane default configuration, but this cannot be taken as given. If publishing this application in a public repository can be considered "putting the software into production", then the software contain two distinct security misconfigurations. First, it still runs in debug mode, even though even the default configuration file explicitly tolds in ALL CAPS that this should not be done in production. The most obvious indication why this is a security problems is with the Flaw #2's SQL injection: with the debug-mode enabled, the attacker can see that the SQL is executed as is and even given an helpful error message. Without the debug mode, there's only a 500 Server Error which still can indicate there's an SQL injection opportunity, but this information requires a bit more sleuthing. In general, showing internal error messages to user can allow the attacker to atleast gather more information about the internal working of the software. Secondly, the application stores its secret key in the settings.py instead of being read from a separate env-file. Thus the secret key is also included in the git repo and available publicly and is not _secret_.

To fix these issues, the configuration should be changes so that 1) debug mode is disabled (which also requires updating ALLOWED_HOSTS) and 2) the secret key is read using an env-file (for example, by using python-dotenv package).

## Flaw #4: Security Logging and Monitoring Failures
The flaw is located in [settings.py](https://github.com/Tharmat/hy-cybersecurity-project/blob/master/mysite/settings.py#L140)

By default, Django runs in debug mode and logs a lot of stuff to console. If and when you disable the debug mode, the [default](https://docs.djangoproject.com/en/5.1/ref/logging/#django-s-default-logging-configuration)) is that only django.* messages of ERROR or CRITICAL level are logged to AdminEmailHandler, not to a file. Thus running the default logging in non-debug mode can be considered a logging failure or a flaw as there might not be enough logs to monitor and investigate potential security incidents. This application has this fixed by implementing a barebones _security logging_ that logs both security.DisallowedHost and security.csrf to a separate security.log file. This can be tested by:
1. Changing DEBUG to False in settings.py -> This both removes localhost from the default allowed hosts, as well as disables the default debug logging
2. Including a random hostname that is not localhost in ALLOWED_HOSTS in settings.py. For example, uncomment the example setting in [settings.py](https://github.com/Tharmat/hy-cybersecurity-project/blob/master/mysite/settings.py#L43)
3. Try to access the app. The connection is refused and the connection attempt is logged to the security.log file.

## Flaw #5: Cross-Site Scripting (XSS)


