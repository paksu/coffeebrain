import unittest
import tempfile
import shutil
import dataloader
import os


class TestDataLoader(unittest.TestCase):
    def test_categorize_and_split_dataset(self):
        left_dataset, right_dataset = dataloader.categorize_and_split_dataset([
            ['one', 'little', 'little'],
            ['two', 'empty', 'plenty'],
            ['three', 'full', 'full'],
            ['four', 'little', 'empty'],
            ['six', 'little', 'empty'],
            ['seven', 'full', 'empty'],
            ['eight', 'little', 'unknown']
        ])
        self.assertItemsEqual(left_dataset['little'], ['one', 'four', 'six', 'eight'])
        self.assertItemsEqual(left_dataset['empty'], ['two'])
        self.assertItemsEqual(left_dataset['full'], ['three', 'seven'])

        self.assertItemsEqual(right_dataset['little'], ['one'])
        self.assertItemsEqual(right_dataset['empty'], ['four', 'six', 'seven'])
        self.assertItemsEqual(right_dataset['plenty'], ['two'])
        self.assertItemsEqual(right_dataset['full'], ['three'])

    def test_create_directories(self):
        temp_dir = tempfile.mkdtemp()
        dataloader.create_directories(root=temp_dir)

        # check that images were created
        self.assertTrue("{}/images".format(temp_dir), "Missing images directory")

        # check that dataset directories were created
        for dataset in ['training_data', 'testing_data']:
            for label in ['unknown', 'empty', 'little', 'plenty']:
                left_dir = "{}/{}/left_{}".format(temp_dir, dataset, label)
                right_dir = "{}/{}/right_{}".format(temp_dir, dataset, label)
                self.assertTrue(os.path.isdir(left_dir), "Missing directory {}".format(left_dir))
                self.assertTrue(os.path.isdir(right_dir), "Missing directory {}".format(right_dir))

        shutil.rmtree(temp_dir)

if __name__ == '__main__':
    unittest.main()
