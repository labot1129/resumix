SYSTEM_PROMPT = "You are a smart assistant to career advisors at the Harvard Extension School. You will reply with JSON only."

TAILORING_PROMPT = """
Consider the following CV:
<CV_TEXT>

Your task is to rewrite the given CV. Follow these guidelines:
- Be truthful and objective to the experience listed in the CV
- Be specific rather than general
- Rewrite job highlight items using STAR methodology (but do not mention STAR explicitly)
- Fix spelling and grammar errors
- Write to express not impress
- Articulate and don't be flowery
- Prefer active voice over passive voice
- Do not include a summary about the candidate

Improved CV:
"""

BASICS_PROMPT = """
You are going to write a JSON resume section for an applicant applying for job posts.

Consider the following CV:
<CV_TEXT>

Now consider the following TypeScript Interface for the JSON schema:

interface Basics {
    name: string;
    email: string;
    phone: string;
    website: string;
    address: string;
}

Write the basics section according to the Basic schema. On the response, include only the JSON.
"""

EDUCATION_PROMPT = """
You are going to write a JSON resume section for an applicant applying for job posts.

Consider the following CV:
<CV_TEXT>

Now consider the following TypeScript Interface for the JSON schema:

interface EducationItem {
    institution: string;
    area: string;
    additionalAreas: string[];
    studyType: string;
    startDate: string;
    endDate: string;
    score: string;
    location: string;
}

interface Education {
    education: EducationItem[];
}

Write the education section according to the Education schema. On the response, include only the JSON.
"""

WORK_PROMPT = """
You are going to write a JSON resume section for an applicant applying for job posts.

Consider the following CV:
<CV_TEXT>

Now consider the following TypeScript Interface for the JSON schema:

interface WorkItem {
    company: string;
    position: string;
    startDate: string;
    endDate: string;
    location: string;
    highlights: string[];
}

interface Work {
    work: WorkItem[];
}

Write a work section for the candidate according to the Work schema. Include only the work experience and not the project experience. For each work experience, provide  a company name, position name, start and end date, and bullet point for the highlights. Follow the Harvard Extension School Resume guidelines and phrase the highlights with the STAR methodology
"""

PROJECTS_PROMPT = """
You are going to write a JSON resume section for an applicant applying for job posts.

Consider the following CV:
<CV_TEXT>

Now consider the following TypeScript Interface for the JSON schema:

interface ProjectItem {
    name: string;
    description: string;
    keywords: string[];
    url: string;
}

interface Projects {
    projects: ProjectItem[];
}

Write the projects section according to the Projects schema. Include all projects, but only the ones present in the CV. On the response, include only the JSON.
"""

SKILLS_PROMPT = """
You are going to write a JSON resume section for an applicant applying for job posts.

Consider the following CV:
<CV_TEXT>

type HardSkills = "Programming Languages" | "Tools" | "Frameworks" | "Computer Proficiency";
type SoftSkills = "Team Work" | "Communication" | "Leadership" | "Problem Solving" | "Creativity";
type OtherSkills = string;

Now consider the following TypeScript Interface for the JSON schema:

interface SkillItem {
    name: HardSkills | SoftSkills | OtherSkills;
    keywords: string[];
}

interface Skills {
    skills: SkillItem[];
}

Write the skills section according to the Skills schema. Include only up to the top 4 skill names that are present in the CV and related with the education and work experience. On the response, include only the JSON.
"""

PROMPT_MAP = {
    "personal_info": BASICS_PROMPT,
    "education": EDUCATION_PROMPT,
    "experience": WORK_PROMPT,
    "projects": PROJECTS_PROMPT,
    "skills": SKILLS_PROMPT,
    "tailor": TAILORING_PROMPT,
}

PROJECTS_SCORE_PROMPT = """
You are a professional HR analyst.
Please evaluate the following **resume section** based on the provided **job description** and rate it from 0 to 10 across six key criteria.

## Job Description

**Basic Requirements**:
<JD_BASIC_TEXT>

**Preferred Requirements**:
<JD_PREFERRED_TEXT>

## Resume Section:
<CV_TEXT>

## Evaluation Instructions:

Score the section on a scale from 0 to 10 for each dimension below.
Give an integer score and concise explanation.
If a dimension is not applicable, assign 0 and explain why.

### Evaluation Dimensions:
- **Completeness**: Does the section provide complete and sufficient information?
- **Clarity**: Is the writing clear, organized, and easy to follow?
- **Relevance**: Does the content align with the basic and preferred requirements?
- **Professional Language**: Does the candidate use appropriate technical and formal language?
- **Achievement-Oriented**: Are accomplishments and results emphasized?
- **Quantitative Support**: Are there any numbers, data, or measurable indicators?

At the end, give a concise **comment** summarizing strengths and improvement suggestions.

## Output JSON Format

You must return **only** valid JSON in the following format:

interface ScoreResult {
  "Completeness": int;
  "Clarity": int;
  "Relevance": int;
  "ProfessionalLanguage": int;
  "AchievementOriented": int;
  "QuantitativeSupport": int;
  "Comment": str;
}
"""

SCORE_PROMPT_MAP = {
    "personal_info": PROJECTS_SCORE_PROMPT,
    "education": PROJECTS_SCORE_PROMPT,
    "experience": PROJECTS_SCORE_PROMPT,
    "projects": PROJECTS_SCORE_PROMPT,
    "skills": PROJECTS_SCORE_PROMPT,
}
