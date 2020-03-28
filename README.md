Flask App + Gunicorn Web Server

Currently running gunicorn with on worker so that I can incoporate socketIO, which requires sticky sessions.

Eventually, I can add a load balancer (nginx) in front of this to manage multiple different, one worker gunicorn processes.

