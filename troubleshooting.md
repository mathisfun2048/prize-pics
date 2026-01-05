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