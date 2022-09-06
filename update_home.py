import json
from textwrap import indent
from notion_client import Client
import datetime
from random import randint

keys = json.load(open("keys.json", 'r'))
images = json.load(open("notion.json", 'r'))
emoji = [
    '🙂',
    '🤑',
    '😎',
    '🤓',
    '🧀',
    '⭐',
    '✨',
    '💯',
]


def get_time():
    now = datetime.datetime.now()
    if now.hour > 18 or now.hour < 6:
        return 'dark'
    else:
        return 'light'


def update_title(notion: Client):
    notion.blocks.update(
        **{
            "block_id": images['title'],
            "heading_1": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": ("Good morning, " if get_time() == 'light' else "Good evening, ") + "Kanishq"
                    },
                    "annotations": {
                        "color": ("red" if get_time() == 'light' else "purple")
                    }
                }]
            }
        }
    )


def update_headings(notion: Client):
    for heading in images['heading_1']:
        notion.blocks.update(
            **{
                "block_id": heading['id'],
                "heading_1": {
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": heading['content']
                        }
                    }],
                    "color": ("red_background" if get_time() == 'light' else "blue_background")
                }
            }
        )
    for heading in images['heading_2']:
        notion.blocks.update(
            **{
                "block_id": heading['id'],
                "heading_2": {
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": heading['content']
                        }
                    }],
                    "color": ("orange_background" if get_time() == 'light' else "purple_background")
                }
            }
        )


def get_updated(page):
    cover = page['cover']['external']['url']
    if cover == images['cover'][get_time()]:
        return True
    else:
        return False


def update_cover(notion: Client):
    notion.pages.update(
        **{
            "page_id": keys['ilios'],
            'cover': {
                "type": "external",
                "external": {
                        "url": images['cover'][get_time()]
                }
            },
            'icon': {
                "type": "emoji",
                "emoji": emoji[randint(0, len(emoji) - 1)],
            }
        }
    )


def update_images(notion: Client):
    for image in images['images']:
        id = image['id']
        notion.blocks.update(
            **{
                "block_id": id,
                "image": {
                    "external": {
                        "url": image[get_time()]
                    }
                }
            }
        )


def update_home():
    notion = Client(auth=keys['notion'])
    page = notion.pages.retrieve(keys['ilios'])
    if get_updated(page):
        return
    update_cover(notion)
    update_title(notion)
    update_images(notion)
    update_headings(notion)


if __name__ == "__main__":
    update_home()
