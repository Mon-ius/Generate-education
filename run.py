from app import create_app
from app.models import Ngrok
from ext import db

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Ngrok': Ngrok}
if __name__ == '__main__': 
    app.run(debug=True)          