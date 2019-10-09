import glob
import os
import pprint as pp
import sys
import re


def main(args):
    path = args[1]
    file_paths = glob.glob(path + "/*")
    # pp.pprint(file_paths)

    years = re.compile(r"20[0-9][0-9]")
    types = re.compile(r"(test|exam|ct)([ _]*[1-9])*")
    coursecodes = re.compile(r"[a-z]{3}[0-9]{4}([fswhz])")

    all_years = set()

    all_types = set()
    all_coursecodes = set()

    for file_path in file_paths:
        filename = file_path.split(os.sep)[-1].lower()

        # Figure out the test type & number
        match = re.search(types, filename)
        if match:

            all_types.add(re.sub(r"(test|ct)[_]?[0-9]?", "test ", match.group(0)))
        else:
            pp.pprint("Error: " + filename)

        # Figure out the year
        match = re.search(years, filename)
        if match:
            all_years.add(match.group(0))
        else:
            pp.pprint("Error: " + filename)
    pp.pprint(all_types)
    pp.pprint(all_years)

    # for type in all_types:
    #     for year in all_years:
    #         os.makedirs(os.path.join(path, make_proper(type), make_proper(year)), exist_ok=True)


def make_proper(text: str):
    answers = re.compile(r"(memo|memorandum|sol|answers)")
    supp = re.compile(r"(supp|supplementary)")
    text = text.replace("_", " ").title()
    text = re.sub(answers, "MEMO", text)
    text = re.sub(supp, "SUPP", text)
    return text


if __name__ == '__main__':
    main(sys.argv)


