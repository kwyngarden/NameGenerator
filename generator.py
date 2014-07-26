#!/usr/bin/python
from argparse import ArgumentParser
from math import floor
from nltk.util import bigrams
from optparse import OptionParser
from random import choice, normalvariate, random, sample

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
VOWEL_GROUP_MAX_LEN = 2
CONSONANT_GROUP_MAX_LEN = 3
MIN_NUM_GROUPS = 3
MAX_NUM_GROUPS = 7

START_VOWEL_PROB = 0.425 # Historically accurate for US first names
LAST_NAME_LENGTH_EXTENSION = 0.5
DEFAULT_MEAN_NUM_GROUPS = 4.5
MEAN_GROUPS_OPTION_ADJUSTMENT = 1.0


class NameGeneratorModel:
    
    def _add_char_bigram(self, first, second):
        following_chars = self.bigram_map.get(first, [])
        following_chars.append(second)
        self.bigram_map[first] = following_chars

    def get_start_group(self, use_vowels):
        if use_vowels:
            return choice(self.start_groups_vowels)
        else:
            return choice(self.start_groups_consonants)

    def get_group_following(self, letter):
        next_letter = choice(self.bigram_map.get(letter))
        group_list = self.consonant_groups if letter in VOWELS else self.vowel_groups
        return choice([group for group in group_list if group.startswith(next_letter)])

    def get_end_group_following(self, letter):
        next_letter = choice(self.bigram_map.get(letter))
        group_list = self.end_groups_consonants if letter in VOWELS else self.end_groups_vowels
        return choice([group for group in group_list if group.startswith(next_letter)])
 
    def _process_first_group(self, group, is_vowels):
        if is_vowels:
            self.start_groups_vowels.append(group)
        else:
            self.start_groups_consonants.append(group)

    def _process_word(self, word):
        vowel_groups = []
        consonant_groups = []
        current_group = ''
        current_group_is_vowels = True
        is_first_group = True
        
        for i in range(len(word)):
            if (word[i] in VOWELS) == current_group_is_vowels:
                current_group += word[i]
            elif current_group:
                self._add_char_bigram(current_group[-1], word[i])
                if is_first_group:
                    self._process_first_group(current_group, current_group_is_vowels)
                    is_first_group = False
                if current_group_is_vowels and len(current_group) <= VOWEL_GROUP_MAX_LEN:
                    self.vowel_groups.append(current_group)
                elif not current_group_is_vowels and len(current_group) <= CONSONANT_GROUP_MAX_LEN:
                    self.consonant_groups.append(current_group)
                current_group_is_vowels = not current_group_is_vowels
                current_group = '' + word[i]
            else:
                current_group_is_vowels = not current_group_is_vowels
                current_group = '' + word[i]
        
        if current_group_is_vowels:
            if len(current_group) <= VOWEL_GROUP_MAX_LEN:
                self.vowel_groups.append(current_group)
            self.end_groups_vowels.append(current_group)
        else:
            if len(current_group) <= CONSONANT_GROUP_MAX_LEN:
                self.consonant_groups.append(current_group)
            self.end_groups_consonants.append(current_group)

    def train(self, words):
        self.vowel_groups = []
        self.consonant_groups = []
        self.start_groups_vowels = []
        self.start_groups_consonants = []
        self.end_groups_vowels = []
        self.end_groups_consonants = []
        self.bigram_map = {}

        for word in words:
            self._process_word(word)


def clamp(val, min_val, max_val):
    return min_val if val < min_val else max_val if val > max_val else val

def get_english_words(dict_filename):
    english_dict = open(dict_filename, 'r')
    words = set()
    
    for word in english_dict.readlines():
        word = word.strip()
        # Don't train on short words or capitalized words (proper nouns, etc.)
        if len(word) >= 3 and word.islower():
            words.add(word)
    
    english_dict.close()
    return words

def get_num_letter_groups(mean_groups):
    groups = int(floor(normalvariate(mean_groups, 1.0)))
    return clamp(groups, MIN_NUM_GROUPS, MAX_NUM_GROUPS)

def get_name_component(model, english_words, mean_groups, start_with_vowel):
    num_groups = get_num_letter_groups(mean_groups)
    component = model.get_start_group(start_with_vowel)
    current_group_is_vowels = not start_with_vowel
    for i in range(1, num_groups - 1):
        component += model.get_group_following(component[-1])
        current_group_is_vowels = not current_group_is_vowels
    component += model.get_end_group_following(component[-1])
    return component.capitalize()

def get_title(english_words):
    identifiers = [
        'Captain of the',
        'Commander of the',
        'Defender of the',
        'King beyond the',
        'King in the',
        'King of the',
        'King under the',
        'Knight of the',
        'Lord of the',
        'Master of the',
        'Prince of the',
        'Protector of the',
    ]
    words = sample(english_words, 2)
    return '{identifier} {word1} {word2}'.format(
        identifier=choice(identifiers),
        word1=words[0].capitalize(),
        word2=words[1].capitalize(),
    )

def get_name(model, english_words, num_letter_groups, use_titles):
    first = get_name_component(model, english_words, num_letter_groups, random() < START_VOWEL_PROB)
    last = get_name_component(model, english_words, num_letter_groups + LAST_NAME_LENGTH_EXTENSION, random() < START_VOWEL_PROB)
    full_name = first + ' ' + last
    if use_titles:
        full_name += ', ' + get_title(english_words)
    return full_name

if __name__ == '__main__':
    parser = ArgumentParser(description='Procedural name generator, with optional fun titles appended to the generated names.')
    parser.add_argument('-n', '--num-names', type=int, default=5, help='Number of names to generate')
    parser.add_argument('-t', '--use-titles', action='store_true', help='Append titles to names')
    parser.add_argument('-d', '--large-dict', action='store_true', help='Train name generator with larger dictionary')
    parser.add_argument('-f', '--dict-file', help='Newline-separated dictionary file on which to train names')
    parser.add_argument('-s', '--short-names', action='store_true', help='On average, generate shorter names')
    parser.add_argument('-l', '--long-names', action='store_true', help='On average, generate longer names')
    args = parser.parse_args()

    # Train model on chosen dictionary.
    dict_filename = (
        args.dict_file if args.dict_file 
        else 'large.txt' if args.large_dict
        else 'small.txt'
    )
    english_words = get_english_words(dict_filename)
    model = NameGeneratorModel()
    model.train(english_words)
    
    # Adjust mean number of letter groups per name component to account for
    # command-line arguments (opposing arguments will cancel each other out).
    mean_num_groups = DEFAULT_MEAN_NUM_GROUPS
    if args.short_names:
        mean_num_groups -= MEAN_GROUPS_OPTION_ADJUSTMENT
    if args.long_names:
        mean_num_groups += MEAN_GROUPS_OPTION_ADJUSTMENT
    
    # Print out the requested number of names, one per line.
    for i in range(args.num_names):
        print get_name(model, english_words, mean_num_groups, args.use_titles)
