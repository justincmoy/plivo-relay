from actions import action_handler
from checks import check_plivo_signature, check_plivo_allowed_numbers

from flask import Flask, request
import traceback
app = Flask(__name__)


@app.route('/plivo', methods=['GET', 'POST'])
def process_plivo_request():
    try:
        from_number = request.form.get('From', '')

        check_plivo_signature(request.base_url, request.form, request.headers)
        check_plivo_allowed_numbers(from_number)

        action = request.form.get('Text', '').lower().strip()
        action_handler(from_number, action)
    except Exception:
        print(traceback.format_exc())

    return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
