from aiogram.utils.helper import Helper, HelperMode, ListItem


class BotStates(Helper):
    mode = HelperMode.snake_case

    GET_PICTURES = ListItem()
    SEND_PDF = ListItem()


if __name__ == '__main__':
    print(TestStates.all())
