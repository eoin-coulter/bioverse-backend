-- Create questionnaires table
CREATE TABLE IF NOT EXISTS questionnaire_questionnaires (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL
);

-- Create questions table
CREATE TABLE IF NOT EXISTS questionnaire_questions (
    id INTEGER PRIMARY KEY,
    data JSONB NOT NULL  
);

-- Create junction table for questionnaire and question
CREATE TABLE IF NOT EXISTS questionnaire_junction (
    id INTEGER PRIMARY KEY,
    questionnaire_id INTEGER REFERENCES questionnaire_questionnaires(id) ON DELETE CASCADE,
    question_id INTEGER REFERENCES questionnaire_question(id) ON DELETE CASCADE,
    priority INTEGER NOT NULL
);

-- Create answers table
CREATE TABLE IF NOT EXISTS answer (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,  
    questionnaire_id INT REFERENCES questionnaire_questionnaires(id) ON DELETE CASCADE,  
    question_id INT REFERENCES questionnaire_question(id) ON DELETE CASCADE,  
    answer_content TEXT NOT NULL
);
