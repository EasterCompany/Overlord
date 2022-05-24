
<div style="margin:0 0 128px 0;">
    <p align="center" style="border-bottom:0px;padding:9px 0 0 0;"> [ 1.0.0 27/April/2022 ] </p>
    <h1 align="center" style="margin-bottom:64px;border-bottom:0px;"> Overlord </h1>
</div>


### Description

Overlord is a pre-configured Django Backend ready to be deployed from the moment you pull the repo. Using Overlord-Tools (A CLI for developers) we can generate a template React application based on Create-React-App with all the nescessery requirements for our Front End Applications.


With a single Overlord server we can host many front end applications across the web. This is the beuty of Overlord.


### Overlord Tools


You can access Overlord-Tools via the `o` file in your root directory. If this file is missing you can run the following command to reinstall it.

```bash
python run.py tools install
```

or access tools directly like such

```bash
python run.py tools [insert_command_and_arguments_here]
```

or preferably install using the first command and then just use the `o file` from there on

```bash
./o command -arg1 -arg2
```


Overlord is designed with a core developer philosophy. Where most projects designed to be built with Overlord are developed by a single person - and using our automated git tools you'll find working with Overlord takes a lot of mundane day-to-day tasks out of your life completely.


For example; we can automate `git add . && git commit -am "insert meaningful message here" && git push origin master` into the following OLT command:

```bash
./o commit -all -"100% optional message argument"
```

isn't that just glorious. And that's only scratching the surface. Read OLT (Overlord-Tools) documentation for more on commands and automation.


### Overlord Clients

As of release 1.0; we only support a single React-PWA client option. We will soon transition to supporting React-Native for mobile & web development under one solution and then coming in release 2.0 we will support an Angular web client option.

To generate a React-PWA client template in the `clients` directory just run `./o create -app_name_here`

And everything will be taken care of for you.


### Routes

Django provides a routing system - however traditional routing systems as essential as they are, are not as good as something like React-Router for developing modern web applications inside the browser.

Overlord handles this by overiding all the routing systems in Django with a new method which provides a parent route for the client and then all children of that route are handled by the React-Router within that application.


### ORM

Django's ORM is lovely. Who doesn't enjoy using it over the alternatives. A lot of Django projects are exclusively django-based because of the ORM.
So... that's why we built Overlord on-top of Django.

Simple.


### PA Integrations

We have full integration with www.pythonanywhere.com services. Which means we have the worlds-best CI/CD pipeline you'll ever get to use.
Everything you need is automated and perfected by simply running `./o deploy` from Overlord-Tools.

Read OLT Documentation for more information on PA Integrations and deployment automation.
