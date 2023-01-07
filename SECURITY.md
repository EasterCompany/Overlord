# Security Policy

## Supported Versions

LTS (long-term-support) versions are released annually in January of each year and regular versions are released on an
unscheduled basis.

LTS versions will no longer be supported once the next LTS version has been released and unsupported versions will
receive a notification to update as soon as possible.

New feature updates will be developed and deployed with a "it's ready when it's ready" policy.

| Version | Currently Supported | LTS                |
| ------- | ------------------- | ------------------ |
| 1.2.x   | :white_check_mark:  | :white_check_mark: |
| 1.0.x   | :x:                 | :x:                |

## Version Labels

The Overlord Framework has a simple version labeling strategy although it is unique.

A version label contains three numbers each separated by a point like this: `1.2.3`
The first number represents a "major release", the second number represents a "minor release" and the third represents
a "patch release".

**Major releases** mean that your method of updating is now broken, any previous projects using this framework may no-longer
be supported or will at least require some level of re-write to be made compatible again.

**Minor releases** mean that you may not notice any difference when you update to the new version, except you will have
more features than before.

**Patch releases** mean that you won't notice any difference at all, except the new version contains bug fixes.

Each minor version release follows a pattern - and this is where the version labeling system becomes quite unique.

Publicly available versions of Overlord will always contain an even number for the minor release value. Odd numbers for
the minor release are private versions that are only to be used internally at Easter Company. This is because we use
Overlord for all of our products and usually run a private version internally in-which we prototype new ideas to satisfy
our requirements.

It may take some time before we can make all of these features public due to various reasons, sometimes this is because
certain features may have security vulnerabilities and sometimes this may be because certain features are dependent on
proprietary software developed by Easter Company.

## Reporting a Vulnerability

If you have identified a vulnerability within the Framework or just want to make a feature request please get in-touch
with as using this email address [contact@easter.company](mailto:contact@easter.company)
