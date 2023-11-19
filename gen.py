# app.py

from flask import Flask, render_template, request
from flask_cors import CORS
import openai  # Import the OpenAI library

app = Flask(__name__)
CORS(app)

# Set your OpenAI API key
openai.api_key = "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"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_email', methods=['POST'])
def generate_email():
    if request.method == 'POST': 
        your_name = request.form['your_name']
        leads_name = request.form['leads_name']
        lead_title = request.form['lead_title']
        leads_company = request.form['leads_company']
        company_size = request.form['company_size']
        sector = request.form['sector']
        interested_in = request.form['interested_in']
        pain_point = request.form['pain_point']
        form_prompt = f"Your Name: {your_name}\nLeads Name: {leads_name}\nLead Title: {lead_title}\nLeads Company: {leads_company}\nCompany Size: {company_size}\nSector: {sector}\nInterested In: {interested_in}\nTheir Pain Point: {pain_point}"
        
        baseline_prompt = """
AI assistant, your task is to compose a reply to a potential lead who has filled in a web form. Make sure to thank them for reaching out at the start of the email. The email you're drafting should be a introduction that clearly encapsulates our identity, the nature of our operations, and how our product/service can be of benefit. 
The tone of the email should align perfectly with our Brand Voice, which is defined as "professional and informative, demonstrating an expert authoritative tone." The text should be both friendly and inviting, with a clear demonstration of empathy and inclusivity. This tone should serve to assure the recipient of our commitment to quality and reliability.  
The brand persona that should come across is that of a knowledgeable and reliable guide whose main goal is to enrich user skills and promote fair, inclusive hiring practices. Don't use the word "Pain Point" within the email, instead use words like challenges. You are only allowed to use up to 125 words.
The language used should be clear, straightforward, and engaging, with a strong emphasis on accessible education and the empowerment of the user.
The email should highlight that our company (SocialTalent) specializes in creating high-quality actionable learning content that addresses C-suite problems across various domains, including Hiring (Recruiting, Interviewing, and Interview prep for candidates), Onboarding, DEI, Leadership, and Internal Mobility.
It can also mention that our learning library is beneficial for every career and skill level, from individual contributors to senior leaders.
Lastly, communicate that our learning platform is easy to buy, deploy, and use - at scale. Keep the writing engaging, informative, and professional, reflecting our brand persona and values. 
"Your Name" refers to the Sales rep. "Length of Email" refers to how long the email should be. 
You should always mention our company name "SocialTalent". Please include any relevant information you have on the problems that the selected industry could be experiencing. 
"Company Size" refers to how many employees work within "Leads Company" be sure to mention this.
The information following this is both information about the lead, but also information about the sales rep who is filling in a form to generate this email.
"""
        
        full_prompt = baseline_prompt + form_prompt

        # Make a request to the OpenAI GPT-3 API using the new interface
        response = openai.completions.create(
            model="text-davinci-002",  # Choose the engine based on your needs
            prompt=full_prompt,
            max_tokens=400  # Adjust as needed
        )

        # Extract the generated content from the API response
        generated_content = response.choices[0].text

        return render_template('result.html', prompt=full_prompt, generated_content=generated_content)

if __name__ == '__main__':
    app.run(debug=True)
