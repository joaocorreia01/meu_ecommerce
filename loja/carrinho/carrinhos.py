from flask import redirect, url_for, render_template, request, flash, session, current_app
from loja import db, app

@app.route('/addCart', methods=['POST'])
def AddCart():
    try:
        pass
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)
    