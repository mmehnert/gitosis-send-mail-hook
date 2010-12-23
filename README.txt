gitosis-send-mail-hook

This is a script that should make it possible to inform all persons that
have acces to a gitosis-managed repository upon changes via the
post-receive-email script.

Change 

recipients=$(git config hooks.mailinglist)

to 

recipients=$(/path/gitosis-send-mail-hook.py)

in your copy of post-receive-email from
/usr/share/doc/git-core/contrib/hooks/

