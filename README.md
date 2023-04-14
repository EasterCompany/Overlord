<h6 align="center" style="border-bottom:0px;padding:9px 0 0 0;"> [ v1.2.9 14/04/2023 ] </h6>
<h1 align="center" style="margin-bottom:32px;border-bottom:0px;"> The Overlord Framework </h1>

### Welcome

The Overlord Framework, developed by Easter Company, is the one true full stack framework for developing
Python/Typescript Web & Mobile applications. General updates are released on an unscheduled basis and LTS
(long-term-support) versions are released annually.
[Watch a short introduction video here.](https://www.easter.company/overlord/introduction)

### Install

You can either download the contents of this repository and start building your project that way, or you can install
Overlord's `create-app` command. Which will allow you to create an Overlord App from your terminal. To do so, just copy
the code below into your terminal and hit enter.

```bash
sudo rm /bin/create-app &>/dev/null
sudo wget -P /bin/ https://raw.githubusercontent.com/EasterCompany/RDFS/Prd/Overlord/create-app
sudo chmod +x /bin/create-app
```

### Install Without Sudo

If you don't have sudo permissions or you don't want to install the `create-app` command globally on your system you can
use this as an alternative.

```bash
rm ~/create-app &>/dev/null
wget -P ~/ https://raw.githubusercontent.com/EasterCompany/RDFS/Prd/Overlord/create-app
mv ~/create-app ~/.create-app
chmod +x ~/.create-app
echo 'alias create-app="~/.create-app"' >> ~/.bashrc
```

### Documentation

If you're looking for our beautifully crafted and detailed documentation then you should
[visit our website](https://www.easter.company/overlord).

The documentation also includes a full series of tutorial style videos to guide you in a more entertaining fashion;
however, if you are a well-seasoned professional you may prefer to just read the written format on each page.

### FAQS

**Q:** How do I get started?<br/>
**A:** Check out the [getting started](https://www.easter.company/overlord/getting_started) page in the documentation.

**Q:** How can I make a feature request?<br/>
**A:** Email us at [contact@easter.company](mailto:contact@easter.company)

**Q:** How do I use E-Panel with my app?<br/>
**A:** Until further notice, E-Panel is free-to-use if you've subscribed to a an Easter Company custom app development
plan in-which Easter Company has designed, developed & deployed an application for you. Otherwise you will need to be
**invited to the closed beta by an existing user**.

### Donations

We aren't currently accepting donations, but if you're interested in helping out then please get in-touch via this email
[contact@easter.company](mailto:contact@easter.company)
