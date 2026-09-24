import { useEffect, useMemo, useState } from 'react';
import {
  Activity,
  AlertCircle,
  Anvil,
  ArrowUpRight,
  Bot,
  CheckCircle2,
  ChevronDown,
  ClipboardCheck,
  FolderKanban,
  LoaderCircle,
  Menu,
  Pencil,
  Plus,
  Send,
  SlidersHorizontal,
  Sparkles,
  Trash2,
  X,
} from 'lucide-react';
import { api } from './api';

const unpack = (value) => value?.rows || value || [];

const asProject = (row) =>
  Array.isArray(row)
    ? { id: row[0], name: row[1], createdAt: row[2] }
    : { id: row.project_id, name: row.project_name, createdAt: row.created_at };

const asAgent = (row) =>
  Array.isArray(row)
    ? { id: row[0], name: row[1], projectId: row[2] }
    : { id: row.agent_id, name: row.agent_name, projectId: row.project_id };

const asPrompt = (row) =>
  Array.isArray(row)
    ? { id: row[0], agentId: row[1], text: row[2], version: row[3] }
    : { id: row.prompt_id, agentId: row.agent_id, text: row.prompt, version: row.version };

function Empty({ icon: Icon, title, text, action }) {
  return (
    <div className="empty">
      <Icon size={28} />
      <h3>{title}</h3>
      <p>{text}</p>
      {action}
    </div>
  );
}

function Modal({ title, children, close }) {
  return (
    <div className="overlay" role="dialog" aria-modal="true">
      <div className="modal">
        <button className="icon-btn close" onClick={close}>
          <X size={19} />
        </button>
        <h2>{title}</h2>
        {children}
      </div>
    </div>
  );
}

