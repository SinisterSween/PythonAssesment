I was able to create a transaction engine in python. However I started with user input and had issues converting this to
a CSV reader to be able to parse through all lines as it did not want to convert a list object to a float. I didnt want
to keep you all waiting any longer so I wanted to turn it in. Further I wasnt able to get all functions working properly
but I hope this shows you some skill level. I also found a rust solution to this but I didnt write that so I didnt want
to submit it as my work but also wanted to show my resourcefulness at finding solutions without reinventing the wheel as
sometimes someone out there has already done exactly what you are trying to do.

There is self testing built in and that is the default. If you want to do user inputs take out Test().run() and put
App().run()