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
    examples = extract_examples(problem_url, output_dir)

    return input_txt, examples

def download_input(input_url, output_dir):
    input_path = os.path.join(output_dir, "input.txt")
    if os.path.exists(input_path):
        print("input.txt already exists. Skipping download.")
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

def extract_examples(problem_url, output_dir):
    example1_path = os.path.join(output_dir, "example1.txt")
    example2_path = os.path.join(output_dir, "example2.txt")
    examples = []
    if os.path.exists(example1_path):
        print("example.txt already exists. Skipping extraction.")
        with open(example1_path, "r") as f:
            examples.append(f.read().strip())
    if os.path.exists(example2_path):
        print("example_part_two.txt already exists. Skipping extraction.")
        with open(example2_path, "r") as f:
            examples.append(f.read().strip())

    if len(examples) == 2:
        return examples

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
            if len(examples) == 0 and len(parser.examples) >= 1:
                with open(example1_path, "w") as f:
                    f.write(parser.examples[0])
                examples.append(parser.examples[0])
                print("Example input for Part One extracted successfully.")
            if len(parser.examples) >= 2:
                with open(example2_path, "w") as f:
                    f.write(parser.examples[1])
                examples.append(parser.examples[1])
                print("Example input for Part Two extracted successfully.")
            else:
                print("No example input for Part Two found.")
            return examples
        else:
            print("No example inputs found.")
            return examples
    else:
        print(f"Failed to retrieve problem page. Status code: {response.status_code}")
        return examples
