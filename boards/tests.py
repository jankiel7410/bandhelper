from django.contrib.auth.models import User
from django.test import TestCase

from boards import models


class UserTest(TestCase):
    def test_has_default_board(self):
        """
        When you create an user, a default board must be created.
        """
        user = User.objects.create(username='test user', email='test_user@bandhelper.com')
        self.assertEqual(user.boards.count(), 1)


class BoardTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test user', email='test_user@bandhelper.com')
        self.board = self.user.boards.first()

    def test_default_board_has_3_lists(self):
        """
        Assert that default board has 3 lists.
        """
        self.assertEqual(self.board.lists.count(), 3)

    def test_default_lists(self):
        """
        Assert that default lists have proper names.
        """
        default_titles = ['Propositions', 'To try', 'Accepted', ]
        lists = self.board.lists.all()
        for board_list in lists:
            self.assertIn(board_list.title, default_titles)

    def test_default_lists_positions(self):
        """
        Test positions of lists. Default lists should have positions: 0, 1 and 2.
        New list should have number 3.
        """
        positions = {0, 1, 2}
        lists = self.board.lists.all()
        self.assertEqual({l.position for l in lists}, positions)
        new_list = models.List.objects.create(board=self.board, title='new list')
        new_list_position = 3
        self.assertEqual(new_list.position, new_list_position)
