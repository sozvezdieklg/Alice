import logging

from flask import Flask, request, jsonify

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

storageSession = {}


def get_suggests(user_id):
    session = storageSession[user_id]
    suggests = [{'titile': suggest, 'hide': True}
                for suggest in session['suggests'][:2]]
    session['suggests'] = session['suggests'][1:]
    storageSession[user_id] = session

    if len(suggests) < 2:
        suggests.append({
            'title': "Ладно",
            "url": "https://eda.yandex.ru/kaluga",
            "hide": True

        })
    return suggests


def handle_dialog(request, response):
    user_id = request['session']['user_id']
    if request['session']['new']:
        storageSession[user_id] = {
            'suggests': [
                "Не хочу",
                "Не буду",
                "Отстань"
            ]
        }
        response['response']['text'] = 'Привет, купи слона!'
        response[response]['buttons'] = get_suggests(user_id)
        return
    if request['request']['original_utterance'].lower() in [
        "ладно",
        "куплю",
        "покупаю",
        "хорошо",
        "уже купил"
    ]:
        response['response']['text'] = "А еще слона можно заказать на Яндкс.Еда!"
        response['response']['end_session'] = True
        return
    response['response']['text'] = \
        f"Все говорят {request['request']['original_utterance']}, а ты купи слона на Яндекс Еде"
    response['response']['button'] = get_suggests(user_id)


@app.route('/post', methods=['POST'])
def main():
    logging.info(f"Request: {request.json!r}")
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(request.json, response)
    logging.info(f"Response: {response!r}")
    return jsonify(response)


if __name__ == '__main__':
    app.run()
