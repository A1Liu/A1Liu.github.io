import os # import re # escaped = re.escape(a_string)
from nltk.corpus import stopwords
from scripts.jekyll_utils import get_post_path, make_assets_folder

en_stopwords = set( stopwords.words('english') )

def capitalize_title_word(word):
    if (len(word) > 5 or word not in en_stopwords) and word.upper() != word:
        return word.capitalize()
    return word

def make_post(
    title, display_title=None,date=None, categories=[], tags=[],
    is_draft = True, has_assets = True):

    # Setting up vars
    if display_title is None: display_title = title
    display_title = ' '.join( [capitalize_title_word(word) for word in display_title.split(' ')] )
    output_path = get_post_path(title,date=date,is_draft=is_draft)
    if has_assets: make_blog_assets_folder(title,date)
    
    with open( output_path, 'x') as f:
        f.write('---\n')
        f.write('title: {}\n'.format(display_title))
        f.write('categories: [%s]\n' % ', '.join(categories) )
        f.write('tags: [%s]\n' % ', '.join(tags) )
        f.write('---\n')
