# Flask RESTful API
The assessment is a back-end-only Python application by Flask that runs on the web.
The application interrogates a local MySQL database through API endpoints, which
allow data fetching and all CRUD operations. To protect the endpoints from
unauthorised access, a JSON Web Token system has been implemented. The session's
timeout is 30 minutes. 

However, the web token is refreshed at every request to guarantee the use of the
application without interruptions. The application also handles error inputs that the
User might run into, preventing the application from crashing. In case of human error,
the User can remake a request by providing the right inputs.
Requests can be made through the website Postman. However, to perform some
requests, the desktop version of the service has to be installed.

A database is created on the application startup, and some data are uploaded. This
process is performed only once, meaning data will not be overwritten. The database has
two tables joined by a One to One relationship. The table Student comes with a sample
dataset whilst the Address table is empty. An additional table, User, hosts information
about users in order to perform login operations. A default user is added with the
following credentials:

email: guest@xandertalent.com
password: Welcome_to_this_assessment01

Finally, the application provides an additional endpoint to interact with Google's
Geocoding API. By passing the StudentID, the application can interrogate Google's API
using latitude and longitude as parameters. This will return an address, which will be
inserted into the address table
