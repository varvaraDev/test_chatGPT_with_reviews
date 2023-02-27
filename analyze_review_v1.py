"""
I added only the use of the environment variable OPENAI_API_KEY
Result - source_analyzed.csv
"""
import openai
from dotenv import load_dotenv
import csv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def rate_review(review_text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Rate this review from 1 to 10 based on the tone:\n\n{review_text}\n\nRating:",
        temperature=0.5,
        max_tokens=1,
        n=1,
        stop=None,
        timeout=10,
    )
    rating = int(response.choices[0].text)
    return rating


def analyze_file(file_path):
    file_name = os.path.basename(file_path)
    new_file_name = os.path.splitext(file_name)[0] + "_analyzed.csv"
    with open(file_path, "r") as input_file, open(new_file_name, "w", newline="") as output_file:
        reader = csv.DictReader(input_file)
        fieldnames = reader.fieldnames + ["rate"]
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        rows = []
        for row in reader:
            rating = rate_review(row["review text"])
            row["rate"] = rating
            rows.append(row)
        rows = sorted(rows, key=lambda x: x["rate"], reverse=True)
        writer.writerows(rows)


def analyze_directory(directory_path):
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(directory_path, file_name)
            analyze_file(file_path)


if __name__ == '__main__':
    analyze_directory(".")

