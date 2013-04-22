simplelivepoll
==============

I've gone for two booleans on a question: 'live' and 'closed'.

The main page

http://127.0.0.1:8000/questions/

will redirect to the first 'live', not 'closed' question, or 404 if there isn't one (so the front-end should keep checking that URL?).

When a question becomes available it is at the ID, e.g.:

http://127.0.0.1:8000/questions/1/

This is a form to submit you answer, which on success, redirects to the relevant results URL:

http://127.0.0.1:8000/results/1/

This will also 404 until the results are available (the closed boolean).

once that page is loaded the front end should again check in with /questions/ to see when the next question is available.

Does that work? Anything I can do to make the front-end easier (apart from writing a "real" REST api, which seemed a bit much…)
