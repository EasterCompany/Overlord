
<div style="margin:0 0 128px 0;">
    <p align="center" style="border-bottom:0px;padding:9px 0 0 0;"> [ 1.0.0 27/April/2022 ] </p>
    <h1 align="center" style="margin-bottom:64px;border-bottom:0px;"> Developer Tools </h1>
</div>

## Introduction

This an open source developer tools package by Easter Company for automating the development, testing & deployment
processes for use with *Overlord* on *Linux* hosted with *PythonAnywhere*, version controlled by *Git* and designed with
a methodology to highly emphasizing *Code Reuse & Extensibility* between all of your internal Overlord repositories.

**STAGING**: [eastercompany.eu](https://eastercompany.eu.pythonanywhere.com/)

**PRODUCTION**: [easter.company](https://www.easter.company/)

Some features may be specific to our development & hosting solutions but most will be useful to all developers
regardless of your methods as long as you're using Overlord.

## Installation

Install the `o script` (Overlord Script) file by running `run.py` on your projects targeted python executable and use
the following command.

```bash
python run.py tools install
```

A file named `o` will appear in your current working directory. Which should be the same as where your `run.py` file
is located. The `o script` file will allow you to run `tools` directly from your command line.

```bash
./o [arg 1] [arg 2] [arg 3] ...etc
```

This file should be ignored by your .gitignore file because it will hard-code a path to your selected python executable
on your machine which you intend to use for your project, which maybe different for each developer, or machine.

If you need to update your `o script` file you can run the above command again or use the following command.

```bash
./o install
```

The install command with also set the up-stream origins of your `dev (development)` and `main (production)` branch to
the appropriate origin for each branch `dev -> dev` and `main -> main`. You should not need to change this setting.

**WARNING** installing or re-installing Overlord-Tools will break your environment configuration settings by replacing
them with the default settings and you will be required to re-add your `PythonAnywhere API Key` and any other secrets to
your `./.config/secret.json` file.

## Clients

Using the clients argument you can install all of your clients currently within the `clients` directory automatically.

```bash
./o install -clients
```

Or you can specifically install a single client with the following command

```bash
./o install -clients -"client_name_here"
```

## Pulling Changes

Pull all of the latest changes from your repository including any changes to the submodules contained within and with
the following command:

```bash
./o update
```

## Changing Branches

You can switch between the `main` (production) branch and the `dev` (development) branch for all your repositories and
submodules with a single command.

To switch all your repositories to the production branch.

```bash
./o main
```

Or switch all your repositories to the development branch.

```bash
./o dev
```

**WARNING** changing branches is not a recommended practice; Instead you should clone the `main (production)` branch to
one directory and then clone the `dev (development)` branch to another directory. Only modify the `dev` branch and then
merge `dev -> main` on a regular release schedule.

## Committing Changes

Commit your changes to a repository with a message where `repo` is the name of the repository you are committing
ie; `tools`

```bash
./o commit -"repo" -"enter a meaningful message."
```

Here is an example of the above command for each of the possible repositories where `client` is the name of a client
submodule (ie; `pardoewray`) you have installed and `clients` is the clients directory (`submodule`).

```bash
./o commit -"{client_name}" -"fixed some bug"
./o commit -clients -"updated {client_name}"

./o commit -tools -"fixed some bug"
./o commit -server -"updated clients & tools"
```

You are not always required to use quotes around your arguments although if you want to use syntax from bash
commands inside your message string you will need to use quotes. For example; the `&` operator will cause errors without
surrounding the parameter in `"quotes"`.

**WARNING** when committing changes, all modified files will be automatically added to the commit similar to a
`git commit -am` command. This should be avoided if you wish to commit specific changes from your local environment and
instead a generic `git add` & `git commit -m` should be used on your target repository.

## Pushing Changes

When you are ready to push all your commits for both the parent & submodules repositories you can use the following:

```bash
./o push
```

If required you will need to enter a username & password for each repository that has been pushed. In-order to avoid
this we will only clone repositories and submodules from the `CLONE via SSH` command provided in the repositories README
file.

## Merging `dev -> main`

When you are ready to merge all your changes from the `dev (development)` branch into the `main (production)` branch for
any given repository you should use the following command:

```bash
./o merge -"repo" -"message"
```

Where `repo` is the name of the repository; using an identical structure to the `commit` command.

```bash
./o merge -"{client_name}" -"fixed some bug"
./o merge -clients -"updated {client_name}"

./o merge -tools -"added some feature"
./o merge -server -"updated clients & tools"
```

Or you can use the following command:

```bash
./o merge -all
```

To merge all the changes from the current `dev` branch into `main` and recursively merge all contained submodules `dev`
branches into their respective `main` branches.

**WARNING** it is important to keep the `dev` branch of a parent repository consistent with the `dev` branch of each
submodule contained within; as releases will be made on a scheduled basis and package all repositories together. This is
so that we can avoid conflicts in dependencies between new versions of software which may be reused within other
existing project repositories.

ie; The `Staging-Server` running `Overlord Release 2` should contain `Overlord-Tools Release 2` while
`Pardoewray-Server` running `Overlord Release 1` should only use `Overlord-Tools Release 1` respectively. While
`Staging-Server (dev)` on your local environment should only use `Overlord-Tools (dev)` as well.

<div style='margin:10% 0 5% 25%;'>
  <h1 align="center" style="color:lightgrey"> Basic Commands </h1>
</div>

## Unit Tests

To run *all unit tests* in your application use the following command:

```bash
./o test
```

## Run Development Mode

To run *all clients* in development mode with your development server use the following command:

```bash
./o run
```

The Django server will be running on `localhost:8000` while each react clients  will be running on their designated
ports. `localhost:3000` is the default setting however each client should have it's own port number assigned to it by
the `.env` file in the clients root directory.

**WARNING** this will begin to launch each installed client as a separate process, if you have many clients already
installed you may want to avoid this feature and refer to:
- [Run Django Server](#Run-Server)
- [Run React Client](#Run-Client)

## Start Production Mode

To test *any client* in production mode using your development server, try the following command:

```bash
./o start
```

- All unit tests will run in production mode before starting the server, and will exit on failure of any test.
- Migrations will be made and applied automatically upon successful execution of all tests.
- All clients will be built and optimized for production.
- Then the server will be started and will serve production API endpoints and production builds of any clients that are
already installed.

**WARNING** this operation may take quite a while to complete successfully and is not recommended for testing purposes,
instead you should prove that each individual client behaves as expected in development mode - then test your server in
standalone mode before attempting to run everything together in production mode.

<div style='margin:10% 0 5% 25%;'>
  <h1 align="center" style="color:lightgrey"> Django Tools </h1>
</div>

## New Django Secret Key

To generate a new Django secret key for your server, use the following command:

```bash
./o new_secret_key
```

A new secret will be generated in your `.config` directory within `secret.json` using the `SECRET_KEY` value. This will
only affect the environment this command is run on.

```JSON
{
  "SECRET_KEY": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  ...
}
```

## Database Migrations

To run your Django migrations (ie; `run.py makemigrations` & `run.py migrate`) just use:

```bash
./o migrate
```

This command does not usually need to be run manually - as migrations will be automatically handled when the Django
server is started. However just incase you are required to manually run migrations this command is available.

## Run Server

To run your Django server without any clients, use the following command:

```bash
./o runserver
```

This will start the Django Server on its own at `localhost:8000` serving the locally built versions of your `clients`.

<div style='margin:10% 0 5% 25%;'>
  <h1 align="center" style="color:lightgrey"> Client Tools </h1>
</div>

## Run Client

To run your react application in standalone development mode (without any server), use the following command:

```bash
./o runclient -"app name"
```

This will start the React Client on its own at `localhost:3000` by default or on which ever port is specified by the
`.env` file in it's root directory. Typically Overlord will automatically generate an `.env` file in the clients root
directory every time a client is loaded. However if Overlord is not running and no `.env` file exists then `3000` is the
redundant port.

You can also launch all your clients simultaneously in one command by doing the following:

```bash
./o runclient -all
```

**WARNING** be careful when running all clients in parallel as your browser will spawn a new tab in your browser for
each client and initially each one will boot-up sequentially.

## Create New Client

To create a new client from our TypeScript-PWA template, use the following command:

```bash
./o create -"app_name"
```

and a new client will appear in the `clients` directory ready for deployment.
The URL of the application will need to be added to your django configuration manually.

## Variable Meta Data

Overlord Tools uses variable meta data that is generated on each build of your client.
Variable meta data tags look like this: `{# meta_data #}`.

Here is a list of the all the currently supported variable meta data tags

| Tag                | Content               |
| ------------------ | --------------------- |
| time_of_last_build | %Y-%m-%dT%H:%M:%S     |

## Sharing Code

You can allow the sharing of source code across multiple clients & projects by using the `shared directory` & `share`
command.

```bash
./o share -"path" -"client_name"
```

For example; we have a file within the `clients/shared` directory `library/server/request` that we can share with a
client and keep it automatically updated by using the following command;

```bash
./o share -library/server/request.ts -"client_name"
```

Or we can share the entire `library/server` module by using the following command;

```bash
./o share -library/server -"client_name"
```

If a file contained with a shared module is already individually shared with a client, then the individual share rule
will be removed and the file will only be shared as part of the entire module.

A shared directory will appear inside the clients src directory with all shared modules appearing inside that folder,
and they will be updated to match the contents of the original file every time `OLT (Overlord Tools)` is started - so
whenever you run a client or server from `OLT` the new contents of that file or module will be automatically distributed
to your targeted clients.

<div style='margin:10% 0 5% 25%;'>
  <h1 align="center" style="color:lightgrey"> Server Tools </h1>
</div>

## General Usage

You can control the host server by adding the api key to the `.config/secret.json` file.
To talk to the python anywhere hosted server use the following command:

```bash
./o server -"command"
```

below find a list of available commands for the server tool.

## Web Apps

To get a detailed list of available web apps and their associated domains.

```bash
./o server -apps
```

## Consoles

To get a detailed list of available consoles

```bash
./o server -consoles
```

## CPU quota

To get a details on the CPU quota

```bash
./o server -cpu
```

## Always on Tasks

To get a detailed list of active always on tasks

```bash
./o server -tasks
```

<div style='margin:10% 0 5% 25%;'>
  <h1 align="center" style="color:lightgrey"> CI/CD Tools </h1>
</div>

## Setup

In order to run CI/CD commands you will need to add the target domain to your `.config/secret.json`. The domain setting
should begin with either `http` or `https` and end with a trailing `/`.

```json
{
  ...
  "DOMAIN_URL": "https://easter.company/",
  ...
}
```

CI/CD commands can only be requested from a Overlord local environment which is running the same parent repository
on the same branch as the target server.

ie; in-order to make a CI/CD request to a `server` based on the `Staging-Server` repo which is on the `main` branch
you will need to be working from a `local environment` based on `Staging-Server` which is also on the `main` branch.

## Server Restart

Restarting the server will selectively reboot the parent Django server associated with the repository you're currently
developing.

```bash
./o server -restart
```

## Server Update

The server update command will request the server to update to the latest version from the git repositories `current`
branch.

```bash
./o server -update
```

<div style='margin:10% 0 5% 25%;'>
  <h1 align="center" style="color:lightgrey"> Misc. Tools </h1>
</div>

## Help

To get help you can use the following command:

```bash
./o help
```

<p align="center" style="margin:10% 0 5% 0;">
  Documentation by <i>Easter Company</i>
</p>
