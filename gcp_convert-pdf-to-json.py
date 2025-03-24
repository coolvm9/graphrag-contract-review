import os
from vertexai import init
from vertexai.preview.generative_models import GenerativeModel, GenerationConfig
from PyPDF2 import PdfReader
from env_loader_util import load_env, get_env_variable

# Load environment variables
load_env()

# Load GCP project details
PROJECT_ID = get_env_variable("GCP_PROJECT_ID")
LOCATION = get_env_variable("GCP_LOCATION") or "us-central1"

# Initialize Vertex AI client
init(project=PROJECT_ID, location=LOCATION)

# Load system and extraction prompts
with open("system_prompt.txt", "r") as f:
    system_prompt = f.read()

with open("contract_extraction_prompt.txt", "r") as f:
    extraction_prompt = f.read()

# Read text from PDF
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

pdf_path = "./data/input/sample.pdf"
pdf_text = extract_text_from_pdf(pdf_path)

# Compose full prompt
full_prompt = f"{system_prompt}\n\n{extraction_prompt}\n\nContract:\n{pdf_text}"

# Initialize Gemini model
model = GenerativeModel("gemini-1.5-flash-001")

# Generate content
response = model.generate_content(
    [full_prompt],
    generation_config=GenerationConfig(
        temperature=0.1,
        top_p=1.0,
        top_k=40,
        max_output_tokens=2048
    )
)

# Save the response
output_dir = "./data/output/"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, f"{os.path.basename(pdf_path)}_gcp.json")

with open(output_path, "w", encoding="utf-8") as f:
    f.write(response.text)

print(f"✅ Extracted JSON saved to: {output_path}")
