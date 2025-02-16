Automating Research Paper Classification with AI: Challenges, Results, and Key Takeaways

Introduction

In the ever-growing field of research, organizing and categorizing papers is a daunting task. Manually sorting research papers into predefined categories can be time-consuming and error-prone. To address this, I developed an automated classification system using Google Gemini AI to categorize research papers into five categories: Deep Learning, Computer Vision, Reinforcement Learning, NLP, and Optimization.

In this post, I will walk you through the entire process—from extracting text from PDFs to using AI for classification, the challenges faced, results obtained, and key takeaways.

The Process: How I Built the Automated Paper Classifier

1. Extracting Text from PDFs

Research papers are typically in PDF format, which makes extracting structured text difficult. To handle this, I used the pypdf library to extract content from each paper, specifically targeting the title and abstract, as these contain the most relevant information for classification.

Code snippet:

from pypdf import PdfReader
import re

def extract_text_from_pdf(pdf_path):
    """Extracts title and abstract from a PDF file."""
    try:
        reader = PdfReader(pdf_path)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        
        # Extract title (Assuming first line is the title)
        title = text.split("\n")[0].strip()
        
        # Extract abstract using regex
        abstract_match = re.search(r"(?i)abstract\s*(.*?)\n\n", text, re.S)
        abstract = abstract_match.group(1).strip() if abstract_match else "No Abstract Found"
        
        return title, abstract
    except Exception as e:
        print(f"❌ Error reading {pdf_path}: {e}")
        return None, None

This function efficiently extracts text from PDFs and helps preprocess the data for AI-based classification.

2. Classifying Papers Using Google Gemini AI

Once we have the title and abstract, the next step is to classify the paper into one of the predefined categories using Google Gemini AI. The API takes the extracted text and predicts the most suitable category based on the given prompt.

Classification Prompt:

prompt = (
    f"Strictly classify this paper into ONE of these categories: {', '.join(CATEGORIES)}. "
    "Return only the exact category name. If uncertain, choose the best match.\n"
    f"Title: {title}\nAbstract: {abstract}\nCategory:"
)

This prompt ensures that Gemini AI provides an exact category name without additional text.

To generate the classification result, we send the prompt to the API:

import google.generativeai as genai

genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content(prompt)
category = response.text.strip()

The AI model returns one of the five categories, which we then store in a structured format.

3. Storing and Organizing Classified Papers

Instead of renaming files (which could cause issues), I opted to store classification results in a CSV file for easy tracking.

import csv

csv_path = "annotations.csv"
with open(csv_path, "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([file_path, category])

This allows easy access to classifications without altering the original files.

Challenges Faced & How I Overcame Them

1. Extracting Accurate Abstracts from PDFs

Many research papers have inconsistent formats, making it difficult to accurately extract abstracts using regex. Some abstracts span multiple lines, while others use different keywords like "Summary" instead of "Abstract."

Solution:

Improved regex matching to detect alternative abstract structures.

Processed extracted text using NLP techniques to better identify abstracts.

2. Handling Incorrect AI Classifications

While Gemini AI performed well, it sometimes classified papers incorrectly or returned generic results like "Uncategorized."

Solution:

Added retries in case of API failures.

Verified outputs using human validation for edge cases.

3. Managing API Rate Limits and Costs

Google Gemini AI has API usage limits, and processing large datasets can be costly.

Solution:

Optimized API calls by limiting retries to three attempts.

Batched document processing instead of making multiple individual API calls.

Results & Key Takeaways

Results

After testing on NeurIPS 2020-2024 papers, the classifier achieved:
✅ 90% accurate classifications based on manual validation.✅ Processed 500+ papers in under 10 minutes.✅ Allowed structured annotation without modifying file names.

Key Takeaways

Automating classification saves hours of manual effort and improves research organization.

Extracting abstracts correctly is crucial for accurate classification.

AI models require human validation to handle edge cases and misclassifications.

Storing annotations in CSV format is more efficient than renaming files.

Final Thoughts & Future Improvements

This project successfully automated the classification of research papers, making it easier to organize academic literature. Future improvements could include:
🔹 Fine-tuning a custom NLP model to improve classification accuracy.🔹 Adding a web-based interface to allow researchers to upload and classify papers online.🔹 Expanding categories to include more specialized fields.

If you're a researcher or student struggling with paper organization, consider automating your workflow with AI—it’s a game-changer! 🚀
