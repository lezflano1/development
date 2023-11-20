# gen.py

from flask import Flask, render_template, request
from flask_cors import CORS
import openai  # Import the OpenAI library
from google.cloud import secretmanager_v1

# Retrieve the API key from environment variables
api_key = os.getenv("OpenAPI")

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_email', methods=['GET', 'POST'])
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
    As a sales development representative, your task is to compose an introductory email response, not exceeding 125 words but try your best to keep them short, to a potential client who has reached out via our website. The email should not be longer than 125 words or it will ruin everything. Begin with expressing gratitude for their interest.  

Replace "Pain Point" with "challenges". Incorporate relevant information about the challenges faced by the potential client's industry and the size of their company. Substitute "Your Name" and "Company Size" with appropriate sales representative information and the potential client's company size. We don't sell courses so don't mention them.

Here is our full elevator pitch, please use it to help form this email. "I work for a company called SocialTalent, a market-leading learning platform that helps organizations to build high-performing, work-smart teams.
What does that mean? Our learning library is packed with actionable, bite-sized training videos, delivered by leading experts in Recruiting, Interviewing, Leadership, DEI, and Internal Mobility. We want to make every employee work-smart regardless of their career level or learning style.
We work with industry giants, like Cisco, CVS, Amazon, and HelloFresh, to deliver learning to millions of users. Our content consistently receives high user satisfaction scores, with an industry-beating course completion rate of over 87%
Organizations come to us when they want to solve critical workplace challenges. Let me explain what I mean.
Nearly 8 out of 10 organizations are struggling to hire talent right now.  That’s the highest % ever surveyed. We address this challenge by providing training for every stakeholder in the hiring process - the recruiters, the hiring managers, and the candidates -  helping to build a culture of hiring excellence.
The second need is about retaining and getting the most out of existing talent. Hiring the right talent is just the first step. Employee engagement leads to retention, increased productivity, and innovation. Whether an employee stays and prospers or leaves and sends us back to square one is 80% down to the leader they work under. We upskill leaders on how to hire, onboard, develop, and lead their teams to succeed, with an extra emphasis on how to succeed when managing hybrid or remote teams. 
While inclusive hiring is essential, great companies know that DEI goes beyond recruitment. We've made DEI a central focus in our learning library, providing organizations with the tools and knowledge to create welcoming and inclusive environments for all employees.
Lastly, we’re always striving to future-proof our customers for the opportunities and challenges of tomorrow. We’ve recently introduced training for every employee on how to leverage generative AI to be work-smart no matter what their role, whilst being conscious of AI’s potential for bias, hallucinations, and an increased risk of data privacy breaches.
So whatever the need - hiring and retaining talent, building inclusive workplaces, or leading hybrid teams - our learning content can help you solve it.
We believe that learning should be accessible to every employee, regardless of their career level, learning style, or workplace. Our inclusive platform is designed to make learning engaging and user-friendly, with bite-sized content inspired by streaming platforms. It's easy to purchase and roll out, supporting teams of any size. With our mobile app, LMS integrations, and support for multiple learning styles, we ensure that all employees can access the same high-quality training.
So that’s us. A market-leading learning platform. Solving big talent challenges, for some of the world’s biggest brands."

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
