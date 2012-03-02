import next
import unittest

class TestFileParser(unittest.TestCase):

    def test_blank_file(self):
        blank = next.TodoFile('tests/blank.otl')
        self.assertEqual('', blank.next()[2])

    def test_signle(self):
        tf = next.TodoFile('tests/single.otl')
        self.assertEqual('line one', tf.next()[2])

    def test_flat_file(self):
        tf = next.TodoFile('tests/flat.otl')
        self.assertEqual('line one', tf.next()[2])

    def test_skip_completed(self):
        tf = next.TodoFile('tests/skip.otl')
        self.assertEqual('line three', tf.next()[2])

    def test_multi_level(self):
        tf = next.TodoFile('tests/multi_level.otl')
        self.assertEqual('1a1', tf.next()[2])

    def test_multi_level_skip(self):
        tf = next.TodoFile('tests/multi_level_skip.otl')
        self.assertEqual('1a', tf.next()[2])

    def test_multi_level_skip_subs(self):
        tf = next.TodoFile('tests/multi_level_skip_subs.otl')
        self.assertEqual('1b', tf.next()[2])

if __name__ == '__main__':
    unittest.main()

