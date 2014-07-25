from math import floor
from nltk.util import bigrams
from random import choice, normalvariate, random, sample

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
VOWEL_GROUP_MAX_LEN = 2
CONSONANT_GROUP_MAX_LEN = 3

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

    def get_end_group_following(self, letter):
        next_letter = choice(self.bigram_map.get(letter))
        group_list = self.end_groups_consonants if letter in VOWELS else self.end_groups_vowels
        return choice([group for group in group_list if group.startswith(next_letter)])
        

    def get_group_following(self, letter):
        next_letter = choice(self.bigram_map.get(letter))
        group_list = self.consonant_groups if letter in VOWELS else self.vowel_groups
        return choice([group for group in group_list if group.startswith(next_letter)])

    def _process_first_group(self, group, is_vowels):
        if is_vowels:
            self.start_groups_vowels.append(group)
        else:
            self.start_groups_consonants.append(group)

    def _get_letter_groupings_and_bigrams(self, word):
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
            self._get_letter_groupings_and_bigrams(word)


def get_english_words(dict_filename):
    english_dict = open(dict_filename, 'r')
    words = set()
    for word in english_dict.readlines():
        word = word.strip()
        if word.islower() and len(word) >= 3:
            words.add(word)
    english_dict.close()
    return words

def get_num_letter_groups(mean_groups):
    groups = int(floor(normalvariate(mean_groups, 1.5)))
    return 3 if groups < 3 else 7 if groups > 7 else groups

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
        'King of the',
        'Protector of the',
        'Knight of the',
        'Lord of the',
        'Master of the',
        'Defender of the',
        'Prince of the',
        'Captain of the',
        'Commander of the',
        'King under the',
        'King beyond the',
        'King in the',
    ]
    words = sample(english_words, 2)
    return '{identifier} {word1} {word2}'.format(
        identifier=choice(identifiers),
        word1=words[0].capitalize(),
        word2=words[1].capitalize(),
    )

def get_name(model, english_words, use_titles):
    first = get_name_component(model, english_words, 4.25, random() < 0.45)
    last = get_name_component(model, english_words, 5, choice([True, False]))
    full_name = first + ' ' + last
    if use_titles:
        full_name += ', ' + get_title(english_words)
    return full_name

if __name__ == '__main__':
    names_to_generate = 10
    use_titles = True
    dict_size = 'small'

    english_words = get_english_words(dict_size + '.txt')
    model = NameGeneratorModel()
    model.train(english_words)

    for i in range(names_to_generate):
        print get_name(model, english_words, use_titles)
