"""
There I fixed prompt to be the same as in the snippet from first_solution.py
Result - ./data/Task2 - Data_analyzed.csv
"""

import openai
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()
# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


# Define function to analyze review tone
def analyze_review(review):
    response = openai.Completion.create(
        engine="text-davinci-002",
        # prompt=(f"Rate this review on a scale of 1-10 based on tone: {review}"),
        prompt=f"Rate this review from 1 to 10 based on the tone:\n\n{review}\n\nRating:",
        max_tokens=1,
        n=1,
        stop=None,
        temperature=0.5,
    )

    rating = int(response.choices[0].text)
    return rating


# Define function to read file, analyze reviews, and write results
def analyze_file(filename):
    # Read CSV file into pandas DataFrame
    df = pd.read_csv(filename)

    # Analyze review tone and assign rating
    df["rate"] = df["review text"].apply(analyze_review)

    # Sort by rating in descending order
    df = df.sort_values("rate", ascending=False)

    # Write results to new file with _analyzed.csv suffix
    new_filename = filename.replace(".csv", "_analyzed.csv")
    df.to_csv(new_filename, index=False)

    return new_filename


# Define function to analyze all files in directory
def analyze_directory(directory):
    # Get list of CSV files in directory
    files = [f for f in os.listdir(directory) if f.endswith(".csv")]

    # Analyze each file and print results
    for file in files:
        print(f"Analyzing {file}...")
        new_filename = analyze_file(os.path.join(directory, file))
        print(f"Results saved to {new_filename}")


# Call analyze_directory function on directory of choice
analyze_directory("./data")
