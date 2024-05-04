import openai
from sec_api import ExtractorApi

openai.api_key = "API_KEY_HERE"
extractorApi = ExtractorApi("API_KEY_HERE")

#My API Key- 5b0e8de482a9c0852530401777de33e510d536c75e1d4f7ea1ee2702946a7282

filing_url = "https://www.sec.gov/Archives/edgar/data/1652044/000165204423000016/goog-20221231.htm"

section_text = extractorApi.get_section(
  filing_url, 
  "1A", 
  "text"
)

prompt = f"Summarize the following text in 25 sentences:\n{section_text}"

response = openai.Completion.create(
  engine="text-davinci-003", 
  prompt=prompt
)

print(response["choices"][0]["text"])

section_text = extractorApi.get_section(
  filing_url, 
  "8", 
  "text"
)

prompt = f"Summarize the following text in 25 sentences:\n{section_text}"

response = openai.Completion.create(
  engine="text-davinci-003", 
  prompt=prompt
)

print(response["choices"][0]["text"])