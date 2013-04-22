simplelivepoll
==============

The first questions is at:

http://127.0.0.1:8000/questions/1/

If the question isn't live yet, it will 404.

This is a form to submit you answer, which on success, redirects to the relevant results URL:

http://127.0.0.1:8000/results/1/

The front-end JS just then needs to keep checking the next question (id 2)? until that URL doesn't 404, and redirect to it when it does.