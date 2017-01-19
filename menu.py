import sys

from friend import Friend
from friend_manager import FriendManager
from util import get_absolute_path_of_file_parent_directory


class Menu:
    def __init__(self):
        self.friend_manger = FriendManager(
            get_absolute_path_of_file_parent_directory(__file__) +
            '/chumme.db')
        self.choices = {
            '1': self.add_friend,
            '2': self.modify_friend,
            '3': self.show_friends,
            '4': self.quit,
        }

    @staticmethod
    def _display_welcome_message():
        print('Welcome to ChumMe!')
        print('This application allows you to keep track of your friends.')

    @staticmethod
    def _display_menu():
        print("""Menu:
1. Add a friend
2. Modify friend
3. Show friends
4. Quit
""")


    def run(self):
        self._display_welcome_message()
        while True:
            self._display_menu()
            choice = input('Enter an option: ')

            try:
                self.choices[choice]()
            except KeyError:
                print('{} is not a valid choice.'.format(choice))

    def add_friend(self):
        first_name = input("Enter friend's first name: ")
        last_name = input("Enter friend's last name: ")
        self.friend_manger.add_friend(
            Friend(first_name=first_name, last_name=last_name))
        print('Your friend {0} {1} has been added.'.
              format(first_name, last_name))
        print()

    def modify_friend(self):
        friends = self.friend_manger.get_friends()
        print('Friends:')
        valid_ids = []
        for friend in friends:
            valid_ids.append(str(friend.id))
            print('{0}. {1} {2}'.format(
                friend.id, friend.name, friend.last_name))

        while True:
            id = input('What friend do you want to modify? ')

            if id in valid_ids:
                break

            print('Invalid option!')

        for field in ['first name', 'middle name', 'last name', 'birthdate', 'email', 'cell phone']:
            answer = input('Do you want to modify {}? (y/n) '.format(field))
            if answer in ('y', 'n'):
                if answer == 'y':
                    value = input('Enter value for {}: '.format(field))
                    db_field = '_'.join(field.split())
                    self.friend_manger.update_friend(id, db_field, value)
                    print('{} has been updated'.format(field))
                continue
            print('{} is not a valid option.'.format(answer))

    def show_friends(self):
        friends = self.friend_manger.get_friends()
        if not friends:
            print('There are no friends to show.')
            print()
            return

        print('Friends:')
        for i, friend in enumerate(friends):
            print('{0}. {1} {2}'.
                  format(i + 1, friend.first_name, friend.last_name))
        print()

    def quit(self):
        print('Thank you for using your ChumMe.')
        sys.exit(0)