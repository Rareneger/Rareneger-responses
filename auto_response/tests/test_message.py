import sys
sys.path.insert(0, './auto_response')

from mock_tests import MockInfo
import unittest
import message

class TestMessager(unittest.TestCase):

    def test_next_row(self):
        messager = message.Messager(MockInfo())

        self.assertEqual(messager.actual_row, 0)

        messager.next_row()
        self.assertEqual(messager.actual_row, 1)


    def test_previous_row(self):
        messager = message.Messager(MockInfo())

        self.assertEqual(messager.actual_row, 0)

        messager.previous_row()
        self.assertEqual(messager.actual_row, 0)

        messager.actual_row = 5
        messager.previous_row()
        self.assertEqual(messager.actual_row, 4)

    def test_is_position_valid(self):
        messager = message.Messager(MockInfo())

        self.assertTrue(messager.is_position_valid())
        messager.actual_row = 10
        self.assertFalse(messager.is_position_valid())

    def test_get_person_infos(self):
        messager = message.Messager(MockInfo())

        person = messager.get_person_infos()

        self.assertTrue(isinstance(person, message.PersonInfos))

    def test_get_command_message(self):
        messager = message.Messager(MockInfo())
        msg = messager.get_command_message(messager.get_person_infos())
        self.assertTrue(isinstance(msg, str))

    def test_mount_message(self):
        messager = message.Messager(MockInfo())
        msg = messager.mount_message(messager.get_person_infos())
        self.assertTrue(isinstance(msg, str))

if __name__ == '__main__':
    unittest.main()