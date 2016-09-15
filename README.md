# Gsevol-web

Gsevol is a web application for reconciling and visualizing phylogenetic trees. See [Gsevol live](http://gsevol.azor.mimuw.edu.pl/).
It was started as a thesis project in Bioinformatics.

The app is based on three computational packages by [Paweł Górecki](http://www.mimuw.edu.pl/~gorecki/). They are external dependencies, not included in this repo and are not published anywhere at the moment. So if you'd like to set up the project, please contact @otraczyk for the mssing parts.

Most of the code is written in Django. It uses celery message queue to delegate computational tasks and websockets to send back results. The frontend (embedded in app) uses ReactJS for code organization.
