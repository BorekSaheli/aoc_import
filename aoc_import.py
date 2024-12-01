import os
import requests
import inspect
from html.parser import HTMLParser

SESSION_COOKIE = os.environ.get("AOC_SESSION_COOKIE")

headers = {
    "Cookie": f"session={SESSION_COOKIE}",
    "User-Agent": "Mozilla/5.0 (compatible; AdventOfCodeScript/1.0)",
}

def get_data(year=2024, day=1, output_dir=None):
    if output_dir is None:
        frame = inspect.currentframe()
        caller_frame = inspect.getouterframes(frame)[1]
        caller_file = caller_frame.filename
        output_dir = os.path.dirname(os.path.abspath(caller_file))

    input_url = f"https://adventofcode.com/{year}/day/{day}/input"
    problem_url = f"https://adventofcode.com/{year}/day/{day}"
    input_txt = download_input(input_url, output_dir)
    example1_txt, example2_txt = extract_examples(problem_url, output_dir)

    return input_txt, example1_txt, example2_txt

def download_input(input_url, output_dir):
    input_path = os.path.join(output_dir, "input.txt")
    if os.path.exists(input_path):
        print("input.txt already exists. Loading from file.")
        with open(input_path, "r") as f:
            return f.read().strip()
    response = requests.get(input_url, headers=headers)
    if response.status_code == 200:
        with open(input_path, "w") as f:
            f.write(response.text.strip())
        print("input.txt downloaded successfully.")
        return response.text.strip()
    else:
        print(f"Failed to download input.txt. Status code: {response.status_code}")
        return None

def extract_examples(problem_url, output_dir):
    example1_path = os.path.join(output_dir, "example1.txt")
    example2_path = os.path.join(output_dir, "example2.txt")
    example1_txt = None
    example2_txt = None

    # Check if example1.txt exists
    if os.path.exists(example1_path):
        print("example1.txt already exists. Loading from file.")
        with open(example1_path, "r") as f:
            example1_txt = f.read().strip()
    # Check if example2.txt exists
    if os.path.exists(example2_path):
        print("example2.txt already exists. Loading from file.")
        with open(example2_path, "r") as f:
            example2_txt = f.read().strip()
    # If both examples exist, return them
    if example1_txt is not None and example2_txt is not None:
        return example1_txt, example2_txt

    # Else, proceed to parse the problem page
    response = requests.get(problem_url, headers=headers)
    if response.status_code == 200:
        class ExampleHTMLParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.in_article = False
                self.in_pre = False
                self.examples = []
                self.current_example = ''

            def handle_starttag(self, tag, attrs):
                if tag == 'article':
                    self.in_article = True
                elif tag == 'pre' and self.in_article:
                    self.in_pre = True

            def handle_endtag(self, tag):
                if tag == 'pre' and self.in_pre:
                    self.in_pre = False
                    self.examples.append(self.current_example.strip())
                    self.current_example = ''
                elif tag == 'article':
                    self.in_article = False

            def handle_data(self, data):
                if self.in_pre:
                    self.current_example += data

        parser = ExampleHTMLParser()
        parser.feed(response.text)

        if parser.examples:
            if example1_txt is None and len(parser.examples) >= 1:
                example1_txt = parser.examples[0]
                with open(example1_path, "w") as f:
                    f.write(example1_txt)
                print("example1.txt downloaded successfully.")
            if example2_txt is None and len(parser.examples) >= 2:
                example2_txt = parser.examples[1]
                with open(example2_path, "w") as f:
                    f.write(example2_txt)
                print("example2.txt downloaded successfully.")
            if example1_txt is None:
                print("No example input found.")
            return example1_txt, example2_txt
        else:
            print("No example inputs found.")
            return example1_txt, example2_txt
    else:
        print(f"Failed to retrieve problem page. Status code: {response.status_code}")
        return example1_txt, example2_txt
