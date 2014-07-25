from nltk.util import bigrams
from random import choice, sample

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'

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
                if current_group_is_vowels:
                    self.vowel_groups.append(current_group)
                else:
                    self.consonant_groups.append(current_group)
                current_group_is_vowels = not current_group_is_vowels
                current_group = '' + word[i]
            else:
                current_group_is_vowels = not current_group_is_vowels
                current_group = '' + word[i]

    def train(self, words):
        self.vowel_groups = []
        self.consonant_groups = []
        self.start_groups_vowels = []
        self.start_groups_consonants = []
        self.bigram_map = {}

        for word in words:
            if len(word) > 3:
                self._get_letter_groupings_and_bigrams(word)


def get_english_words():
    english_dict = open('words.txt')
    words = set()
    for word in english_dict.readlines():
        words.add(word.strip().lower())
    english_dict.close()
    return words

def get_name_component(model, english_words, num_groups, start_with_vowel):
    component = sample(english_words, 1)[0]
    while component in english_words:
        component = model.get_start_group(start_with_vowel)
        current_group_is_vowels = not start_with_vowel
        for i in range(1, num_groups):
            component += model.get_group_following(component[-1])
            current_group_is_vowels = not current_group_is_vowels
    return component.capitalize()

def get_name(model, english_words):
    first = get_name_component(model, english_words, 4, choice([True, False, False]))
    last = get_name_component(model, english_words, 4, choice([True, False, False]))
    return first + ' ' + last

if __name__ == '__main__':
    names_to_generate = 10
    english_words = get_english_words()
    model = NameGeneratorModel()
    model.train(english_words)

    for i in range(names_to_generate):
        print get_name(model, english_words)




