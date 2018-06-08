from app import create_app, cli

from ext import db
from app.models import User, Post, Section


app = create_app()
cli.register(app)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Section': Section}

if __name__ == '__main__': 
    app.run(debug=True)          
