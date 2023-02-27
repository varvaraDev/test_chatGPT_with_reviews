"""
no passing API KEY
no typing
no handle errors
"""

import os
import pandas as pd
import openai

# Set up logging
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

file_handler = logging.FileHandler('../tests_and_improvments/analyze_directory.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def analyze_review(review, engine="text-davinci-002"):
    # Analyze the sentiment of the review
    prompt = f"Rate this review from 1 to 10 based on the tone:\n\n{review}\n\nRating:"
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=1,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Extract the rating from the response
    rating = int(response.choices[0].text.strip())
    return rating


def analyze_file(filename):
    # Read the CSV file into a pandas DataFrame
    with open(filename, 'r') as f:
        df = pd.read_csv(f)

    # Analyze the review tone and assign a rating
    df["rating"] = df["review text"].apply(analyze_review)

    # Sort by rating in descending order
    df = df.sort_values("rating", ascending=False)

    # Write the results to a new file with _analyzed.csv suffix
    new_filename = filename.replace(".csv", "_analyzed.csv")
    with open(new_filename, 'w') as f:
        df.to_csv(f, index=False)

    return new_filename


def analyze_directory(directory, engine="text-davinci-002"):
    # Get a list of CSV files in the directory
    files = [f for f in os.listdir(directory) if f.endswith(".csv")]

    # Analyze each file and print results
    for filename in files:
        logger.info(f"Analyzing {filename}...")
        try:
            new_filename = analyze_file(os.path.join(directory, filename))
            logger.info(f"Results saved to {new_filename}")
        except Exception as e:
            logger.exception(f"Failed to analyze {filename}: {e}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="The directory to analyze.")
    parser.add_argument("--engine", default="text-davinci-002", help="The OpenAI GPT engine to use for the analysis.")
    args = parser.parse_args()

    analyze_directory(args.directory, args.engine)
