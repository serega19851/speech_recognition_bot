import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env
import random
from auxiliary_file import detect_intent_texts


def echo(event, vk_api_, project_id, session_id):
    answer = detect_intent_texts(
        project_id, session_id, event.text, 'ru-RU')

    if not answer.intent.is_fallback:
        vk_api_.messages.send(
            user_id=event.user_id,
            message=answer.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


def main():
    env = Env()
    env.read_env()
    vk_token = env.str('VK_GROUP_TOKEN')
    project_id = env.str('PROJECT_ID')
    session_id = env.str('VK_CHAT_ID')

    vk_session = vk_api.VkApi(token=vk_token)
    longpoll = VkLongPoll(vk_session)
    vk_api_ = vk_session.get_api()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api_, project_id, session_id)


if __name__ == '__main__':
    main()
