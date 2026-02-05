# datsci_testing
A repository for tinkering and learning, related to a class I took.


## Homework 2
- How do you fill in the missing dates from the grants data?

I'd fill them in as NaN, as there's no real way to know when they were supposed to be. You could estimate, but this is innacurate. They already are this way by default, so nothing needs to be done.

- PI_NAMEs contains multiple names. We can only connect individual people. Can you make it so that we can get "grantees"?

I'll make a new column in the data frame titled 'grantees' that contains each grantee in a list. 

- The dates for Articles are problematic. Can you fix them?

The program initially only reads line breaks for the dates. I can fix them by redefining how the data frame reads the date/time info should work.
