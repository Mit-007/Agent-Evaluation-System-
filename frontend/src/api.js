const BASE_URL = (import.meta.env.VITE_API_BASE_URL || '/api').replace(/\/$/, '');

async function request(path, options = {}) {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.detail || `Request failed (${response.status})`);
  }

  return response.status === 204 ? null : response.json();
}

export const api = {
  projects: () => request('/projects'),

  createProject: (project_name) =>
    request('/projects', {
      method: 'POST',
      body: JSON.stringify({ project_name }),
    }),

  updateProject: (id, project_new_name) =>
    request(`/projects/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ project_new_name }),
    }),

  deleteProject: (id) =>
    request(`/projects/${id}`, {
      method: 'DELETE',
    }),

  agents: (id) => request(`/projects/${id}/agents`),

  createAgent: (id, agent_name) =>
    request(`/projects/${id}/agents`, {
      method: 'POST',
      body: JSON.stringify({ agent_name }),
    }),

  updateAgent: (id, agent_new_name) =>
    request(`/agents/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ agent_new_name }),
    }),

  deleteAgent: (id) =>
    request(`/agents/${id}`, {
      method: 'DELETE',
    }),

  prompts: (id) => request(`/agents/${id}/prompts`),

  createPrompt: (id, prompt) =>
    request(`/agents/${id}/prompts`, {
      method: 'POST',
      body: JSON.stringify({ prompt }),
    }),

  updatePrompt: (id, new_prompt) =>
    request(`/prompts/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ new_prompt }),
    }),

  deletePrompt: (id) =>
    request(`/prompts/${id}`, {
      method: 'DELETE',
    }),

  dimensions: (id) => request(`/projects/${id}/dimensions`),

  setDimensions: (id, dimensions_list) =>
    request(`/projects/${id}/dimensions`, {
      method: 'POST',
      body: JSON.stringify({ dimensions_list }),
    }),

  updateDimension: (id, new_dimension_description) =>
    request(`/dimensions/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ new_dimension_description }),
    }),

  deleteDimension: (id) =>
    request(`/dimensions/${id}`, {
      method: 'DELETE',
    }),

  evaluate: (agent_id, chat) =>
    request('/evaluations/run', {
      method: 'POST',
      body: JSON.stringify({ agent_id, chat }),
    }),

  evaluations: (id) => request(`/agents/${id}/evaluations`),
};
