
<div style="margin:0 0 128px 0;">
    <p align="center" style="border-bottom:0px;padding:9px 0 0 0;"> [ 1.0.0 27/April/2022 ] </p>
    <h1 align="center" style="margin-bottom:64px;border-bottom:0px;"> Overlord </h1>
</div>

## Welcome to the Overlord framework!

**This is not a new JavaScript Framework!** and we aren't reinventing the wheel on the back end either.

So, what is Overlord?

Overlord is the worlds most extensive **full stack framework** which majorily streamlines development by utilizing a single code base (Python & JavaScript) for Desktop, Android and iOS applications. Also offering an optional package called E-Panel which provides you with pop up software & server infrastructure or the ability to deploy from your own virtual or physical server. All ready to go with a single command.

The server will host a Python-Django based API and serve a React-Native-Web application to any web browsers that attempt to visit it. By default this is your administration panel app `E-Panel`.

Your React-Native based application is deployable to Android & iOS through their respective dedicated app stores.

Also includes: 

- Additional built in Libraries
- Lots of free UI Components
- A few free UI Templates
- Code sharing across all your apps/clients/servers
- Great CLI tools (including integrations for administrating your staging or produciton server remotely)
- Single code base support for Desktop (via the web browser), Native Android, Native iOS and potentially with a little tweaking on your part... probably anything else.
- Android Phone Emulator with all your overlord clients pre-installed
- iOS Phone Emulator with all your overlord clients pre-installed
- Hot reloading when editing code and emulator simaltaneously
- User registration, login, logout, profile features
- Optional administration panel app

...and everything else you will ever need, but we will get to that later.


## Overlord Tools
#### [Read More](https://github.com/EasterCompany/Overlord/blob/main/tools)

Overlord-Tools is a single CLI interface to interact with our 'Custom Django Backend' ready to deploy alongside any number of React-Native based clients (built in PWA, Android & iOS support) locally on our development computers and also remotely control the production versions of the clients you have installed.

You can access Overlord-Tools via the `o` file in your root directory. If you don't have this file or this file is missing you can run the following command to (re)install it.

```bash
python run.py tools install
```

or access tools directly like such

```bash
python run.py tools [insert command and arguments here]
```

The generic input format when using the `./o` file is usually like this

```bash
./o command -arg1 -arg2
```

### Setup a local Server




## Overlord Clients
#### [Read More](https://github.com/EasterCompany/Overlord/tree/main/clients)


