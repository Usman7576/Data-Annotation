import os
import re
import time
import google.generativeai as genai
from pypdf import PdfReader  # ✅ Import for PDF processing

# Configure Gemini API
API_KEY = "AIzaSyDorprhphVsD7d3yOVhQzLlgPIZz4M3Nok"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

# Categories for classification
CATEGORIES = ["Deep Learning", "Computer Vision", "Reinforcement Learning", "NLP", "Optimization"]

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

def classify_paper(title, abstract, retries=3):
    """Uses Google Gemini API to classify a research paper."""
    prompt = (
        f"Strictly classify this paper into ONE of these categories: {', '.join(CATEGORIES)}. "
        "Return only the exact category name. If uncertain, choose the best match.\n"
        f"Title: {title}\nAbstract: {abstract}\nCategory:"
    )

    model = genai.GenerativeModel("gemini-1.5-flash")

    for _ in range(retries):
        try:
            response = model.generate_content(prompt)
            category = response.text.strip()

            # Debug print to check API response
            print(f"Debug: API returned '{category}'")

            if category in CATEGORIES:
                return category
            return "Uncategorized"
        except Exception as e:
            print(f"API Error: {e}")
            time.sleep(2)
    
    return "Error"

def annotate_papers(folder_path):
    """Processes all PDF papers in the folder and annotates them."""
    files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
    total_files = len(files)
    annotated_files = 0

    if total_files == 0:
        print("❌ No PDF files found in the folder.")
        return

    print(f"✅ Total papers found: {total_files}\n")

    for index, file in enumerate(files, start=1):
        file_path = os.path.join(folder_path, file)
        print(f"🔹 Processing ({index}/{total_files}): {file} ...", end=" ")

        # Extract text
        title, abstract = extract_text_from_pdf(file_path)
        if not title or not abstract:
            print("❌ Skipped (No text found)")
            continue

        # Classify paper
        category = classify_paper(title, abstract)

        if category == "Error":
            print("❌ Failed")
            continue

        # Rename file with category
        new_filename = f"{category}_{file}"
        new_path = os.path.join(folder_path, new_filename)
        os.rename(file_path, new_path)

        annotated_files += 1
        print(f"✅ Annotated as: {category}")

    print(f"\n🎯 Annotation completed: {annotated_files}/{total_files} files processed.")

if __name__ == "__main__":
    base_folder = r"F:\Web Scrapping\nips_papers_2020-2024"

    if os.path.exists(base_folder):
        annotate_papers(base_folder)
    else:
        print(f"❌ Folder not found: {base_folder}")
