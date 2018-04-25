# run a test or a production server
from api import app


app.run(host='0.0.0.0', port=8080, debug=True)
