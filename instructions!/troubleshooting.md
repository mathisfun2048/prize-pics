# Troubleshooting

I've had a lot of niche problems while doing hardware, so I'm compiling all the problems I've encountered in this doc!

## "nasty" ssh problem

When trying to ssh onto your raspberry pi, you might get the following error:

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
```
This is because when you install a fresh copy of raspberian on a board you used for a different project, your ip address **won't** change, but your host name might. That is what causes this error. To fix, you need authorize that ip address with the following command: 

``` sh-keygen -R <IP ADDRESS> ```

## pushing files from rpi to github

Somehting really annoying about pushing files from your RPi to github is that you need to enter your username and password. However, you don't enter your password! You need to enter a personal access token!. The way you can get one is:

github -> settings -> developer settings ->  personal access tokens -> tokens -> generate new token

** Make sure you copy this token! If you don't you'll have to make a new one!