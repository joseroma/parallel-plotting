import unittest
from Code.parallelCoordinates import ParallelCoordinates

class TestMethods(unittest.TestCase):
    ##### Missing data  #########

    def test_empty_file_name_throws_exception(self):
        self.parallel = ParallelCoordinates(file='', library='pyplot')
        with self.assertRaises(Exception):
            self.parallel.plot()

    def test_try_to_call_save_without_passing_result_parameter_throws_exception(self):
        self.parallel = ParallelCoordinates(file='FUN.BB11002.tsv', library='pyplot')
        with self.assertRaises(Exception):
            self.parallel.save("jpeh.html")

    def test_empty_file_throws_exception_no_columns_parse_from_file(self):
        self.parallel = ParallelCoordinates(file='../Tests/testing_files/empty', library='pyplot')
        with self.assertRaises(Exception):
            self.parallel.plot()

    ##### Wrong data  #########

    def test_wrong_library_name_throws_exception(self):
        self.parallel = ParallelCoordinates(file='FUN.BB11002.tsv', library='pypplot')
        with self.assertRaises(Exception):
            self.parallel.plot()

    def test_wrong_file_name_throws_exception(self):
        self.parallel = ParallelCoordinates(file='FUN.BB11003.tsv', library='pyplot')
        with self.assertRaises(Exception):
            self.parallel.plot()

    def test_try_to_save_on_a_extension_not_allowed_throws_exception_plotly(self):
        self.parallel = ParallelCoordinates(file='../data/FUN.BB11001.tsv', library='plotly')
        res = self.parallel.plot()
        with self.assertRaises(Exception):
            self.parallel.save(res, "results.ppp")
    def test_try_to_save_on_a_extension_not_allowed_throws_exception_pyplot(self):
        self.parallel = ParallelCoordinates(file='../data/FUN.BB11001.tsv', library='pyplot', save_file_name="Results/results.ppp")
        res = self.parallel.plot()
        with self.assertRaises(Exception):
            self.parallel.save(res)

    def test_try_to_save_on_a_extension_not_allowed_throws_exception_bokeh(self):
        self.parallel = ParallelCoordinates(file='../data/FUN.BB11001.tsv', library='bokeh', save_file_name="Results/results.ppp")
        res = self.parallel.plot()
        with self.assertRaises(Exception):
            self.parallel.save(res)

    def test_try_to_execute_data_frame_with_too_much_columns_throws_exception(self):
        self.parallel = ParallelCoordinates(file='../Tests/testing_files/tooBig.csv', library='plotly')
        with self.assertRaises(Exception):
            self.parallel.plot()

    def test_try_to_read_data_frame_with_invalid_extension_throws_exception(self):
        self.parallel = ParallelCoordinates(file='../Tests/testing_files/empty.ppp', library='plotly')
        with self.assertRaises(Exception):
            self.parallel.plot()

    def test_try_to_set_tags_and_length_tags_does_not_match_length_columns_throws_exception(self):
        self.parallel = ParallelCoordinates(file='iris.csv', library='plotly', tags=['Una'])
        with self.assertRaises(Exception):
            self.parallel.plot()

    def tearDown(self):
        print("Test passed correctly")
