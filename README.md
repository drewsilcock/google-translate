google-translate
================

Description
-----------

This is a simple Python script to leverage Google's very useful Translate to translate a phrase, given by the user, from and into languages of the user's choice (given that Google Translate supports them).

Motivation
----------

The Google Translate API is a paid service, but you can easily use Google to translate your phrases without using the API. This is exactly what this does.

Installation
------------

It uses standard Python distribution utilities, so it's as simple as doing this:

```bash
$ git clone https://github.com/drewsberry/google-translate.git

$ cd google-translate

$ python setup.py install
```

Usage
-----

Well, you can always run `python google_translate.py --help` to get more help, but here's how you'd basically use it:

```bash
$ python google_translate.py "dog" --from "English" --to "Mongolian"
```

You could also use it as part of another Python program:

```python
>>> from google_translate.google_translate import translate

>>> my_phrase = "Hund"

>>> from_lang = "German"

>>> to_lang = "Chinese"

>>> translate(my_phrase, from_lang, to_lang)
```

How It Works
------------

Essentially, this program does two things:

* Uses `urllib2` to make a connection to Google and requests the page corresponding to the query giving the translation we want, spoofing the Chrome browser user agent; and
* Uses Beautiful Soup to parse the resulting HTML and identify the elements that are always used to contain the translation, then extracts them.

It's basically a very simple web scraper.

Features
--------

* If the program detects that the phrase has been translated to a non-roman alphabet language, then it returns both the true translation and the romanisation of the translation.

Todo
----

* Give option to also give "more translations"
* Give option to return/print Unicode code.
* More rigorously test of all the different options.
