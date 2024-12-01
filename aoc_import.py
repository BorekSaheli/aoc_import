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
    example = extract_example(problem_url, output_dir)

    return input_txt, example

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

def extract_example(problem_url, output_dir):
    example_path = os.path.join(output_dir, "example.txt")
    if os.path.exists(example_path):
        print("example.txt already exists. Skipping extraction.")
        with open(example_path, "r") as f:
            return f.read().strip()
    response = requests.get(problem_url, headers=headers)
    if response.status_code == 200:
        class ExampleHTMLParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.in_pre = False
                self.example_text = ''
                self.found = False

            def handle_starttag(self, tag, attrs):
                if tag == 'pre' and not self.found:
                    self.in_pre = True

            def handle_endtag(self, tag):
                if tag == 'pre' and self.in_pre:
                    self.in_pre = False
                    self.found = True  # Only capture the first <pre> block

            def handle_data(self, data):
                if self.in_pre:
                    self.example_text += data

        parser = ExampleHTMLParser()
        parser.feed(response.text)
        if parser.example_text:
            with open(example_path, "w") as f:
                f.write(parser.example_text.strip())
            print("Example input extracted successfully.")
            return parser.example_text.strip()
        else:
            print("No example input found.")
    else:
        print(f"Failed to retrieve problem page. Status code: {response.status_code}")
