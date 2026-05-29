import { useState, useEffect } from 'react'
import {
    fetchProjects, fetchExperience, fetchSkills,
    createProject, createExperience, createSkill,
    updateProject, updateExperience, updateSkill,
    deleteProject, deleteExperience, deleteSkill
} from './api'

function Admin() {
    const [activeTab, setActiveTab] = useState('projects')
    const [projects, setProjects] = useState([])
    const [experience, setExperience] = useState([])
    const [skills, setSkills] = useState([])
    const [messages, setMessages] = useState([])

    // Editing State
    const [editingId, setEditingId] = useState(null)

    // Forms
    const [projForm, setProjForm] = useState({ number: '', title: '', description: '', tags: '', features: '', color_class: 'p1' })
    const [expForm, setExpForm] = useState({ position: '', company: '', period: '', description: '', details: '' })
    const [skillForm, setSkillForm] = useState({ category: 'Frontend', name: '', pill_class: 'fe' })

    useEffect(() => {
        load()
    }, [])

    const load = async () => {
        const [p, e, s] = await Promise.all([fetchProjects(), fetchExperience(), fetchSkills()])
        setProjects(p)
        setExperience(e)
        setSkills(s)

        // Fetch messages
        try {
            const res = await fetch("http://localhost:8000/api/contact")
            if (res.ok) setMessages(await res.json())
        } catch (err) { console.error(err) }
    }

    const resetForms = () => {
        setEditingId(null)
        setProjForm({ number: '', title: '', description: '', tags: '', features: '', color_class: 'p1' })
        setExpForm({ position: '', company: '', period: '', description: '', details: '' })
        setSkillForm({ category: 'Frontend', name: '', pill_class: 'fe' })
    }

    const handleProjSubmit = async (e) => {
        e.preventDefault()
        if (editingId) {
            await updateProject(editingId, projForm)
        } else {
            await createProject(projForm)
        }
        resetForms()
        load()
    }

    const handleExpSubmit = async (e) => {
        e.preventDefault()
        if (editingId) {
            await updateExperience(editingId, expForm)
        } else {
            await createExperience(expForm)
        }
        resetForms()
        load()
    }

    const handleSkillSubmit = async (e) => {
        e.preventDefault()
        if (editingId) {
            await updateSkill(editingId, skillForm)
        } else {
            await createSkill(skillForm)
        }
        resetForms()
        load()
    }

    const startEditProj = (p) => {
        setEditingId(p.id)
        setProjForm({ ...p })
        window.scrollTo({ top: 0, behavior: 'smooth' })
    }

    const startEditExp = (e) => {
        setEditingId(e.id)
        setExpForm({ ...e })
        window.scrollTo({ top: 0, behavior: 'smooth' })
    }

    const startEditSkill = (s) => {
        setEditingId(s.id)
        setSkillForm({ ...s })
        window.scrollTo({ top: 0, behavior: 'smooth' })
    }

    const handleDeleteProj = async (id) => {
        if (confirm('Delete this project?')) {
            await deleteProject(id)
            load()
        }
    }

    const handleDeleteExp = async (id) => {
        if (confirm('Delete this experience?')) {
            await deleteExperience(id)
            load()
        }
    }

    const handleDeleteSkill = async (id) => {
        if (confirm('Delete this skill?')) {
            await deleteSkill(id)
            load()
        }
    }

    return (
        <div className="admin-container" style={{ padding: '6rem 2rem', maxWidth: '1200px', margin: '0 auto', background: '#000', minHeight: '100vh', color: '#fff' }}>
            <div className="section-header" style={{ marginBottom: '4rem' }}>
                <h2 className="toolkit-title" style={{ fontSize: '3rem' }}>Admin <span className="highlight">Dashboard</span></h2>
                <p style={{ color: 'var(--text-secondary)' }}>Centralized control for your portfolio and messages.</p>
            </div>

            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1.2rem', marginBottom: '3rem' }}>
                <button onClick={() => { setActiveTab('projects'); resetForms(); }} className={activeTab === 'projects' ? 'btn-primary' : 'btn-outline'}>Projects</button>
                <button onClick={() => { setActiveTab('experience'); resetForms(); }} className={activeTab === 'experience' ? 'btn-primary' : 'btn-outline'}>Experience</button>
                <button onClick={() => { setActiveTab('skills'); resetForms(); }} className={activeTab === 'skills' ? 'btn-primary' : 'btn-outline'}>Skills (Toolkit)</button>
                <button onClick={() => { setActiveTab('messages'); resetForms(); }} className={activeTab === 'messages' ? 'btn-primary' : 'btn-outline'}>Messages</button>
                <a href="/" className="btn-outline">View Site</a>
            </div>

            {activeTab === 'projects' && (
                <div className="fade-up">
                    <form className="contact-form" style={{ marginBottom: '3rem', background: '#080808' }} onSubmit={handleProjSubmit}>
                        <h4 style={{ marginBottom: '1.5rem' }}>{editingId ? 'Edit Project' : 'Add New Project'}</h4>
                        <input type="text" placeholder="Project Number (e.g. 01)" className="form-input" style={{ marginBottom: '1rem' }} value={projForm.number} onChange={e => setProjForm({ ...projForm, number: e.target.value })} required />
                        <input type="text" placeholder="Title" className="form-input" style={{ marginBottom: '1rem' }} value={projForm.title} onChange={e => setProjForm({ ...projForm, title: e.target.value })} required />
                        <textarea placeholder="Description" className="form-input" style={{ marginBottom: '1rem', height: '100px' }} value={projForm.description} onChange={e => setProjForm({ ...projForm, description: e.target.value })} required />
                        <input type="text" placeholder="Tags (React, FastAPI...)" className="form-input" style={{ marginBottom: '1.5rem' }} value={projForm.tags} onChange={e => setProjForm({ ...projForm, tags: e.target.value })} />
                        <div style={{ display: 'flex', gap: '1rem' }}>
                            <button type="submit" className="btn-primary">{editingId ? 'Update Project' : 'Add Project'}</button>
                            {editingId && <button type="button" className="btn-outline" onClick={resetForms}>Cancel</button>}
                        </div>
                    </form>

                    <h3>Catalog</h3>
                    <div className="admin-list" style={{ marginTop: '1.5rem' }}>
                        {projects.map(p => (
                            <div key={p.id} className="contact-info-card-premium" style={{ marginBottom: '1rem', justifyContent: 'space-between' }}>
                                <div>
                                    <div className="info-val">{p.title}</div>
                                    <div className="info-sub">{p.number} — {p.tags}</div>
                                </div>
                                <div style={{ display: 'flex', gap: '0.8rem' }}>
                                    <button onClick={() => startEditProj(p)} className="btn-outline" style={{ color: 'var(--accent)', borderColor: 'var(--accent)' }}>Edit</button>
                                    <button onClick={() => handleDeleteProj(p.id)} className="btn-outline" style={{ color: '#ef4444', borderColor: '#ef4444' }}>Delete</button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {activeTab === 'skills' && (
                <div className="fade-up">
                    <form className="contact-form" style={{ marginBottom: '3rem', background: '#080808' }} onSubmit={handleSkillSubmit}>
                        <h4 style={{ marginBottom: '1.5rem' }}>{editingId ? 'Edit Skill' : 'Add New Skill'}</h4>
                        <select className="form-input" style={{ marginBottom: '1rem' }} value={skillForm.category} onChange={e => setSkillForm({ ...skillForm, category: e.target.value })}>
                            <option>Frontend</option>
                            <option>Backend</option>
                            <option>Databases</option>
                            <option>State & Data</option>
                            <option>Styling</option>
                            <option>Tools & DevOps</option>
                        </select>
                        <input type="text" placeholder="Skill Name (e.g. React)" className="form-input" style={{ marginBottom: '1.5rem' }} value={skillForm.name} onChange={e => setSkillForm({ ...skillForm, name: e.target.value })} required />
                        <div style={{ display: 'flex', gap: '1rem' }}>
                            <button type="submit" className="btn-primary">{editingId ? 'Update Skill' : 'Add Skill'}</button>
                            {editingId && <button type="button" className="btn-outline" onClick={resetForms}>Cancel</button>}
                        </div>
                    </form>

                    <h3>Your Toolkit</h3>
                    <div className="admin-list" style={{ marginTop: '1.5rem' }}>
                        {skills.map(s => (
                            <div key={s.id} className="contact-info-card-premium" style={{ marginBottom: '1rem', justifyContent: 'space-between' }}>
                                <div>
                                    <div className="info-val">{s.name}</div>
                                    <div className="info-sub">{s.category}</div>
                                </div>
                                <div style={{ display: 'flex', gap: '0.8rem' }}>
                                    <button onClick={() => startEditSkill(s)} className="btn-outline" style={{ color: 'var(--accent)', borderColor: 'var(--accent)' }}>Edit</button>
                                    <button onClick={() => handleDeleteSkill(s.id)} className="btn-outline" style={{ color: '#ef4444', borderColor: '#ef4444' }}>Delete</button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {activeTab === 'experience' && (
                <div className="fade-up">
                    <form className="contact-form" style={{ marginBottom: '3rem', background: '#080808' }} onSubmit={handleExpSubmit}>
                        <h4 style={{ marginBottom: '1.5rem' }}>{editingId ? 'Edit Experience' : 'Add New Experience'}</h4>
                        <input type="text" placeholder="Position" className="form-input" style={{ marginBottom: '1rem' }} value={expForm.position} onChange={e => setExpForm({ ...expForm, position: e.target.value })} required />
                        <input type="text" placeholder="Company" className="form-input" style={{ marginBottom: '1rem' }} value={expForm.company} onChange={e => setExpForm({ ...expForm, company: e.target.value })} required />
                        <input type="text" placeholder="Period" className="form-input" style={{ marginBottom: '1rem' }} value={expForm.period} onChange={e => setExpForm({ ...expForm, period: e.target.value })} required />
                        <textarea placeholder="Brief Description" className="form-input" style={{ marginBottom: '1.5rem', height: '100px' }} value={expForm.description} onChange={e => setExpForm({ ...expForm, description: e.target.value })} required />
                        <div style={{ display: 'flex', gap: '1rem' }}>
                            <button type="submit" className="btn-primary">{editingId ? 'Update Experience' : 'Add Experience'}</button>
                            {editingId && <button type="button" className="btn-outline" onClick={resetForms}>Cancel</button>}
                        </div>
                    </form>

                    <h3>Career History</h3>
                    <div className="admin-list" style={{ marginTop: '1.5rem' }}>
                        {experience.map(e => (
                            <div key={e.id} className="contact-info-card-premium" style={{ marginBottom: '1rem', justifyContent: 'space-between' }}>
                                <div>
                                    <div className="info-val">{e.position}</div>
                                    <div className="info-sub">{e.company} — {e.period}</div>
                                </div>
                                <div style={{ display: 'flex', gap: '0.8rem' }}>
                                    <button onClick={() => startEditExp(e)} className="btn-outline" style={{ color: 'var(--accent)', borderColor: 'var(--accent)' }}>Edit</button>
                                    <button onClick={() => handleDeleteExp(e.id)} className="btn-outline" style={{ color: '#ef4444', borderColor: '#ef4444' }}>Delete</button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {activeTab === 'messages' && (
                <div className="fade-up">
                    <h3>Contact Messages</h3>
                    <div className="admin-list" style={{ marginTop: '1.5rem' }}>
                        {messages.length === 0 && <p style={{ color: 'var(--text-secondary)' }}>No messages yet.</p>}
                        {messages.map(m => (
                            <div key={m.id} className="contact-info-card-premium" style={{ marginBottom: '1.5rem', flexDirection: 'column', alignItems: 'flex-start' }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%', marginBottom: '1rem' }}>
                                    <div className="info-val">{m.name}</div>
                                    <div className="info-sub">{new Date(m.created_at).toLocaleDateString()}</div>
                                </div>
                                <div style={{ color: 'var(--accent)', fontSize: '0.8rem', fontWeight: 700, marginBottom: '0.5rem' }}>{m.email}</div>
                                <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', lineHeight: 1.6 }}>{m.message}</p>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    )
}

export default Admin
