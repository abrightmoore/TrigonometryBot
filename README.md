# TrigonometryBot
A Twitter Bot that generates images using mathematic functions

Check its work on Twitter as https://twitter.com/TrigonometryBot/with_replies

![Sample output](https://pbs.twimg.com/media/C5ZgkRQUwAEjWrr.jpg)

# Dependencies
1. markovbot from @esdalmaijer. Use for witty conversation. Get it via: https://github.com/esdalmaijer/markovbot
2. TwitterAPI by @boxnumber03. Wrapper to communicate via Twitter. Get it via: https://dev.twitter.com/resources/twitter-libraries

# How it works
1. AJB_TrigonometryBot_v9.py is the main module. It connects to Twitter and manages the work/sleep cycle. This bot is lazy so it doesn't get kicked by Twitter.
2. Trigpic.py is where the image rendering goes
3. Test.py is a harness that drives Trigpic.py to generate local images for testing the image rendering methods

The main image routine is in 'beCreative()'. You can add more image renderers to Trigpic.

![Sample output](https://pbs.twimg.com/media/C5bKrvtU0AAT6GC.jpg)

