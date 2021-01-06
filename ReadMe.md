
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

Server will run on port 8000
```bash
cd server && ./manage.py runserver
```

### Start Client

Client will run on port 8100
```bash
cd client && npm start
```

### Start Both

Server will run on port 8000 and client will run on port 8100
```bash
./run.py
```

# Task List

Listed below is the planned feature scope of the next stable build. <br>
Tasks marked (<span style='color:green'> ✔ </span>) have been completed. <br>
Tasks marked (<span style='color:red'> ⨯ </span>) have been discarded. <br>
Tasks left unmarked are currently in development or will begin development soon. <br>

## Patch 0.0.1

### API

   1. Connects to database <span style='color:green'> ✔ </span>
   2. Returns requested journal entry <span style='color:green'> ✔ </span>
   3. Returns requested users journal entries <span style='color:green'> ✔ </span>
   4. Consumes data for new journal entries

---

### User Pages

   1. Register
   2. Login
   3. Logout
   4. Profile
      1. Display picture
      2. Profile biography
      3. Follow button
   5. Feed
      1. Displays your posts
      2. Displays posts from followed users
      3. Displays popular posts from followed topics

---

### Entries

   1. Create
      1. Add text
      2. Add image
   2. Delete
      1. Confirmation
   3. Sharing

---

### Following

   1. Follow
   2. Unfollow
   3. Followers

---

### Longterm Feature Section

   1. Notifications
   2. Direct Messages
   3. Explore Hashtags

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