export default function App() {
  const [projects, setProjects] = useState([]);
  const [projectId, setProjectId] = useState(null);
  const [agents, setAgents] = useState([]);
  const [agentId, setAgentId] = useState(null);
  const [prompts, setPrompts] = useState([]);
  const [dimensions, setDimensions] = useState([]);
  const [evaluations, setEvaluations] = useState([]);
  const [evaluationResult, setEvaluationResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [modal, setModal] = useState(null);
  const [menu, setMenu] = useState(false);
  const [page, setPage] = useState('home');

  const project = projects.find((p) => p.id === projectId);
  const agent = agents.find((a) => a.id === agentId);
  const latestPrompt = prompts.slice().sort((a, b) => b.version - a.version)[0];
  const message = useMemo(() => evaluations[0]?.[3] || evaluations[0]?.chat || '', [evaluations]);

  const fetchProjects = async () => {
    setLoading(true);
    try {
      const result = unpack(await api.projects()).map(asProject);
      setProjects(result);
      setProjectId((current) => current || result[0]?.id || null);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchProjectData = async (id) => {
    if (!id) {
      setAgents([]);
      return;
    }
    try {
      const data = await api.agents(id).catch(() => ({ rows: [] }));
      const list = unpack(data).map(asAgent);
      setAgents(list);
      setAgentId((current) => (list.some((a) => a.id === current) ? current : list[0]?.id || null));
      setDimensions(await api.dimensions(id).catch(() => []));
    } catch (e) {
      setError(e.message);
    }
  };

  const fetchAgentData = async (id) => {
    if (!id) {
      setPrompts([]);
      setEvaluations([]);
      setEvaluationResult(null);
      return;
    }
    try {
      setPrompts(unpack(await api.prompts(id).catch(() => ({ rows: [] }))).map(asPrompt));
      const history = unpack(await api.evaluations(id).catch(() => []));
      setEvaluations(history);
      const saved = history[0]?.output_response || history[0]?.[4];
      setEvaluationResult(saved ? (typeof saved === 'string' ? JSON.parse(saved) : saved) : null);
    } catch (e) {
      setError(e.message);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  useEffect(() => {
    fetchProjectData(projectId);
  }, [projectId]);

  useEffect(() => {
    fetchAgentData(agentId);
  }, [agentId]);

  const create = async (type, values) => {
    try {
      if (type === 'project') {
        const item = await api.createProject(values.name);
        await fetchProjects();
        setProjectId(item.project_id);
      }
      if (type === 'agent') {
        await api.createAgent(projectId, values.name);
        await fetchProjectData(projectId);
      }
      if (type === 'prompt') {
        await api.createPrompt(agentId, values.text);
        await fetchAgentData(agentId);
      }
      if (type === 'dimensions') {
        await api.setDimensions(projectId, values);
        await fetchProjectData(projectId);
      }
      setModal(null);
      setNotice(`${type === 'dimensions' ? 'Evaluation criteria' : type} saved successfully.`);
    } catch (e) {
      setError(e.message);
    }
  };

  const run = async (chat) => {
    if (!agentId || !chat.trim()) return;
    setRunning(true);
    setError('');
    try {
      const result = await api.evaluate(agentId, chat);
      setEvaluationResult(result);
      await fetchAgentData(agentId);
      setNotice('Evaluation completed and added to history.');
    } catch (e) {
      setError(e.message);
    } finally {
      setRunning(false);
    }
  };

  if (loading) {
    return (
      <div className="page-loader">
        <LoaderCircle className="spin" />
        <span>Preparing your workspace…</span>
      </div>
    );
  }

  const nav = (target) => {
    setPage(target);
    setMenu(false);
  };

  return (
    <div className="app">
      <aside className={menu ? 'sidebar open' : 'sidebar'}>
        <div className="brand">
          <span className="brand-mark forge-mark">
            <Anvil size={19} />
          </span>
          <span>Eval Forge</span>
          <button className="mobile-close icon-btn" onClick={() => setMenu(false)}>
            <X />
          </button>
        </div>
        <nav>
          <span className="nav-label">WORKSPACE</span>
          <a className={page === 'home' ? 'active' : ''} onClick={() => nav('home')}>
            <Activity size={18} />
            Home
          </a>
          <a className={page === 'projects' ? 'active' : ''} onClick={() => nav('projects')}>
            <FolderKanban size={18} />
            Projects
          </a>
          <a className={page === 'agents' ? 'active' : ''} onClick={() => nav('agents')}>
            <Bot size={18} />
            Agents
          </a>
          <a className={page === 'prompts' ? 'active' : ''} onClick={() => nav('prompts')}>
            <ClipboardCheck size={18} />
            Prompts
          </a>
          <span className="nav-label">CONFIGURE</span>
          <a className={page === 'dimensions' ? 'active' : ''} onClick={() => nav('dimensions')}>
            <SlidersHorizontal size={18} />
            Dimensions
          </a>
        </nav>
      </aside>

      <main>
        <header>
          <button className="icon-btn mobile-menu" onClick={() => setMenu(true)}>
            <Menu />
          </button>
          <div className="crumb">
            <span>Workspace</span>
            <b>/</b>
            <strong>
              {page === 'home'
                ? project?.name || 'No project selected'
                : page[0].toUpperCase() + page.slice(1)}
            </strong>
          </div>
          <div className="header-actions">
            <span className="status">
              <i /> API connected
            </span>
            <button className="avatar">AK</button>
          </div>
        </header>

        {page === 'home' ? (
          <>
            <section className="content">
              <div className="hero">
                <div>
                  <p className="eyebrow">EVALUATION WORKSPACE</p>
                  <h1>Build reliable AI agents.</h1>
                  <p className="sub">
                    Configure your agent, define what good looks like, and evaluate every response with confidence.
                  </p>
                </div>
                <button className="primary" onClick={() => setModal('project')}>
                  <Plus size={18} />
                  New project
                </button>
              </div>

              {error && (
                <div className="alert error">
                  <AlertCircle size={18} />
                  {error}
                  <button onClick={() => setError('')}>
                    <X size={16} />
                  </button>
                </div>
              )}

              {notice && (
                <div className="alert success">
                  <CheckCircle2 size={18} />
                  {notice}
                  <button onClick={() => setNotice('')}>
                    <X size={16} />
                  </button>
                </div>
              )}

              <div className="selectors">
                <label>
                  Project
                  <select value={projectId || ''} onChange={(e) => setProjectId(Number(e.target.value))}>
                    <option value="">Select a project</option>
                    {projects.map((p) => (
                      <option key={p.id} value={p.id}>
                        {p.name}
                      </option>
                    ))}
                  </select>
                  <ChevronDown />
                </label>

                <label>
                  Agent
                  <select
                    value={agentId || ''}
                    onChange={(e) => setAgentId(Number(e.target.value))}
                    disabled={!projectId}
                  >
                    <option value="">Select an agent</option>
                    {agents.map((a) => (
                      <option key={a.id} value={a.id}>
                        {a.name}
                      </option>
                    ))}
                  </select>
                  <ChevronDown />
                </label>

                <button className="outline" disabled={!projectId} onClick={() => setModal('agent')}>
                  <Plus size={16} />
                  Add agent
                </button>
              </div>

              {!projectId ? (
                <Empty
                  icon={FolderKanban}
                  title="Create your first project"
                  text="Projects keep agents, prompts, and evaluation criteria in one place."
                  action={
                    <button className="primary" onClick={() => setModal('project')}>
                      <Plus size={17} />
                      Create project
                    </button>
                  }
                />
              ) : (
                <>
                  <div className="metrics">
                    <div>
                      <span>ACTIVE AGENTS</span>
                      <strong>{agents.length}</strong>
                      <em>
                        <ArrowUpRight size={14} /> Ready to evaluate
                      </em>
                    </div>
                    <div>
                      <span>EVALUATION CRITERIA</span>
                      <strong>{dimensions.length}</strong>
                      <em>Across this project</em>
                    </div>
                    <div>
                      <span>RUNS FOR THIS AGENT</span>
                      <strong>{evaluations.length}</strong>
                      <em>{evaluations.length ? 'Evaluation history available' : 'No runs yet'}</em>
                    </div>
                  </div>

                  <div className="grid">
                    <section className="card setup">
                      <div className="card-title">
                        <div>
                          <p className="eyebrow">AGENT SETUP</p>
                          <h2>{agent?.name || 'Choose an agent'}</h2>
                        </div>
                        <span className="pill">
                          {latestPrompt ? `v${latestPrompt.version}` : 'No prompt'}
                        </span>
                      </div>
                      {!agent ? (
                        <Empty
                          icon={Bot}
                          title="Add an agent"
                          text="Start by adding an agent to this project."
                          action={
                            <button className="outline" onClick={() => setModal('agent')}>
                              <Plus size={16} />
                              Add agent
                            </button>
                          }
                        />
                      ) : (
                        <>
                          <div className="prompt-preview">
                            <span>SYSTEM PROMPT</span>
                            <p>{latestPrompt?.text || 'No prompt configured yet.'}</p>
                          </div>
                          <button className="text-button" onClick={() => setModal('prompt')}>
                            <Plus size={16} />
                            {latestPrompt ? 'Create new prompt version' : 'Add system prompt'}
                          </button>
                        </>
                      )}
                    </section>

                    <section className="card criteria">
                      <div className="card-title">
                        <div>
                          <p className="eyebrow">QUALITY BAR</p>
                          <h2>Evaluation criteria</h2>
                        </div>
                        <button
                          className="text-button"
                          disabled={!projectId}
                          onClick={() => setModal('dimensions')}
                        >
                          <Plus size={16} />
                          Manage
                        </button>
                      </div>
                      {dimensions.length ? (
                        <div className="criteria-list">
                          {dimensions.map((d, i) => (
                            <div key={d.dimension_id || d[0] || i}>
                              <span>{String(i + 1).padStart(2, '0')}</span>
                              <p>
                                <strong>{d.dimension_name || d[1]}</strong>
                                <small>{d.dimension_description || d[2]}</small>
                              </p>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <Empty
                          icon={ClipboardCheck}
                          title="No criteria yet"
                          text="Add dimensions such as accuracy and tone to guide evaluations."
                          action={
                            <button className="outline" onClick={() => setModal('dimensions')}>
                              <Plus size={16} />
                              Add criteria
                            </button>
                          }
                        />
                      )}
                    </section>
                  </div>

                  <section className="card runner">
                    <div className="runner-copy">
                      <p className="eyebrow">TEST YOUR AGENT</p>
                      <h2>Run an evaluation</h2>
                      <p>
                        Send a real-world message to {agent?.name || 'your agent'} and score it against your configured criteria.
                      </p>
                    </div>
                    <RunBox
                      disabled={!agentId || !latestPrompt}
                      running={running}
                      onRun={run}
                      result={evaluationResult}
                    />
                  </section>

                  <section className="history">
                    <div>
                      <p className="eyebrow">RECENT ACTIVITY</p>
                      <h2>Evaluation history</h2>
                    </div>
                    {evaluations.length ? (
                      <div className="history-list">
                        {evaluations.slice(0, 5).map((e, i) => (
                          <article key={e.tracking_id || e[0] || i}>
                            <span className="run-icon">
                              <CheckCircle2 size={18} />
                            </span>
                            <div>
                              <strong>Evaluation run #{e.tracking_id || e[0]}</strong>
                              <p>{e.chat || e[3] || message || 'Agent response evaluated'}</p>
                            </div>
                            <time>
                              {e.timestamp || e[5]
                                ? new Date(e.timestamp || e[5]).toLocaleString()
                                : 'Completed'}
                            </time>
                          </article>
                        ))}
                      </div>
                    ) : (
                      <Empty
                        icon={Activity}
                        title="No evaluations yet"
                        text="Your completed evaluation runs will appear here."
                      />
                    )}
                  </section>
                </>
              )}
            </section>

            {modal === 'project' && (
              <SimpleForm
                title="Create a project"
                label="Project name"
                placeholder="e.g. Customer Support AI"
                submit="Create project"
                close={() => setModal(null)}
                onSubmit={(v) => create('project', { name: v })}
              />
            )}

            {modal === 'agent' && (
              <SimpleForm
                title="Add an agent"
                label="Agent name"
                placeholder="e.g. Support Assistant"
                submit="Add agent"
                close={() => setModal(null)}
                onSubmit={(v) => create('agent', { name: v })}
              />
            )}

            {modal === 'prompt' && (
              <PromptForm
                close={() => setModal(null)}
                onSubmit={(v) => create('prompt', { text: v })}
              />
            )}

            {modal === 'dimensions' && (
              <DimensionsForm
                close={() => setModal(null)}
                onSubmit={(v) => create('dimensions', v)}
              />
            )}
          </>
        ) : (
          <ManagePage
            type={page}
            projects={projects}
            projectId={projectId}
            setProjectId={setProjectId}
            agents={agents}
            agentId={agentId}
            setAgentId={setAgentId}
            refreshProjects={fetchProjects}
            refreshProject={() => fetchProjectData(projectId)}
            refreshAgent={() => fetchAgentData(agentId)}
            setError={setError}
            setNotice={setNotice}
          />
        )}
      </main>
    </div>
  );
}

function RunBox({ disabled, running, onRun, result }) {
  const [chat, setChat] = useState('');
  const summary = result?.response || result?.overall_assessment_summary;
  const score = result?.overall_score ?? result?.score;
  const dimensions =
    result?.benchmark_score || result?.dimensions_result || result?.dimensions_results || [];

  return (
    <div className="run-box">
      <textarea
        value={chat}
        onChange={(e) => setChat(e.target.value)}
        placeholder="Type a test message for your agent…"
        disabled={disabled}
      />
      <button
        className="primary"
        disabled={disabled || running || !chat.trim()}
        onClick={() => onRun(chat)}
      >
        {running ? <LoaderCircle className="spin" size={17} /> : <Send size={17} />}
        {running ? 'Evaluating…' : 'Run evaluation'}
      </button>
      {disabled && (
        <small>Add an agent and system prompt before running an evaluation.</small>
      )}
      {summary && (
        <div className="evaluation-output">
          <div className="output-title">
            <strong>Evaluation result</strong>
            {score !== undefined && <span>{Number(score).toFixed(1)} / 10</span>}
          </div>
          <p>{summary}</p>
          {dimensions.length > 0 && (
            <div className="score-chips">
              {dimensions.map((item, i) => (
                <span key={item.dimension || i}>
                  {item.dimension || `Criterion ${i + 1}`}: {item.score ?? item.benchmarkScore}/10
                </span>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function SimpleForm({ title, label, placeholder, submit, close, onSubmit }) {
  const [value, setValue] = useState('');

  return (
    <Modal title={title} close={close}>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          onSubmit(value);
        }}
      >
        <label className="field">
          {label}
          <input
            autoFocus
            required
            value={value}
            onChange={(e) => setValue(e.target.value)}
            placeholder={placeholder}
          />
        </label>
        <div className="form-actions">
          <button type="button" className="outline" onClick={close}>
            Cancel
          </button>
          <button className="primary">{submit}</button>
        </div>
      </form>
    </Modal>
  );
}

function PromptForm({ close, onSubmit }) {
  const [value, setValue] = useState('');

  return (
    <Modal title="Add system prompt" close={close}>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          onSubmit(value);
        }}
      >
        <label className="field">
          Instructions for the agent
          <textarea
            autoFocus
            required
            value={value}
            onChange={(e) => setValue(e.target.value)}
            placeholder="Describe the role, goals, style, and constraints…"
          />
        </label>
        <div className="form-actions">
          <button type="button" className="outline" onClick={close}>
            Cancel
          </button>
          <button className="primary">Save prompt</button>
        </div>
      </form>
    </Modal>
  );
}

function DimensionsForm({ close, onSubmit }) {
  const [items, setItems] = useState([
    {
      dimension_name: 'Accuracy',
      dimension_description: 'Response is factually correct and relevant.',
    },
  ]);

  const update = (i, key, value) => {
    setItems(items.map((x, n) => (n === i ? { ...x, [key]: value } : x)));
  };

  return (
    <Modal title="Set evaluation criteria" close={close}>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          onSubmit(items);
        }}
      >
        {items.map((item, i) => (
          <div className="dimension-form" key={i}>
            <input
              required
              value={item.dimension_name}
              onChange={(e) => update(i, 'dimension_name', e.target.value)}
              placeholder="Criterion name"
            />
            <input
              required
              value={item.dimension_description}
              onChange={(e) => update(i, 'dimension_description', e.target.value)}
              placeholder="What does good look like?"
            />
            {items.length > 1 && (
              <button
                type="button"
                className="icon-btn"
                onClick={() => setItems(items.filter((_, n) => n !== i))}
              >
                <X size={17} />
              </button>
            )}
          </div>
        ))}
        <button
          type="button"
          className="text-button"
          onClick={() => setItems([...items, { dimension_name: '', dimension_description: '' }])}
        >
          <Plus size={16} />
          Add another
        </button>
        <div className="form-actions">
          <button type="button" className="outline" onClick={close}>
            Cancel
          </button>
          <button className="primary">Save criteria</button>
        </div>
      </form>
    </Modal>
  );
}

function ManagePage({
  type,
  projects,
  projectId,
  setProjectId,
  agents,
  agentId,
  setAgentId,
  refreshProjects,
  refreshProject,
  refreshAgent,
  setError,
  setNotice,
}) {
  const [modal, setModal] = useState(null);
  const [edit, setEdit] = useState(null);
  const [reload, setReload] = useState(0);

  const title = {
    projects: 'Projects',
    agents: 'Agents',
    prompts: 'Prompts',
    dimensions: 'Dimensions',
  }[type];

  const message = {
    projects: 'Organize evaluation workspaces and their agents.',
    agents: 'Create and maintain the agents in each project.',
    prompts: 'Version your agent instructions with confidence.',
    dimensions: 'Define the quality criteria used in your evaluations.',
  }[type];

  const [items, setItems] = useState([]);

  useEffect(() => {
    if (type === 'dimensions' && projectId) {
      api.dimensions(projectId)
        .then(setItems)
        .catch(() => setItems([]));
    }
  }, [type, projectId]);

  const refresh = async () => {
    if (type === 'projects') {
      await refreshProjects();
    } else if (type === 'agents' || type === 'dimensions') {
      await refreshProject();
      if (type === 'dimensions' && projectId) {
        setItems(await api.dimensions(projectId).catch(() => []));
      }
    } else {
      await refreshAgent();
    }
    setReload((n) => n + 1);
  };

  const perform = async (action) => {
    try {
      await action();
      await refresh();
      setModal(null);
      setEdit(null);
      setNotice(`${title.slice(0, -1)} saved successfully.`);
    } catch (e) {
      setError(e.message);
    }
  };

  const remove = async (label, action) => {
    if (!window.confirm(`Delete this ${label}? This action cannot be undone.`)) return;
    try {
      await action();
      await refresh();
      setNotice(`${label[0].toUpperCase() + label.slice(1)} deleted.`);
    } catch (e) {
      setError(e.message);
    }
  };

  const projectSelect = (
    <label className="manager-select">
      Project
      <select value={projectId || ''} onChange={(e) => setProjectId(Number(e.target.value))}>
        <option value="">Select a project</option>
        {projects.map((p) => (
          <option key={p.id} value={p.id}>
            {p.name}
          </option>
        ))}
      </select>
      <ChevronDown size={15} />
    </label>
  );

  const agentSelect = (
    <label className="manager-select">
      Agent
      <select
        value={agentId || ''}
        onChange={(e) => setAgentId(Number(e.target.value))}
        disabled={!projectId}
      >
        <option value="">Select an agent</option>
        {agents.map((a) => (
          <option key={a.id} value={a.id}>
            {a.name}
          </option>
        ))}
      </select>
      <ChevronDown size={15} />
    </label>
  );

  let body;
  if (type === 'projects') {
    body = (
      <>
        <div className="manager-toolbar">
          <span>
            {projects.length} project{projects.length !== 1 ? 's' : ''}
          </span>
          <button className="primary" onClick={() => setModal('create')}>
            <Plus size={17} />
            New project
          </button>
        </div>
        <div className="manage-grid">
          {projects.map((p) => (
            <ManageCard
              key={p.id}
              title={p.name}
              meta={`Created ${p.createdAt ? new Date(p.createdAt).toLocaleDateString() : 'recently'}`}
              onEdit={() => setEdit({ id: p.id, value: p.name })}
              onDelete={() => remove('project', () => api.deleteProject(p.id))}
            />
          ))}
        </div>
        {!projects.length && (
          <Empty
            icon={FolderKanban}
            title="No projects yet"
            text="Create a project to start organizing your evaluation work."
          />
        )}
      </>
    );
  }

  if (type === 'agents') {
    body = (
      <>
        <div className="manager-toolbar">
          {projectSelect}
          <button className="primary" disabled={!projectId} onClick={() => setModal('create')}>
            <Plus size={17} />
            New agent
          </button>
        </div>
        {projectId ? (
          <div className="manage-grid">
            {agents.map((a) => (
              <ManageCard
                key={a.id}
                icon={<Bot size={19} />}
                title={a.name}
                meta={`Agent ID #${a.id}`}
                onEdit={() => setEdit({ id: a.id, value: a.name })}
                onDelete={() => remove('agent', () => api.deleteAgent(a.id))}
              />
            ))}
          </div>
        ) : (
          <Empty
            icon={Bot}
            title="Select a project"
            text="Choose a project above to manage its agents."
          />
        )}
        {projectId && !agents.length && (
          <Empty
            icon={Bot}
            title="No agents in this project"
            text="Add your first agent to begin creating prompts and evaluations."
          />
        )}
      </>
    );
  }

  if (type === 'prompts') {
    body = (
      <>
        <div className="manager-toolbar selectors-inline">
          {projectSelect}
          {agentSelect}
          <button className="primary" disabled={!agentId} onClick={() => setModal('create')}>
            <Plus size={17} />
            New prompt
          </button>
        </div>
        {agentId ? (
          <PromptList
            agentId={agentId}
            reload={reload}
            onEdit={(p) => setEdit({ id: p.id, value: p.text })}
            onDelete={(id) => remove('prompt', () => api.deletePrompt(id))}
          />
        ) : (
          <Empty
            icon={ClipboardCheck}
            title="Select an agent"
            text="Choose a project and agent to manage its prompt versions."
          />
        )}
      </>
    );
  }

  if (type === 'dimensions') {
    body = (
      <>
        <div className="manager-toolbar">
          {projectSelect}
          <button className="primary" disabled={!projectId} onClick={() => setModal('create')}>
            <Plus size={17} />
            Add dimensions
          </button>
        </div>
        {projectId ? (
          <div className="dimension-list">
            {items.map((d, i) => {
              const id = d.dimension_id || d[0];
              const name = d.dimension_name || d[1];
              const desc = d.dimension_description || d[2];
              return (
                <ManageCard
                  key={id || i}
                  title={name}
                  meta={desc}
                  onEdit={() => setEdit({ id, value: desc, dimension: true })}
                  onDelete={() => remove('dimension', () => api.deleteDimension(id))}
                />
              );
            })}
          </div>
        ) : (
          <Empty
            icon={SlidersHorizontal}
            title="Select a project"
            text="Choose a project to manage its evaluation criteria."
          />
        )}
        {projectId && !items.length && (
          <Empty
            icon={SlidersHorizontal}
            title="No dimensions yet"
            text="Add criteria like accuracy, helpfulness, and tone."
          />
        )}
      </>
    );
  }

  const submitCreate = (value) => {
    if (type === 'projects') return perform(() => api.createProject(value));
    if (type === 'agents') return perform(() => api.createAgent(projectId, value));
    if (type === 'prompts') return perform(() => api.createPrompt(agentId, value));
  };

  return (
    <section className="content manager-page">
      <div className="hero">
        <div>
          <p className="eyebrow">MANAGE WORKSPACE</p>
          <h1>{title}</h1>
          <p className="sub">{message}</p>
        </div>
      </div>
      {body}
      {modal === 'create' && type === 'dimensions' && (
        <DimensionsForm
          close={() => setModal(null)}
          onSubmit={(v) => perform(() => api.setDimensions(projectId, v))}
        />
      )}
      {modal === 'create' && type !== 'dimensions' && (
        <SimpleForm
          title={`Create ${title.slice(0, -1)}`}
          label={`${title.slice(0, -1)} name`}
          placeholder={`Enter ${title.slice(0, -1)} name`}
          submit="Create"
          close={() => setModal(null)}
          onSubmit={submitCreate}
        />
      )}
      {edit && (
        <EditForm
          item={edit}
          label={edit.dimension ? 'Criterion description' : `${title.slice(0, -1)} name`}
          close={() => setEdit(null)}
          onSubmit={(v) =>
            perform(() =>
              edit.dimension
                ? api.updateDimension(edit.id, v)
                : type === 'projects'
                  ? api.updateProject(edit.id, v)
                  : type === 'agents'
                    ? api.updateAgent(edit.id, v)
                    : api.updatePrompt(edit.id, v)
            )
          }
        />
      )}
    </section>
  );
}

function ManageCard({ icon, title, meta, onEdit, onDelete }) {
  return (
    <article className="manage-card">
      {icon && <span className="manage-icon">{icon}</span>}
      <div>
        <h3>{title}</h3>
        <p>{meta}</p>
      </div>
      <div className="row-actions">
        <button className="icon-btn" aria-label="Edit" onClick={onEdit}>
          <Pencil size={16} />
        </button>
        <button className="icon-btn danger" aria-label="Delete" onClick={onDelete}>
          <Trash2 size={16} />
        </button>
      </div>
    </article>
  );
}

function PromptList({ agentId, reload, onEdit, onDelete }) {
  const [list, setList] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    api.prompts(agentId)
      .then((x) => setList(unpack(x).map(asPrompt)))
      .catch(() => setList([]))
      .finally(() => setLoading(false));
  }, [agentId, reload]);

  if (loading) {
    return (
      <div className="inline-load">
        <LoaderCircle className="spin" /> Loading prompts…
      </div>
    );
  }

  return list.length ? (
    <div className="prompt-list">
      {list
        .sort((a, b) => b.version - a.version)
        .map((p) => (
          <article key={p.id} className="manage-card">
            <span className="pill">v{p.version}</span>
            <div>
              <h3>Prompt version {p.version}</h3>
              <p>{p.text}</p>
            </div>
            <div className="row-actions">
              <button className="icon-btn" onClick={() => onEdit(p)}>
                <Pencil size={16} />
              </button>
              <button className="icon-btn danger" onClick={() => onDelete(p.id)}>
                <Trash2 size={16} />
              </button>
            </div>
          </article>
        ))}
    </div>
  ) : (
    <Empty
      icon={ClipboardCheck}
      title="No prompts yet"
      text="Add a system prompt to give this agent clear instructions."
    />
  );
}

function EditForm({ item, label, close, onSubmit }) {
  const [value, setValue] = useState(item.value);

  return (
    <Modal title={`Edit ${label.toLowerCase()}`} close={close}>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          onSubmit(value);
        }}
      >
        <label className="field">
          {label}
          {item.dimension ? (
            <textarea
              autoFocus
              required
              value={value}
              onChange={(e) => setValue(e.target.value)}
            />
          ) : (
            <input
              autoFocus
              required
              value={value}
              onChange={(e) => setValue(e.target.value)}
            />
          )}
        </label>
        <div className="form-actions">
          <button type="button" className="outline" onClick={close}>
            Cancel
          </button>
          <button className="primary">Save changes</button>
        </div>
      </form>
    </Modal>
  );
}
