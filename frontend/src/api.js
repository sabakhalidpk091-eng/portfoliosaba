const BASE = "https://portfoliosabakhalid.vercel.app";

// GET
export async function fetchProjects() {
    const res = await fetch(`${BASE}/api/projects`);
    if (!res.ok) throw new Error("Failed to fetch projects");
    return res.json();
}

export async function fetchSkills() {
    const res = await fetch(`${BASE}/api/skills`);
    if (!res.ok) throw new Error("Failed to fetch skills");
    return res.json();
}

export async function fetchExperience() {
    const res = await fetch(`${BASE}/api/experience`);
    if (!res.ok) throw new Error("Failed to fetch experience");
    return res.json();
}

export async function fetchMessages() {
    const res = await fetch(`${BASE}/api/contact`);
    if (!res.ok) throw new Error("Failed to fetch messages");
    return res.json();
}

// POST
export async function sendContact(data) {
    const res = await fetch(`${BASE}/api/contact`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Failed to send message");
    return res.json();
}

export async function createProject(data) {
    const res = await fetch(`${BASE}/api/projects`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...data, id: 0 }),
    });
    return res.json();
}

export async function updateProject(id, data) {
    const res = await fetch(`${BASE}/api/projects/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...data, id }),
    });
    return res.json();
}

export async function createExperience(data) {
    const res = await fetch(`${BASE}/api/experience`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...data, id: 0 }),
    });
    return res.json();
}

export async function updateExperience(id, data) {
    const res = await fetch(`${BASE}/api/experience/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...data, id }),
    });
    return res.json();
}

export async function createSkill(data) {
    const res = await fetch(`${BASE}/api/skills`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...data, id: 0 }),
    });
    return res.json();
}

export async function updateSkill(id, data) {
    const res = await fetch(`${BASE}/api/skills/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...data, id }),
    });
    return res.json();
}

// DELETE
export async function deleteProject(id) {
    return fetch(`${BASE}/api/projects/${id}`, { method: "DELETE" });
}

export async function deleteExperience(id) {
    return fetch(`${BASE}/api/experience/${id}`, { method: "DELETE" });
}

export async function deleteSkill(id) {
    return fetch(`${BASE}/api/skills/${id}`, { method: "DELETE" });
}
