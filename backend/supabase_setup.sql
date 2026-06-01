-- Supabase setup: creates projects, skills, experience, contacts tables
-- Paste this whole file into Supabase -> SQL Editor -> New Query and click RUN

-- Enable UUID helper (required once per DB)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Table: projects
CREATE TABLE IF NOT EXISTS projects (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  number text,
  title text NOT NULL,
  description text,
  tags text,
  features text,
  color_class text DEFAULT 'p1',
  link text,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Table: skills
CREATE TABLE IF NOT EXISTS skills (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  category text,
  name text NOT NULL,
  pill_class text DEFAULT 'fe',
  created_at timestamptz DEFAULT now()
);

-- Table: experience
CREATE TABLE IF NOT EXISTS experience (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  position text NOT NULL,
  company text NOT NULL,
  period text,
  description text,
  details text,
  created_at timestamptz DEFAULT now()
);

-- Table: contacts
CREATE TABLE IF NOT EXISTS contacts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  email text NOT NULL,
  subject text,
  message text,
  handled boolean DEFAULT false,
  created_at timestamptz DEFAULT now()
);

-- Optional indexes for common queries
CREATE INDEX IF NOT EXISTS idx_projects_created_at ON projects (created_at DESC);
-- (no extra indexes needed for these simple tables)

-- ===== Sample seed data (dummy) =====
INSERT INTO projects (number, title, description, tags, features, color_class, link)
VALUES
('001', 'Personal Portfolio', 'A modern portfolio site built with React and Tailwind.', 'react,tailwind,vite', 'Landing,Projects,Contact', 'p1', 'https://yourdomain.com'),
('002', 'Blog Platform', 'Simple blog with markdown support.', 'node,express,postgres', 'Markdown posts,Tags', 'p2', 'https://blog.yourdomain.com');

INSERT INTO skills (category, name, pill_class)
VALUES
('Frontend','JavaScript','fe'),
('Frontend','React','fe'),
('Backend','Python','be'),
('Database','SQL','db');

INSERT INTO experience (position, company, period, description, details)
VALUES
('Frontend Developer','Acme Co','Jun 2021 – Oct 2023','Built user interfaces and components.','React, Tailwind, Team collaboration'),
('Fullstack Engineer','Startup X','Nov 2023 – Present','Working on product features and infra.','Node, Postgres, Deployment');

INSERT INTO contacts (name, email, subject, message)
VALUES
('Ali Khan', 'ali@example.com', 'Hello', 'I love your portfolio! Can we collaborate?'),
('Sara Ahmed', 'sara@example.com', 'Hiring', 'We have an opportunity you might like.');

-- Update triggers for updated_at (optional)
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ language 'plpgsql';

DROP TRIGGER IF EXISTS trg_projects_updated_at ON projects;
CREATE TRIGGER trg_projects_updated_at
BEFORE UPDATE ON projects
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
