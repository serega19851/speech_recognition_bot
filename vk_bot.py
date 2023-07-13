import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env
import random
from text_dialog_flow import detect_intent_texts
from requests.exceptions import ReadTimeout, ConnectionError
from time import sleep
import telegram


def sends_response_user(event, vk_api_, project_id):
    session_id = f'vk-{event.user_id}'
    answer = detect_intent_texts(
        project_id, session_id, event.text, 'ru-RU')
    if not answer.intent.is_fallback:
        vk_api_.messages.send(
            user_id=event.user_id,
            message=answer.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


def main():
    while True:
        env = Env()
        env.read_env()
        vk_token = env.str('VK_GROUP_TOKEN')
        project_id = env.str('PROJECT_ID')
        session_te_id = env.str('TELEGRAM_CHAT_ID')

        vk_session = vk_api.VkApi(token=vk_token)
        longpoll = VkLongPoll(vk_session)
        vk_api_ = vk_session.get_api()
        bot_log = telegram.Bot(token=env.str('TELEGRAM_LOG'))
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    sends_response_user(event, vk_api_, project_id)
        except ReadTimeout as timeout:
            bot_log.send_message(
                chat_id=session_te_id,
                text=f'Ошибка сети VK бота\n{timeout}\n'
            )
        except ConnectionError as connect_er:
            bot_log.send_message(
                chat_id=session_te_id,
                text=f'Ошибка VK\n{connect_er}\n'
            )
            sleep(20)


if __name__ == '__main__':
    main()
