
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

<h2 style='text-align:center;margin:16px 0 16px 0'> Technology </h2>
<div style='display:flex;justify-content:space-around;'>

   <a href='https://reactjs.org/'>
      <div style='height:64px;width:64px;'>
         <img
            alt='React.js Logo'
            src='https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/react/react.png'
            style='height:64px;width:64px;'
         />
         <h4 style='text-align:center;'> React.js </h4>
      </div>
   </a>

   <a href='https://www.python.org/'>
      <div style='height:64px;width:64px;'>
         <img
            alt='Python Logo'
            src='https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/python/python.png'
            style='height:64px;width:64px;'
         />
         <h4 style='text-align:center;'> Python </h4>
      </div>
   </a>

   <a href='https://nodejs.org/'>
      <div style='height:64px;width:64px;'>
         <img
            alt='Node.js Logo'
            src='https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/nodejs/nodejs.png'
            style='height:64px;width:64px;'
         />
         <h4 style='text-align:center;'> Node.js </h4>
      </div>
   </a>

</div>
