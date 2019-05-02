import unittest
import trello
import arrow
import requests

TEST_BOARD = 'Trello.py Tests'
TEST_LISTS = ['List 1', 'List 2', 'List 3']
TEST_LABELS = ['test-label-1', 'test-label-2']
TEST_CUSTOM_FIELDS = ['CUSTOM_TEXT', 'CUSTOM_DATE']
TEST_DATE = '2099-05-03T09:00:00+00:00'


class TrelloTest(unittest.TestCase):
    def setUp(self):
        self.client = trello.Client()

    def tearDown(self):
        self.client.close()

    def test_boards(self):
        boards = self.client.get_my_boards()
        self.assertIn(TEST_BOARD, boards)

    def test_board_labels(self):
        board = self.client.get_my_boards()[TEST_BOARD]
        labels = board.get_labels()
        self.assertEqual(TEST_LABELS, labels.keys())

    def test_lists(self):
        board = self.client.get_my_boards()[TEST_BOARD]
        lists = board.get_lists()
        self.assertEqual(TEST_LISTS, lists.keys())

    def test_cards(self):
        board = self.client.get_my_boards()[TEST_BOARD]
        cards = board.get_cards()
        labels = board.get_labels()
        lists = board.get_lists()
        custom_fields = board.get_custom_fields()

        label_0 = labels[TEST_LABELS[0]]
        label_1 = labels[TEST_LABELS[1]]
        list_0 = lists[TEST_LISTS[0]]
        list_1 = lists[TEST_LISTS[1]]
        custom_field_text = custom_fields[TEST_CUSTOM_FIELDS[0]]
        custom_field_date = custom_fields[TEST_CUSTOM_FIELDS[1]]

        for card in cards:
            self.assertTrue(card.last_activity)
            if card.name == 'Card 1':
                self.assertTrue(card.is_in_list(list_0))
                self.assertFalse(card.is_in_list(list_1))
                self.assertTrue(card.has_label(label_0))
                self.assertFalse(card.has_label(label_1))
                self.assertEqual(card.get_custom_field(custom_field_text), 'TEST')
                self.assertEqual(card.get_custom_field(custom_field_date), arrow.get(TEST_DATE))
                self.assertRaises(requests.exceptions.HTTPError, card.add_label, label_0)
                #self.assertRaises(requests.exceptions.HTTPError, card.move_to_list, list_0)
                self.assertEqual(card.due, arrow.get(TEST_DATE))
                self.assertTrue(card.due_complete)
                card.move_to_list(list_1)
                card.move_to_list(list_0)
            else:
                self.assertFalse(card.has_label(label_0))
                self.assertFalse(card.has_label(label_1))                
                self.assertIsNone(card.get_custom_field(custom_field_text))
                self.assertIsNone(card.get_custom_field(custom_field_date))
                self.assertEqual(card.due, None)
                self.assertFalse(card.has_label(label_0))
                self.assertFalse(card.has_label(label_1))
                card.add_label(label_0)
                card.remove_label(label_0)

    def test_custom_fields(self):
        board = self.client.get_my_boards()[TEST_BOARD]
        custom_fields = board.get_custom_fields()
        self.assertEqual(TEST_CUSTOM_FIELDS, custom_fields.keys())
