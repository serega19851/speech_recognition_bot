import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env
import random


def echo(event, vk_api_):

    vk_api_.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1, 1000))


def main():
    env = Env()
    env.read_env()
    vk_token = env.str('VK_GROUP_TOKEN')
    vk_session = vk_api.VkApi(token=vk_token)
    longpoll = VkLongPoll(vk_session)
    vk_api_ = vk_session.get_api()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api_)


if __name__ == '__main__':
    main()
