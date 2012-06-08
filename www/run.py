import os
from app import application

if __name__ == '__main__':
    app_port = int(os.environ.get('PORT', 5000))
    application.run(debug = True, host='0.0.0.0', port=app_port)
