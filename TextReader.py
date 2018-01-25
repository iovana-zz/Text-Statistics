import unittest
import string
import random
import sys

# Currently supported file extensions
txt_file_types = ["txt"]

class FileReader:

    def __init__(self, file_name, is_file=True):
        self.file_name = file_name
        self.is_file = is_file
        self.file_lines = []
        # Save the statistics but make them inaccessible
        self.__char_frequency = {}
        self.__most_common_letters = None
        self.__word_count = None
        self.__avg_no_letters = None
        self.__construct_word_array()
        self.__most_common_letters_frequency = 0

    # Check if the file type provided can be read
    def is_valid_filetype(self):
        # Get the file extension
        file_name = self.file_name.split(".")
        try:
            file_type = file_name[1]
        except IndexError:
            raise IndexError("Error: No file extension found.")
        return file_type in txt_file_types

    # Read the file contents provided it's a valid type
    def read_file(self):
        valid = self.is_valid_filetype()
        if not valid:
            raise Exception("Error: Invalid file type. " + str(txt_file_types) + " expected.")
        try:
            txt_file = open(self.file_name, "r")
        except IOError:
            raise IOError("Error: File does not exist.")
        return txt_file.read()

    # Process the text into an array of lines containing an array of words for easier processing
    def __construct_word_array(self):
        if self.is_file:
            file_contents = self.read_file()
        else:
            file_contents = self.file_name
        # Record the character frequency including punctuation
        self.__calc_char_frequency(file_contents)

        # Split the lines by newline character
        file_lines = file_contents.splitlines()

        for line in file_lines:
            # Remove all punctuation
            line = line.translate(None, string.punctuation)
            self.file_lines.append(line.split())

    def __calc_char_frequency(self, file_contents):
        for char in file_contents:
                if char in self.__char_frequency:
                    self.__char_frequency[char] += 1
                else:
                    self.__char_frequency[char] = 1

    def get_word_count(self):
        if self.__word_count is None:
            self.__word_count = 0
            for line in self.file_lines:
                self.__word_count += len(line)
        return self.__word_count

    def get_line_count(self):
        return len(self.file_lines)

    def get_most_common_letter(self):
        if self.__most_common_letters is None:
            self.__most_common_letters = []
            max_count = 0
            for char, value in self.__char_frequency.iteritems():
                if char in string.ascii_lowercase:
                    try:
                        # Sum with the upper character frequency value
                        value = value + self.__char_frequency[char.upper()]
                    except KeyError:
                        pass
                    if value > max_count:
                        self.__most_common_letters_frequency = value
                        max_count = value
                        self.__most_common_letters = [char]
                    elif value == max_count:
                        self.__most_common_letters.append(char)
        return self.__most_common_letters

    def get_avg_no_letters(self):
        if self.__avg_no_letters is None:
            self.__avg_no_letters = 0.0
            sum_letters = 0.0
            word_count = self.get_word_count()
            for line in self.file_lines:
                for word in line:
                    word_length = len(word)
                    sum_letters += word_length
            # File might be empty
            if word_count != 0:
                self.__avg_no_letters = round(sum_letters / word_count, 1)
        return self.__avg_no_letters

    def print_stats(self):
        if len(self.file_lines) == 0:
            print "File is empty"
            return
        print "The statistics for this file are:"
        print "The word count is " + str(self.get_word_count())
        letters = self.get_most_common_letter()
        if len(letters) == 1:
            print "The most common letter is %s occuring %s times." % (str(letters[0]),
                                                                       self.__most_common_letters_frequency)
        else:
            print "The most common letters are %s occuring %s times " % ((str(letters).strip('[]\'').replace("'", "")),
                                                                         self.__most_common_letters_frequency)
        print "The average number of letters per word is " + str(self.get_avg_no_letters())
        print "The line count is " + str(self.get_line_count())

class Test(unittest.TestCase):
    def setUp(self):
        self.builder = FileReader('Document.txt')

    def testRunner(self):
        self.builder.print_stats()

    # Generate random string for testing
    def generateString(self, letter_count, word_count):
        alphabet = string.uppercase + string.lowercase
        text = ""
        line_count = 1

        while word_count > 0:
            new_word = "".join(random.sample(alphabet, letter_count))
            if random.randrange(0, 5) == 0:
                text = text + new_word + '\n'
                if word_count != 1:
                    line_count += 1
            else:
                text = text + new_word + " "
            word_count -= 1
        return text, line_count

    def runSingleTest(self):
        word_count = random.randrange(0, 1000)
        if word_count == 0:
            letter_count = 0
        else:
            letter_count = random.randrange(1, 5)

        text_line_count = self.generateString(letter_count, word_count)
        text = text_line_count[0]
        line_count = text_line_count[1]
        file_lines = FileReader(text, is_file=False)
        assert file_lines.get_word_count() == word_count
        assert file_lines.get_line_count() == line_count
        assert file_lines.get_avg_no_letters() == letter_count

    def testStatistics(self):
        no_of_runs = 100
        while no_of_runs > 0:
            self.runSingleTest()
            no_of_runs -= 1

if __name__ == "__main__":
    if len(sys.argv) == 2:
        text = FileReader(sys.argv[1])
        text.print_stats()

