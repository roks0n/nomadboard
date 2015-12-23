import re

VALID_TAGS = [
    'reactjs', 'emberjs', 'angularjs', 'javascript', 'nodejs', 'meteorjs', 'ajax', 'flux',

    'ruby', 'ror', 'ruby on rails',

    'python', 'flask', 'django',

    'java',

    'php', 'wordpress', 'drupal', 'laravel', 'zend', 'symfony',

    'sql', 'rest', 'api', 'bigdata', 'aws', 'go', 'rust', 'mongodb', 'redis',

    'c++', 'c#', 'scala', 'go', 'swift', 'erlang'

    'html', 'css', 'html', 'css', 'mysql', 'nosql', 'docker',

    'frontend', 'backend', 'fullstack', 'devops', 'ops', 'ios', 'android', 'ux', 'ui',
    'data science', 'admin', 'machine learning', 'qa', 'engineer', 'elasticsearch', 'C',
    'objective-c', 'analyst', 'security', 'saas', 'cloud', 'linux', 'scrum', 'data',

    'oss',

    'operations support systems', 'dev ops', 'c plus plus', 'es',
    'quality assurance', 'java script',

]

KEYWORD_MAPPING = {
    'ruby on rails': 'ror',
    'operations support systems': 'oss',
    'dev ops': 'devops',
    'c plus plus': 'c++',
    'es': 'elasticsearch',
    'elastic search': 'elasticsearch',
    'quality assurance': 'qa',
    'objective c': 'objective-c',
    'objectivec': 'objective-c',
    'js': 'javascript',
    'java script': 'javascript'
}


def normalize_string(input):
    """
    Normalizes a given string into something with which we can work with.

    Args:
        input: string

    Returns: string

    """
    string = input.lower().replace('-', '').replace('/', ' ')
    normalized_spaces = ' '.join(string.strip('').split())
    return normalized_spaces


def extract_tags(input):
    """
    Extract tags from a given string

    Args:
        input:

    Returns: list of tags

    """
    tags = []
    normalized_string = normalize_string(input)
    for tag in VALID_TAGS:
        if re.findall(r'\b{}\b'.format(re.escape(tag)), normalized_string):
            tags.append(tag)
    return tags


def normalize_tags(list):
    """
    Normalize a list of tags

    Args:
        list: list of tag(s)

    Returns: list of normalized tag(s)

    """
    return [KEYWORD_MAPPING[tag] if tag in KEYWORD_MAPPING else tag for tag in list]


def extract_and_normalize_tags(input):
    tags = extract_tags(input)
    return normalize_tags(tags)
