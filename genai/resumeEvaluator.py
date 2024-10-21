import json
from openai import OpenAI
import os
import docx

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ResumeEvaluator:
    def __init__(self, job_description_path, resume_path, company_name):
        self.job_description = self._load_word_document(job_description_path)
        self.candidate_resume = self._load_word_document(resume_path)
        self.company_name = company_name
        self.company_profile = ""
        self.agents = []
        
        self._initialize_agents()
        self._fetch_company_info()

    def _initialize_agents(self):
        self.agents.append({'name': 'CompanyFitAgent', 'role': 'Research'})
        self.agents.append({'name': 'ResumeEvaluationAgent', 'role': 'Evaluator'})
        self.agents.append({'name': 'SkillGapAnalysisAgent', 'role': 'Analysis'})
        self.agents.append({'name': 'CulturalFitAnalysisAgent', 'role': 'Analysis'})
        self.agents.append({'name': 'IndustryTrendAgent', 'role': 'Research'})
        self.agents.append({'name': 'KeywordOptimizationAgent', 'role': 'Optimization'})
        self.agents.append({'name': 'CandidatePositioningAgent', 'role': 'Strategy'})

    def _fetch_company_info(self):
        prompt = f"Research the company {self.company_name} and provide relevant information on its values, mission, work culture, and industry position."
        self.company_profile = self._call_openai_api(prompt)
        print(f"Company profile obtained: {self.company_profile.content}\n")

    def _load_word_document(self, file_path):
        doc = docx.Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])


    def _call_openai_api(self, prompt):
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                 {"role": "system", "content": "You are a helpful assistant."},
                 {"role": "user", "content": prompt}
                ]
            )

        return completion.choices[0].message

    def evaluate_resume(self):
        evaluation_prompt = (
            f"Evaluate the given resume against the job description and fit for the company.\n\n"
            f"Job Description: {self.job_description}\n\n"
            f"Company Profile: {self.company_profile}\n\n"
            f"Candidate Resume: {self.candidate_resume}"
        )
        evaluation_result = self._call_openai_api(evaluation_prompt)
        
        skill_gap_prompt = (
            f"Identify any skill gaps between the job description and the candidate's resume.\n\n"
            f"Job Description: {self.job_description}\n\n"
            f"Candidate Resume: {self.candidate_resume}"
        )
        skill_gap_result = self._call_openai_api(skill_gap_prompt)
        
        cultural_fit_prompt = (
            f"Analyze the candidate's experience and interests to determine alignment with the company's work culture and values.\n\n"
            f"Company Profile: {self.company_profile}\n\n"
            f"Candidate Resume: {self.candidate_resume}"
        )
        cultural_fit_result = self._call_openai_api(cultural_fit_prompt)
        
        industry_trend_prompt = (
            f"Analyze current industry trends and evaluate how well the candidate's experience aligns with these trends.\n\n"
            f"Job Description: {self.job_description}\n\n"
            f"Candidate Resume: {self.candidate_resume}"
        )
        industry_trend_result = self._call_openai_api(industry_trend_prompt)
        
        keyword_optimization_prompt = (
            f"Evaluate the candidate's resume for keyword optimization for the given job description, ensuring it is optimized for ATS (Applicant Tracking Systems).\n\n"
            f"Job Description: {self.job_description}\n\n"
            f"Candidate Resume: {self.candidate_resume}"
        )
        keyword_optimization_result = self._call_openai_api(keyword_optimization_prompt)
        
        positioning_prompt = (
            f"Provide suggestions on how the candidate can position themselves for future roles at the company, beyond the current job description. Highlight achievements that align with the company's long-term goals.\n\n"
            f"Company Profile: {self.company_profile}\n\n"
            f"Candidate Resume: {self.candidate_resume}"
        )
        positioning_result = self._call_openai_api(positioning_prompt)
        
        suggestions_prompt = (
            f"Provide suggestions for the candidate to be more qualified for the position and how to reframe their resume based on the needs of the position and the culture of the company.\n\n"
            f"Job Description: {self.job_description}\n\n"
            f"Company Profile: {self.company_profile}\n\n"
            f"Candidate Resume: {self.candidate_resume}"
        )
        suggestions_result = self._call_openai_api(suggestions_prompt)
        
        return {
            "Evaluation Result": evaluation_result.content,
            "Skill Gap Analysis": skill_gap_result.content,
            "Cultural Fit Analysis": cultural_fit_result.content,
            "Industry Trend Analysis": industry_trend_result.content,
            "Keyword Optimization Analysis": keyword_optimization_result.content,
            "Candidate Positioning Suggestions": positioning_result.content,
            "Suggestions for Improvement": suggestions_result.content
        }

if __name__ == "__main__":
    
    job_description_path = "job_description.docx"
    resume_path = "candidate_resume.docx"
    
    company_name = "FedEx Corporation"

    evaluator = ResumeEvaluator(job_description_path, resume_path, company_name)
    evaluation_results = evaluator.evaluate_resume()

    print("\nFinal Evaluation Result:\n")
    for key, result in evaluation_results.items():
        print(f"{key}: {result}\n")
