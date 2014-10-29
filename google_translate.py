import urllib2
import click
import bs4

languages = ["Afrikaans", "Albanian", "Arabic", "Armenian", "Azerbaijani",
             "Basque", "Belarusian", "Bengali", "Bosnian", "Bulgarian",
             "Catalan", "Cebuano", "Chinese", "Croatian", "Czech", "Danish",
             "Dutch", "English", "Esperanto", "Estonian", "Filipino",
             "Finnish", "French", "Galician", "Georgian", "German", "Greek",
             "Gujarati", "Haitian creole", "Hausa", "Hebrew", "Hindi", "Hmong",
             "Hungarian", "Icelandic", "Igbo", "Indonesian", "Irish",
             "Italian", "Japanese", "Javanese", "Kannada", "Khmer", "Korean",
             "Lao", "Latin", "Latvian", "Lithuanian", "Macedonian", "Malay",
             "Maltese", "Maori", "Marathi", "Mongolian", "Nepali", "Norwegian",
             "Persian", "Polish", "Portuguese", "Punjabi", "Romanian",
             "Russian", "Serbian", "Slovak", "Slovenian", "Somali", "Spanish",
             "Swahili", "Swedish", "Tamil", "Telugu", "Thai", "Turkish",
             "Ukrainian", "Urdu", "Vietnamese", "Welsh", "Yiddish", "Yoruba",
             "Zulu"]


def get_webpage(url, verbose):
    """ Queries Google for the web page containing the translation. """

    chrome_user_agent = """\
        Mozilla/5.0 (Windows NT 6.3; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/37.0.2049.0 Safari/537.36"""

    if verbose:
        print "\nAttempting request to url..."
    request = urllib2.Request(url)
    if verbose:
        print "Request to url completed."

    opener = urllib2.build_opener()
    request.add_header("User-Agent", chrome_user_agent)

    if verbose:
        print "\nDownloading data from url..."
    data = opener.open(request).read()
    if verbose:
        print "Data successfully downloaded from url."

    if debug:
        with open("output.html", "w") as f:
            f.write(data)

    return data


def parse_page(text, verbose):
    """ Parses the web page text for the all important translation. """

    if verbose:
        print "\nParsing web page for translation..."
    soup = bs4.BeautifulSoup(text)
    trans_results = [td.find("span") for td in
                     soup.findAll("pre", {"data-placeholder": "Translation"})]

    roman_results = [td.find("span") for td in
                     soup.findAll("pre", {"id": "tw-target-rmn"})]

    if not trans_results:
        print "Error: No translation found on web page."
        exit(2)

    translation = trans_results[0].text
    if verbose:
        print "Translation successfully found.\n"

    romanisation = roman_results[0].text
    if verbose:
        print "Romanisation successfully found.\n"

    return translation, romanisation


def print_langs(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("Supported languages:\n")
    for lang in languages:
        if lang == languages[-1]:
            click.echo(lang + ".")
        else:
            click.echo(lang + ", ")
    ctx.exit()


@click.command()
@click.argument("phrase")
@click.option("-f", "--from", "_from", default="English",
              help="The language to translate from.")
@click.option("-t", "--to",
              prompt="Please enter the language you'd like to translate to",
              help="The language to translate to.")
@click.option("-l", "--languages", is_flag=True, callback=print_langs,
              expose_value=False, is_eager=True, default=False)
@click.option("-v", "--verbose", is_flag=True)
@click.option("-d", "--debug", is_flag=True
def translate(phrase, _from, to, verbose, debug):
    """ Translate words from one language to another using Google Translate."""

    _from = _from.lower().capitalize()
    to = to.lower().capitalize()

    if _from not in languages or to not in languages:
        print "Error: language {} not supported. See `translate.py --langs`"
        print "       for all supported languages."
        exit(1)

    if not _from:
        if verbose:
            print ("\nTranslating {} to {} using autodetect..."
                   .format(phrase, to))
        query = "translation+{}+to+{}".format(phrase, to).replace(" ", "+")
    else:
        if verbose:
            print "\nTranslating {} from {} to {}...".format(phrase, _from, to)
        query = ("translate+{}+from+{}+to+{}"
                 .format(phrase, _from, to).replace(" ", "+"))

    url = "https://google.co.uk/search?q=" + query

    text = get_webpage(url, verbose)

    translation, romanisation = parse_page(text, verbose, debug)

    print "Translation:", translation
    if romanisation:
        print "Romanisation:", romanisation

    return translation


if __name__ == "__main__":
    translate()
