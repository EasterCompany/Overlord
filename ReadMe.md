
# Overlord Web Repository

Contained within this repository is a collection of open source applications which are
deployed on the [easter.company](https://easter.company) domain and are contained within
the Overlord framework. You can find documentation for these applications in this
repository [here.](https://github.com/eastercompany/overlord/docs) If you have any
queries, bug reports or general requests please do not hesitate to get in touch using
[facebook](https://facebook.com/eastercompany) or
[twitter](https://twitter.com/eastercompany).

## Local Host

### Start Server

Server will run on <b>port 8000</b>
```bash
./manage.py server
```

### Start Client

Client will run on <b>port 8100</b>
```bash
./manage.py client
```

### Start Test Suite

Pytest Suite will run on your local machine
```bash
./manage.py test
```

### Start Server & Client

<b>Server</b> will run on <b>port 8000</b><br/>
and <b>client</b> will run on <b>port 8100</b>
```bash
./manage.py run
```

### Start Production Build Process

When the production build is the latest version you won't need to run the client.
```bash
./manage.py build
```

# Task List

Listed below is the planned feature scope of the next stable build. <br>
Tasks marked (<span style='color:green'> ✔ </span>) have been completed. <br>
Tasks marked (<span style='color:red'> ⨯ </span>) have been discarded. <br>
Tasks left unmarked are currently in development or will begin development soon. <br>

# Patch 0.0.1

### User API

   1. Registers new users
   2. Approves user login
   3. ends user on logout

---

### Journal API

   1. Connects to database <span style='color:green'> ✔ </span>
   2. Returns requested journal entry <span style='color:green'> ✔ </span>
   3. Returns requested users journal entries <span style='color:green'> ✔ </span>
   4. Consumes data for new journal entries
      1. Head
      2. Body
      3. Type
      4. Image
      5. Set date
      6. Set user

---

### Following API

   1. Follow user
   2. Unfollow user
   3. Return list of following
   4. Return list of followers

---

### User Pages

   1. Register
   2. Login

---

### Journal Pages

   1. New Entry Page
      1. Consumes entry head
      2. Consumes entry body
      3. Consumes entry date
      4. Consumes entry user
      5. Consumes entry type
      6. Consumes entry image
   2. My Entries Page
      1. Display entries
      2. Display picture
      3. Updates picture
      4. Profile biography
      5. Followers
      6. Following
      7. Follow Button
   3. My Feed Page
      1. Displays entries from followed users
      2. Displays entries from followed topics
      3. Suggests new users to follow
      4. Suggests new topics to follow

---

### Longterm Feature Section

   1. Notifications
   2. Direct Messages
   3. Hashtags & Topics
   4. User Settings
   5. Easter Company Global Profile

<br />
<br />
<h2> Technology </h2>
<table>
   <tr>
      <td valign="middle">
         <a href='https://reactjs.org/'>
            <img
               alt='React.js'
               src='https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/react/react.png'
               width='64px'
               height='64px'
            />
            <p align='center'> React.js </p>
         </a>
      </td>
      <td valign="middle">
         <a href='https://www.python.org/'>
            <img
               alt='Python'
               src='https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/python/python.png'
               width='64px'
               height='64px'
            />
            <p align='center'> Python </p>
         </a>
      </td>
      <td valign="middle">
         <a href='https://nodejs.org/'>
            <img
               alt='Node.js'
               src='https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/nodejs/nodejs.png'
               width='64px'
               height='64px'
            />
            <p align='center'> Node.js </p>
         </a>
      </td>
      <td valign="middle">
         <a href='https://www.djangoproject.com/'>
            <img
               alt='Django'
               src='https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/django/django.png'
               width='64px'
               height='64px'
            />
            <p align='center'> Django </p>
         </a>
      </td>
   </tr>
</table>
<br />
<br />

<p align='center'> Easter Company © 2021 </p>
