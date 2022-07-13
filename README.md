
<div style="margin:0 0 128px 0;">
    <p align="center" style="border-bottom:0px;padding:9px 0 0 0;"> [ 1.0.0 27/April/2022 ] </p>
    <h1 align="center" style="margin-bottom:64px;border-bottom:0px;"> Overlord </h1>
</div>

## Welcome to the Overlord framework!

**This is not a new JavaScript Framework!** and we aren't reinventing the wheel on the server either.

So, what is Overlord?

**Overlord is the worlds most extensive full stack framework** which majorly streamlines development by utilizing a
single code base (Python & JavaScript) for Desktop, Android and iOS applications. Also offering an optional package
called E-Panel which provides you with pop up software & server infrastructure or the ability to deploy from your own
virtual or physical server. All ready to go with a single command.

The server will host a Python-Django based API and serve a React-Native-Web application to any web browsers that attempt
to visit it.

By default your administration panel and content-management-system interface is `E Panel` and can be accessed by going
to the `/e_panel` route for your app in a web browser.

Your React-Native based application is deployable to Android & iOS through their respective dedicated app stores.

Also includes:

- Additional built in Libraries
- Lots of free UI Components & Templates
- Code sharing across all your apps/clients/servers
- CLI tools /w integrations for administrating your Dev, Lab, Staging or Production servers remotely)
- Single code base support for Desktop (via the web browser), native Android and native iOS
- Android Phone Emulator with all your overlord clients pre-installed available for Linux & Windows Users
- iOS Phone Emulator with all your overlord clients pre-installed available for Apple M1 Users
- Remote device testing tool for QA testing on iOS or Android if your development station does not support emulation
- Hot reloading when editing code while emulating devices simultaneously
- User registration, login, logout, profile features
- Optional administration panel app

...and everything else you will ever need, but we will get to that later.


## Overlord Tools
#### [Read More](https://github.com/EasterCompany/Overlord/blob/main/tools)

Overlord-Tools is a single CLI interface to interact with our 'Custom Django Backend' ready to deploy alongside any
number of React-Native based clients (built in PWA, Android & iOS support) locally on our development computers and also
remotely control the production versions of the clients you have installed.

You can access Overlord-Tools via the `o` file in your root directory. The generic input format when using the `./o`
file is usually like this

```bash
./o command -arg1 -arg2
```

If you would like to isolate a terminal window to Overlord run an empty command line like this:

```bash
./o
```

And you'll no longer need to include `./o` at the beginning of each command line.


### Setup a local Server

...

## Overlord Clients
#### [Read More](https://github.com/EasterCompany/Overlord/tree/main/clients)

...
