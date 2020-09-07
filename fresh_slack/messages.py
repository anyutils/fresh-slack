warning_message = '''
Very quiet channel, here. We tend the channel garden by archiving channels that
have been quiet for {warn_days} days or more, and this channel is one of them.
Archiving a channel removes it from the list of active channels and prevents new
comments from being made there. That makes it easier for newer & tenured folks
alike to find the right place to get their questions, answers and comments heard
without wading through lots of channels -- or worse, posting a comment only to
hear nothing in response.

All existing comments in the channel are retained for easy browsing and
searching and can be read like any other channel. If a need for this particular
channel arises again, it can be unarchived later.

If you'd like to keep this channel active, _SAY ANYTHING_ and we'll reset the
timer. If we don't hear from anyone soon, this channel will be archived.

(control code: stale-channel-warned)
'''

archive_message = '''
This channel is still very quiet. We're archiving this channel as it's been
crickets here for {archive_days} days or longer. Content on this channel is
still available via search and someone can un-archive a channel if they want to
dust it off.

(control code: stale-channel-archived)
'''
