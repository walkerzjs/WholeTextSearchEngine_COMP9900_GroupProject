import modules.utilities as utilities
import modules.html_parser as html_parser

hp = html_parser.html_parser()


def keyword_content(keyword):

    all_files = 'static/outfiles'
    all_names = 'static/filenames'

    all_contents = utilities.load_file(all_files)
    all_names = hp.load_filenames_not_first(all_names)

    results = []

    for i in range(len(all_contents)):
        if keyword.lower() in all_contents[i].lower():
            results.append(all_names[i])

    return results


def keyword_title(keyword):
    all_names = 'static/filenames'
    all_names = hp.load_filenames_not_first(all_names)
    results = []

    for i in range(len(all_names)):
        if all_names[i][1] is None: continue
        if keyword.lower() in all_names[i][1].lower():
            results.append(all_names[i])

    return results
