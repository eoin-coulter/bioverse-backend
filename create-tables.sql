-- Create questionnaires table
CREATE TABLE IF NOT EXISTS questionnaire_questionnaires (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    pword TEXT NOT NULL,
    is_admin BOOLEAN
);
-- Create questions table
CREATE TABLE IF NOT EXISTS questionnaire_questions (
    id INTEGER PRIMARY KEY,
    question JSONB NOT NULL  
);

-- Create junction table for questionnaire and question
CREATE TABLE IF NOT EXISTS questionnaire_junction (
    id INTEGER PRIMARY KEY,
    questionnaire_id INTEGER REFERENCES questionnaire_questionnaires(id) ON DELETE CASCADE,
    question_id INTEGER REFERENCES questionnaire_questions(id) ON DELETE CASCADE,
    priority INTEGER NOT NULL
);

-- Create answers table
CREATE TABLE IF NOT EXISTS answer (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),  
    question_id INT REFERENCES questionnaire_questions(id) ON DELETE CASCADE,  
    answer TEXT NOT NULL
);


