import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import {
  Home as HomeIcon, User, Code, Briefcase, Cpu, Mail, Send,
  ExternalLink, Download, MessageSquare, Plus, Globe, MapPin,
  Shield, Book, Monitor, Terminal, Database, Settings,
  Sun, Moon
} from 'lucide-react'
import { fetchProjects, fetchSkills, fetchExperience, sendContact } from './api'
import Admin from './Admin'
import emailjs from '@emailjs/browser'

function Home() {
  const [theme, setTheme] = useState('dark')
  const [projects, setProjects] = useState([])
  const [skills, setSkills] = useState([])
  const [experience, setExperience] = useState([])
  const [formData, setFormData] = useState({ name: '', email: '', message: '' })
  const [status, setStatus] = useState('')

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'dark'
    setTheme(savedTheme)
    document.documentElement.setAttribute('data-theme', savedTheme)

    const loadData = async () => {
      try {
        const [p, s, e] = await Promise.all([fetchProjects(), fetchSkills(), fetchExperience()])
        setProjects(p)
        setSkills(s)
        setExperience(e)
      } catch (err) {
        console.error("Error loading portfolio data:", err)
      }
    }
    loadData()
  }, [])

  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark'
    setTheme(newTheme)
    localStorage.setItem('theme', newTheme)
    document.documentElement.setAttribute('data-theme', newTheme)
  }

  const handleContactSubmit = async (e) => {
    e.preventDefault()
    setStatus('Sending...')

    // 1. Send to Backend Database
    try {
      await sendContact(formData)
    } catch (err) {
      console.error("DB Save failed:", err)
    }

    // 2. Send Direct Email via EmailJS
    // Replace placeholders with your own keys from EmailJS
    const serviceId = 'service_xxxxxx' // Aapka Service ID
    const templateId = 'template_xxxxxxx' // Aapka Template ID
    const publicKey = 'your_public_key'  // Aapka Public Key

    emailjs.send(serviceId, templateId, {
      from_name: formData.name,
      from_email: formData.email,
      message: formData.message,
      to_email: 'saba@email.com', // Aapka email
    }, publicKey)
      .then(() => {
        setStatus('Success! Email sent and saved.')
        setFormData({ name: '', email: '', message: '' })
      }, (error) => {
        console.error("EmailJS Error:", error)
        setStatus('Saved to database, but email failed. Check your EmailJS keys.')
      })
  }

  const groupedSkills = skills.reduce((acc, skill) => {
    if (!acc[skill.category]) acc[skill.category] = []
    acc[skill.category].push(skill)
    return acc
  }, {})

  return (
    <div className="portfolio-wrapper">
      {/* Background Element */}
      <div className="hero-orb"></div>

      <nav className="navbar fade-in">
        <div className="nav-container">
          <div className="nav-brand-boxed">
            <div className="brand-logo-box">
              <Code size={24} strokeWidth={3} />
            </div>
            <div className="brand-text-wrap">
              <div className="brand-name-main">Saba</div>
              <div className="brand-subtitle">FULL STACK DEVELOPER</div>
            </div>
          </div>

          <div className="nav-links-centered">
            <a href="#about" className="nav-link">About</a>
            <a href="#experience" className="nav-link">Experience</a>
            <a href="#projects" className="nav-link">Projects</a>
            <a href="#skills" className="nav-link">Skills</a>
            <a href="#contact" className="nav-link">Contact</a>
          </div>

          <div className="nav-actions">
            <button className="theme-toggle" onClick={toggleTheme}>
              {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
            </button>
            <a href="#contact" className="btn-primary hire-me-btn" style={{ padding: '0.6rem 1.2rem', fontSize: '0.85rem' }}>
              Hire Me
            </a>
          </div>
        </div>
      </nav>

      <main className="container">
        {/* HERO SECTION */}
        <section className="hero" id="home">
          <div className="hero-tag fade-up d1">
            <span className="hero-dot"></span> Available for opportunities
          </div>
          <h1 className="fade-up d2">
            Hi, I'm <span className="name">Saba</span>
            <span className="role">Full Stack Developer</span>
          </h1>
          <p className="hero-sub fade-up d3">
            I'm a passionate Full Stack Developer with expertise in building modern web applications.
            I love crafting clean, user-friendly frontends using React and Tailwind CSS, and building
            powerful, scalable backends with Python and FastAPI.
          </p>
          <div className="cta-row fade-up d4">
            <a href="#projects" className="btn-primary">View My Work</a>
            <a href="/resume.pdf" className="btn-outline" download>
              <Download size={18} style={{ marginRight: '8px' }} /> Resume
            </a>
            <a href="#contact" className="btn-outline">Get in Touch</a>
          </div>
          <div className="stats-row fade-up d5">
            <div className="stat-item">
              <div className="stat-num">1+</div>
              <div className="stat-label">Years Experience</div>
            </div>
            <div className="stat-item">
              <div className="stat-num">3+</div>
              <div className="stat-label">Projects Built</div>
            </div>
            <div className="stat-item">
              <div className="stat-num">10+</div>
              <div className="stat-label">Technologies</div>
            </div>
          </div>
        </section>

        <div className="divider"></div>

        {/* ABOUT SECTION */}
        <section className="section" id="about">
          <div className="section-header fade-up">
            <div className="section-label">Who I Am</div>
            <div className="section-title">About Me</div>
          </div>
          <div className="about-card fade-up d2">
            <div className="avatar-wrap">
              <div className="avatar">S</div>
              <div className="status-badge">
                <span className="status-dot"></span> Open to work
              </div>
            </div>
            <div className="about-content">
              <div className="about-name">Saba</div>
              <div className="about-role">Full Stack Developer</div>
              <p>
                I'm a passionate Full Stack Developer with expertise in building modern web applications.
                I love crafting clean, user-friendly frontends using React and Tailwind CSS, and building
                powerful, scalable backends with Python and FastAPI. My experience spans databases like
                PostgreSQL and SQL Server, allowing me to deliver complete end-to-end solutions.
                I believe great software is a blend of clean code, thoughtful design, and real-world impact.
              </p>
            </div>
          </div>

          {/* Academic Record Subsection */}
          <div className="academic-record fade-up d3" style={{ marginTop: '4rem' }}>
            <h3 style={{ fontFamily: "'Playfair Display', serif", fontSize: '2rem', marginBottom: '2rem' }}>Academic Record</h3>
            <div className="edu-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
              <div className="edu-item" style={{ background: 'var(--surface-secondary)', padding: '2rem', borderRadius: 'var(--radius)', border: '1px solid var(--border)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
                  <div style={{ width: '40px', height: '40px', background: 'rgba(167, 139, 250, 0.1)', color: 'var(--accent)', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}><Book size={20} /></div>
                  <h4 style={{ fontSize: '1.2rem' }}>BS Information Technology</h4>
                </div>
                <p style={{ color: 'var(--accent)', fontWeight: 600, marginBottom: '0.5rem' }}>Rawalpindi Women Univeristy</p>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>2021 — 2025</p>
              </div>
              <div className="edu-item" style={{ background: 'var(--surface-secondary)', padding: '2rem', borderRadius: 'var(--radius)', border: '1px solid var(--border)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
                  <div style={{ width: '40px', height: '40px', background: 'rgba(167, 139, 250, 0.1)', color: 'var(--accent)', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}><Book size={20} /></div>
                  <h4 style={{ fontSize: '1.2rem' }}>HSSC (Intermediate in Computer Science)</h4>
                </div>
                <p style={{ color: 'var(--accent)', fontWeight: 600, marginBottom: '0.5rem' }}>Islambad Mo College For Girls</p>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>2019 — 2021</p>
              </div>
            </div>
          </div>
        </section>

        <div className="divider"></div>

        {/* SKILLS SECTION */}
        <section className="section" id="skills">
          <div className="section-header fade-up">
            <h2 className="toolkit-title">My <span className="highlight">toolkit.</span></h2>
          </div>

          <div className="toolkit-grid fade-up d2">
            {Object.entries(groupedSkills).map(([category, items], idx) => (
              <div key={category} className={`toolkit-card d${(idx % 5) + 1}`}>
                <div className="toolkit-card-header">
                  {category.toLowerCase().includes('frontend') && <Monitor size={20} className="toolkit-icon" />}
                  {category.toLowerCase().includes('backend') && <Terminal size={20} className="toolkit-icon" />}
                  {category.toLowerCase().includes('database') && <Database size={20} className="toolkit-icon" />}
                  {category.toLowerCase().includes('tool') && <Settings size={20} className="toolkit-icon" />}
                  {(!category.toLowerCase().includes('frontend') &&
                    !category.toLowerCase().includes('backend') &&
                    !category.toLowerCase().includes('database') &&
                    !category.toLowerCase().includes('tool')) && <Cpu size={20} className="toolkit-icon" />}
                  <h3>{category}</h3>
                </div>
                <div className="toolkit-pills">
                  {items.map(skill => (
                    <span key={skill.id} className="toolkit-pill">
                      {skill.name}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </section>

        <div className="divider"></div>

        {/* EXPERIENCE SECTION */}
        <section className="section" id="experience">
          <div className="section-header fade-up">
            <div className="section-label">Career</div>
            <div className="section-title">Work Experience</div>
          </div>
          <div className="experience-list">
            {experience.map((exp, idx) => (
              <div key={exp.id} className="experience-item fade-up">
                <div className="experience-content">
                  <div className="experience-header-row">
                    <div>
                      <h3 className="position-title">{exp.position}</h3>
                      <p className="company-name">{exp.company}</p>
                    </div>
                    <span className="exp-period">{exp.period}</span>
                  </div>
                  <p className="exp-desc">{exp.description}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        <div className="divider"></div>

        {/* PROJECTS SECTION */}
        <section className="section" id="projects">
          <div className="section-header fade-up">
            <h2 className="toolkit-title">Featured <span className="highlight">projects.</span></h2>
          </div>

          <div className="projects-grid-3 fade-up d2">
            {projects.map((p, idx) => (
              <div key={p.id} className="project-feature-card">
                <div className="project-feature-header">
                  <span className="status-badge-live">Live</span>
                  <a href={p.link || "#"} className="project-link-icon">
                    <ExternalLink size={18} />
                  </a>
                </div>

                <div className="project-feature-content">
                  <h3 className="project-feature-title">{p.title}</h3>
                  <p className="project-feature-desc">{p.description}</p>
                </div>

                <div className="project-feature-footer">
                  <div className="project-feature-tags">
                    {p.tags?.split(',').map(tag => (
                      <span key={tag} className="tech-tag-pill">{tag.trim()}</span>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        <div className="divider"></div>

        {/* CONTACT SECTION */}
        <section className="section" id="contact" style={{ textAlign: 'center' }}>
          <div className="contact-premium-header fade-up">
            <h2 className="toolkit-title" style={{ fontSize: '4rem', margin: '0 auto 1.5rem', maxWidth: '800px' }}>
              Let's build something <span className="highlight">great together.</span>
            </h2>
            <p className="contact-subtitle-premium">
              Open to full-time onsite work, freelance projects, and interesting collaborations. Drop me a message.
            </p>

            <a href="mailto:saba@email.com" className="btn-primary" style={{ margin: '3rem auto', display: 'flex', width: 'fit-content', gap: '0.8rem', padding: '1.2rem 2.5rem' }}>
              <Mail size={18} /> Send me an email <Send size={18} />
            </a>
          </div>

          <div className="contact-grid-premium fade-up d2">
            <div className="contact-info-card-premium">
              <div className="contact-info-icon-wrap"><Mail size={20} /></div>
              <div className="contact-info-text">
                <div className="info-label">EMAIL</div>
                <div className="info-val">saba@email.com</div>
                <div className="info-sub">Best way to reach me</div>
              </div>
            </div>
            <div className="contact-info-card-premium">
              <div className="contact-info-icon-wrap"><Globe size={20} /></div>
              <div className="contact-info-text">
                <div className="info-label">WHATSAPP</div>
                <div className="info-val">+92 3230513988</div>
                <div className="info-sub">Quick response</div>
              </div>
            </div>
            <div className="contact-info-card-premium">
              <div className="contact-info-icon-wrap"><User size={20} /></div>
              <div className="contact-info-text">
                <div className="info-label">LINKEDIN</div>
                <a href="https://www.linkedin.com/in/saba-khalid-6ba1793b3/" target="_blank" rel="noopener noreferrer" className="info-val">
                  View Profile
                </a>
                <div className="info-sub">Professional network</div>
              </div>
            </div>
            <div className="contact-info-card-premium">
              <div className="contact-info-icon-wrap"><Code size={20} /></div>
              <div className="contact-info-text">
                <div className="info-label">GITHUB</div>
                <a href="https://github.com/sabakhalidpk091-eng" target="_blank" rel="noopener noreferrer" className="info-val">
                  Check Repos
                </a>
                <div className="info-sub">Code & Repos</div>
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer className="main-footer fade-up">
        <div className="container">
          <div className="footer-top">
            <div className="footer-brand-col">
              <div className="footer-logo">SABA.</div>
              <p className="footer-bio">Full-Stack Developer building fast, scalable, and polished web applications.</p>
              <div className="footer-socials">
                <a href="https://github.com/sabakhalidpk091-eng" target="_blank" rel="noopener noreferrer" className="social-icon-btn"><Code size={18} /></a>
                <a href="https://www.linkedin.com/in/saba-khalid-6ba1793b3/" target="_blank" rel="noopener noreferrer" className="social-icon-btn"><User size={18} /></a>
                <a href="https://wa.me/923230513988" target="_blank" rel="noopener noreferrer" className="social-icon-btn"><MessageSquare size={18} /></a>
              </div>
            </div>

            <div className="footer-links-col">
              <h4>SECTIONS</h4>
              <a href="#about">About</a>
              <a href="#experience">Experience</a>
              <a href="#projects">Projects</a>
              <a href="#skills">Skills</a>
              <a href="#contact">Contact</a>
            </div>

            <div className="footer-links-col">
              <h4>CONTACT</h4>
              <a href="mailto:saba@email.com">Email</a>
              <a href="https://wa.me/923230513988" target="_blank" rel="noopener noreferrer">WhatsApp</a>
              <a href="https://www.linkedin.com/in/saba-khalid-6ba1793b3/" target="_blank" rel="noopener noreferrer">LinkedIn</a>
            </div>

            <div className="footer-status-col">
              <div className="open-to-work-card">
                <h3>Open to work</h3>
                <p>Onsite Full-time · Contract</p>
                <a href="#contact" className="btn-primary">
                  Get in touch <Send size={16} />
                </a>
              </div>
            </div>
          </div>

          <div className="footer-bottom">
            <div className="copyright">© 2026 Saba. All rights reserved.</div>
            <div className="built-with">Built with React · Tailwind CSS · FastAPI</div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/admin" element={<Admin />} />
      </Routes>
    </Router>
  )

}
