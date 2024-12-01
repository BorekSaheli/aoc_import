import os
import requests
from bs4 import BeautifulSoup
import inspect

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
        soup = BeautifulSoup(response.text, "html.parser")
        examples = soup.find_all("pre")
        if examples:
            with open(example_path, "w") as f:
                f.write(examples[0].text.strip())
            print("Example input extracted successfully.")
            return examples[0].text.strip()
        else:
            print("No example input found.")
    else:
        print(f"Failed to retrieve problem page. Status code: {response.status_code}")





