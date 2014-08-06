NameGenerator
=============

For when you need a large number of random but pronounceable names (characters, places, etc). Alternatively, give your friends funny names and titles.

A couple lists of English words used for training are included for convenience. Feel free to substitute your own list (perhaps /usr/share/dict/words on a Unix-like system).

Sample usage
------------
Generate 10 names:
~~~
keithwyngarden$ python generator.py -n 10
Mioblat Fentia
Squttyo Hextia
Nar Reuro
Collyo Rene
Idos Thoundene
Molly Upo
Pes Ror
Alda Rele
Manaty Mede
Petak Anlang
~~~

Use a larger training dictionary and generate longer average names:
~~~
keithwyngarden$ python generator.py -d -l
Shen Fogab
Pyrero Prepie
Ossourably Danateugy
Olapiepo Perizz
Sonsha Geobla
Detizort Reactraoft
Agno Spiofo
Hasse Caflil
Sninonve Enfoscren
Nar Cider
~~~

Now with fun titles!
~~~
keithwyngarden$ python generator.py -t
Stisuss Ampis, Commander of the Bluishness Outbreak
Bungi Dedal, King beyond the Residuary Zany
Inour Dece, King beyond the Radiotelegraph Boustrophedonic
Crerth Gorgen, Lord of the Bezonian Lightning
Beet Cedcunterm, Commander of the Aby Glomeration
Misia Prodor, King in the Versus Quipu
Iseungye Tenge, Defender of the Asclepias Dermoptera
Ciche Heccre, Lord of the Starkly Ophioglossales
Peanoe Hotom, Lord of the Molossidae Goethean
Ainte Platri, Knight of the Stance Thumbscrew
~~~

How it works
------------
A [similar project](http://www.wolfram.com/language/gallery/generate-random-pronounceable-words/) creates random "pronounceable" words using letter bigrams/trigrams.

This program uses an English dictionary to learn groups of adjacent vowels or adjacent consonants that actually appear in English words, then stitches them together (alternating vowel and consonant groups) probabilistically using bigrams.

The number of groups per name is modeled as a normal distribution. The first and last groups in English words are trained separately and used as such in the generated names.

As for the titles? Those are simply two random English words :)
