from sqlite3 import IntegrityError

from kivy.properties import ObjectProperty
from kivy.uix.modalview import ModalView

from controller.popup.getter import \
    get_interest_should_not_be_empty_string_popup, \
    get_interest_already_in_list_popup, get_interest_in_other_interests_popup
from database_manager.util import ChumMeDBManager
from .interest_util import add_interests_to_container, \
    add_interest_button_to_container, perform_operation_with_interests



class EditFriendInterests(ModalView):
    friend = ObjectProperty()

    def __init__(self, friend, **kwargs):
        self.friend = friend
        super().__init__(**kwargs)

        self.interests_to_add = set()
        self.interests_to_remove = set()

        friend_interests = ChumMeDBManager().friend_manager.\
            get_interest_by_friend_id(self.friend.id)
        other_interests = ChumMeDBManager().interest_manager.get_interests()
        other_interests = set(other_interests) - set(friend_interests)

        add_interests_to_container(
            self.friend_interests.interest_container,
            friend_interests, self._remove_interest
        )

        add_interests_to_container(
            self.db_interests.interest_container,
            other_interests, self._add_interest
        )

    def _add_interest(self, instance):
        interest = instance.text
        add_interest_button_to_container(
            self.friend_interests.interest_container,
            interest, self._remove_interest
        )

        self.interests_to_add.add(interest)
        self.interests_to_remove.discard(instance.text)
        self.db_interests.interest_container.remove_widget(instance)

    def _remove_interest(self, instance):
        interest = instance.text
        add_interest_button_to_container(
            self.db_interests.interest_container,
            interest, self._add_interest
        )

        self.interests_to_remove.add(interest)
        self.interests_to_add.discard(interest)
        self.friend_interests.interest_container.remove_widget(instance)

    def add_interest(self, interest):
        if not interest:
            self.popup = get_interest_should_not_be_empty_string_popup(
                self._on_answer
            )
            self.popup.open()
            return

        if self.is_interest_already_added(interest):
            self.popup = get_interest_already_in_list_popup(
                interest, self._on_answer)
            self.popup.open()
            return

        try:
            ChumMeDBManager().interest_manager.add_interest(interest)
        except IntegrityError:
            self.popup = get_interest_in_other_interests_popup(
                interest, self._on_answer)
            self.popup.open()
        else:
            add_interest_button_to_container(
                self.friend_interests.interest_container,
                interest, self._remove_interest
            )

            self.interests_to_add.add(interest)
            self.interest_text.text = ''
            self.interest_text.focus = True

    def is_interest_already_added(self, interest):
        return interest in self.interests_to_add or\
               interest in ChumMeDBManager().friend_manager.\
                   get_interest_by_friend_id(self.friend.id)

    def update_friend_property(self):
        self.friend = ChumMeDBManager().friend_manager.\
            get_interest_by_friend_id(self.friend.id)

    def cancel_edition(self):
        self.dismiss()

    def update_interests(self):
        self.add_interests(self.interests_to_add)
        self.remove_interests(self.interests_to_remove)
        self.dismiss()

    def add_interests(self, interests):
        perform_operation_with_interests(
            ChumMeDBManager().friend_interest_manager.add_friend_interest_ids,
            interests, self.friend
        )

    def remove_interests(self, interests):
        perform_operation_with_interests(
            ChumMeDBManager().\
                friend_interest_manager.delete_friend_interest_ids,
            interests, self.friend
        )

    def _on_answer(self, instance):
        self.popup.dismiss()
        self.interest_text.text = ''
        self.interest_text.focus = True
