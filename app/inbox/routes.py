from flask import render_template, request, redirect, url_for
from . import inbox

messages = []

@inbox.route('/inbox', methods=['GET', 'POST'])
def inbox_view():
    if request.method == 'POST':
        message = request.form.get('message')
        if message:
            messages.append(message)
        return redirect(url_for('inbox.inbox_view'))
    return render_template('inbox.html', messages=messages)

