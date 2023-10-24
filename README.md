# Overlord 1.3
Cross platform command line interface for interacting with the overlord tools api.

## Introduction
This project aims to unify an entire organizational infrastructure into one interface, so a developer can easily
replicate server environments, develop projects, merge and deploy with a full integrated and stress free pipeline and
much more.

## Utils
The utils directory located at `./utils` contains scripts for developers of this repository to use to ease-development.

## Builds & Versions
This section describes the build & versioning structure of Overlord Tools.

### LTS
Current long term support version does not exist. The initial targeted LTS version will be 1.0 and maintain support
for mainstream linux, mac & windows operating systems.

Long Term Support version refers to the major & minor release numbers of a version label,
in this case, 1 is the major release number and 0 is the minor release number. The third number in the version label
is the Patch number and LTS users will still receive these updates.

Patch updates to a LTS version will only ever include bug fixes. Each LTS version will be supported for 1 year starting
on the *31st of January* each year. Upon the release of a new LTS version at the start of a year the previous version
will become archived.

The current LTS version will exist on the LTS branch of this repository.

### Archived
Supported archive versions are within in the `./dist` and should be updated within the merge request when relevant.
Updating a build version that already exists is known as a 'Hot Patch', these kind of releases do not require patch
notes or github release archives associated with them. Hot Patches will effect users with auto-updates enabled, who
force update or who recently installed.

### Build
The local build directory, sometimes called the development build, located at `./build` will be overwritten every time
you run the build command and is useful for testing changes locally.
