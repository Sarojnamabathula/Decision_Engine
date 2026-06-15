from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.routes import router as v1_router
from app.middleware import RequestIDMiddleware
from configs.settings import settings
from rules.registry import registry
from services.logging_service import logger

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.api_version,
        debug=settings.debug
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Request ID
    app.add_middleware(RequestIDMiddleware)

    # Routers
    app.include_router(v1_router, prefix="/api/v1")

    @app.get("/", include_in_schema=False)
    async def root():
        from fastapi.responses import HTMLResponse
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Decision Engine | Strategic Interview Analytics</title>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
            <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@400;500;600&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
            <style>
                :root {
                    --bg: #020617;
                    --sidebar: rgba(15, 23, 42, 0.7);
                    --card: rgba(30, 41, 59, 0.5);
                    --primary: #6366f1;
                    --primary-glow: rgba(99, 102, 241, 0.4);
                    --accent: #a855f7;
                    --text: #f8fafc;
                    --text-muted: #94a3b8;
                    --bot-msg: rgba(30, 41, 59, 0.8);
                    --user-msg: rgba(79, 70, 229, 0.7);
                    --border: rgba(255, 255, 255, 0.08);
                }
                
                * { box-sizing: border-box; }
                body {
                    margin: 0;
                    font-family: 'Inter', sans-serif;
                    background: var(--bg);
                    color: var(--text);
                    display: flex;
                    height: 100vh;
                    overflow: hidden;
                    position: relative;
                }
                
                #three-canvas {
                    position: absolute;
                    top: 0; left: 0; width: 100%; height: 100%;
                    z-index: 0;
                }

                /* Sidebar Layout */
                .sidebar {
                    width: 420px;
                    background: var(--sidebar);
                    backdrop-filter: blur(40px) saturate(200%);
                    border-right: 1px solid var(--border);
                    display: flex;
                    flex-direction: column;
                    z-index: 10;
                    box-shadow: 25px 0 60px rgba(0,0,0,0.6);
                }

                .sidebar-header {
                    padding: 2.5rem;
                    border-bottom: 1px solid var(--border);
                }
                .sidebar-header h2 { 
                    font-family: 'Outfit', sans-serif; 
                    margin: 0; 
                    font-size: 1.8rem;
                    font-weight: 800;
                    letter-spacing: -0.02em;
                    background: linear-gradient(135deg, #818cf8 0%, #c084fc 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }
                .sidebar-header p {
                    margin: 0.5rem 0 0 0;
                    font-size: 0.75rem;
                    color: var(--text-muted);
                    text-transform: uppercase;
                    letter-spacing: 0.15em;
                    font-weight: 700;
                }

                .sidebar-scroll {
                    flex: 1;
                    overflow-y: auto;
                    padding: 2rem;
                    display: flex;
                    flex-direction: column;
                    gap: 1.5rem;
                }
                
                .section-label {
                    font-size: 0.7rem;
                    font-weight: 800;
                    color: var(--primary);
                    text-transform: uppercase;
                    letter-spacing: 0.1em;
                    margin-bottom: 0.5rem;
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                }
                .section-label::after { content: ''; flex: 1; height: 1px; background: var(--border); }

                .control-group {
                    background: var(--card);
                    padding: 1.25rem;
                    border-radius: 1.25rem;
                    border: 1px solid var(--border);
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                }
                .control-group:hover { border-color: var(--primary-glow); background: rgba(30, 41, 59, 0.7); }

                select {
                    width: 100%;
                    background: #0f172a;
                    border: 1px solid var(--border);
                    border-radius: 0.75rem;
                    padding: 0.8rem;
                    color: white;
                    font-family: inherit;
                    font-size: 0.95rem;
                    outline: none;
                    cursor: pointer;
                }

                .slider-info { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; }
                .slider-info label { font-size: 0.8rem; font-weight: 600; color: var(--text-muted); }
                .slider-val { font-family: 'Outfit', sans-serif; font-weight: 700; color: var(--accent); }

                input[type="range"] {
                    -webkit-appearance: none;
                    width: 100%;
                    height: 4px;
                    background: rgba(255,255,255,0.08);
                    border-radius: 2px;
                    outline: none;
                }
                input[type="range"]::-webkit-slider-thumb {
                    -webkit-appearance: none;
                    width: 16px; height: 16px;
                    background: var(--primary);
                    border: 2px solid white;
                    border-radius: 50%;
                    cursor: pointer;
                    box-shadow: 0 0 10px var(--primary-glow);
                    transition: 0.2s;
                }

                /* Observation Deck (Stats in Sidebar) */
                .observation-deck {
                    background: rgba(2, 6, 23, 0.6);
                    border-radius: 1.25rem;
                    padding: 1.5rem;
                    border: 1px solid var(--primary-glow);
                    margin-top: 1rem;
                }
                .stat-row { display: flex; flex-direction: column; gap: 0.25rem; margin-bottom: 1.2rem; }
                .stat-row:last-child { margin-bottom: 0; }
                .stat-label { font-size: 0.65rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase; }
                .stat-value { font-family: 'Outfit', sans-serif; font-size: 1.4rem; font-weight: 700; color: var(--primary); }
                .trace-terminal {
                    background: #020617;
                    border-radius: 0.75rem;
                    padding: 1rem;
                    font-family: 'Fira Code', monospace;
                    font-size: 0.7rem;
                    color: #64748b;
                    max-height: 180px;
                    overflow-y: auto;
                    border: 1px solid var(--border);
                    margin-top: 0.5rem;
                }
                .trace-line { margin-bottom: 0.4rem; border-left: 2px solid var(--primary); padding-left: 0.6rem; }

                .sidebar-footer {
                    padding: 2rem;
                    border-top: 1px solid var(--border);
                    background: rgba(15, 23, 42, 0.4);
                }

                /* Main Experience */
                .main-experience {
                    flex: 1;
                    display: flex;
                    flex-direction: column;
                    z-index: 10;
                    position: relative;
                }

                #chat-container {
                    flex: 1;
                    padding: 4rem 6rem;
                    overflow-y: auto;
                    display: flex;
                    flex-direction: column;
                    gap: 2.5rem;
                    scroll-behavior: smooth;
                }
                
                .message {
                    max-width: 80%;
                    padding: 1.8rem;
                    border-radius: 1.5rem;
                    font-size: 1.05rem;
                    line-height: 1.6;
                    backdrop-filter: blur(12px);
                    border: 1px solid var(--border);
                    animation: messagePop 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                    box-shadow: 0 15px 40px rgba(0,0,0,0.3);
                }
                @keyframes messagePop {
                    from { opacity: 0; transform: translateY(20px) scale(0.95); }
                    to { opacity: 1; transform: translateY(0) scale(1); }
                }

                .bot-message { align-self: flex-start; background: var(--bot-msg); border-bottom-left-radius: 0.2rem; }
                .bot-message b { color: var(--primary); font-family: 'Outfit', sans-serif; letter-spacing: 0.05em; }
                
                .user-message { 
                    align-self: flex-end; 
                    background: var(--user-msg); 
                    border-bottom-right-radius: 0.2rem; 
                    border-color: rgba(99, 102, 241, 0.4);
                    color: white;
                }

                .input-portal {
                    padding: 3rem 6rem;
                    background: linear-gradient(to top, var(--bg) 60%, transparent);
                    display: flex;
                    flex-direction: column;
                    gap: 1.5rem;
                }
                .input-wrap {
                    display: flex;
                    gap: 1.2rem;
                    background: rgba(30, 41, 59, 0.6);
                    padding: 0.6rem;
                    border-radius: 1.5rem;
                    border: 1px solid var(--border);
                    box-shadow: 0 20px 50px rgba(0,0,0,0.4);
                }
                
                #user-input {
                    flex: 1;
                    background: transparent;
                    border: none;
                    padding: 1rem 1.5rem;
                    color: white;
                    font-size: 1.1rem;
                    outline: none;
                }
                
                .btn {
                    padding: 0.8rem 2rem;
                    border-radius: 1rem;
                    font-weight: 700;
                    cursor: pointer;
                    transition: all 0.3s;
                    border: none;
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    font-family: 'Outfit', sans-serif;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                }
                .btn-primary {
                    background: var(--primary);
                    color: white;
                    box-shadow: 0 10px 20px var(--primary-glow);
                }
                .btn-primary:hover:not(:disabled) { transform: translateY(-3px); box-shadow: 0 15px 30px var(--primary-glow); }
                .btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }

                .btn-ghost {
                    background: rgba(255,255,255,0.03);
                    color: var(--text-muted);
                    border: 1px solid var(--border);
                }
                .btn-ghost:hover:not(:disabled) { background: rgba(255,255,255,0.08); color: white; border-color: var(--primary); }

                .action-deck { display: flex; gap: 1rem; justify-content: center; }

                /* Hide Scrollbar */
                ::-webkit-scrollbar { width: 6px; }
                ::-webkit-scrollbar-track { background: transparent; }
                ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 10px; }
                ::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }
            </style>
        </head>
        <body>
            <canvas id="three-canvas"></canvas>

            <aside class="sidebar">
                <div class="sidebar-header">
                    <h2>DECISION CORE</h2>
                    <p>Intelligence Orchestrator</p>
                </div>
                
                <div class="sidebar-scroll">
                    <div class="section-label">Session Parameters</div>
                    
                    <div class="control-group">
                        <label style="font-size:0.7rem; font-weight:800; color:var(--text-muted); display:block; margin-bottom:0.6rem;">TARGET DOMAIN</label>
                        <select id="i-domain">
                            <option value="software">COMPUTATIONAL SYSTEMS ENGINEERING</option>
                            <option value="data">QUANTITATIVE DATA ANALYTICS</option>
                            <option value="ml">ARTIFICIAL INTELLIGENCE & MACHINE LEARNING</option>
                            <option value="product">STRATEGIC PRODUCT ORCHESTRATION</option>
                            <option value="cyber">ADVANCED CYBER DEFENSE & CRYPTOGRAPHY</option>
                            <option value="cloud">CLOUD-NATIVE INFRASTRUCTURE & DEVOPS</option>
                            <option value="quantum">QUANTUM COMPUTING & INFORMATION THEORY</option>
                            <option value="systems">HIGH-PERFORMANCE DISTRIBUTED SYSTEMS</option>
                        </select>
                    </div>

                    <div class="control-group">
                        <div class="slider-info">
                            <label>ANSWER PRECISION</label>
                            <span class="slider-val" id="v-score">0.80</span>
                        </div>
                        <input type="range" id="i-score" min="0" max="1" step="0.05" value="0.80">
                    </div>

                    <div class="control-group">
                        <div class="slider-info">
                            <label>EVALUATOR CONFIDENCE</label>
                            <span class="slider-val" id="v-conf">0.90</span>
                        </div>
                        <input type="range" id="i-conf" min="0" max="1" step="0.05" value="0.90">
                    </div>

                    <div class="control-group">
                        <div class="slider-info">
                            <label>SEMANTIC RELEVANCE</label>
                            <span class="slider-val" id="v-rel">0.95</span>
                        </div>
                        <input type="range" id="i-rel" min="0" max="1" step="0.05" value="0.95">
                    </div>

                    <div class="control-group">
                        <div class="slider-info">
                            <label>COGNITIVE FATIGUE</label>
                            <span class="slider-val" id="v-fat">0.10</span>
                        </div>
                        <input type="range" id="i-fat" min="0" max="1" step="0.05" value="0.10">
                    </div>

                    <div class="section-label">Observation Deck</div>
                    
                    <div class="observation-deck" id="obs-deck" style="opacity: 0.5;">
                        <div class="stat-row">
                            <span class="stat-label">Logic State</span>
                            <span class="stat-value" id="s-rule" style="font-size: 1rem;">IDLE</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-label">Intelligence Score</span>
                            <span class="stat-value" id="s-comp">0.0000</span>
                        </div>
                        <span class="stat-label">Decision Trace</span>
                        <div class="trace-terminal" id="s-trace">
                            <div class="trace-line">Awaiting session initialization...</div>
                        </div>
                    </div>
                </div>

                <div class="sidebar-footer">
                    <button onclick="startInterview()" id="start-btn" class="btn btn-primary" style="width:100%; justify-content:center; padding:1.2rem;">INITIALIZE SESSION</button>
                    <button onclick="resetSim()" class="btn btn-ghost" style="width:100%; justify-content:center; margin-top:0.8rem; font-size:0.8rem;">SYSTEM RESET</button>
                </div>
            </aside>

            <main class="main-experience">
                <div id="chat-container">
                    <div class="message bot-message">
                        <b>SYSTEM STATUS: ONLINE</b><br>
                        Ready to conduct a high-fidelity candidate assessment. Please configure the target domain and session parameters to initiate the sequence.
                    </div>
                </div>

                <div class="input-portal">
                    <div class="input-wrap">
                        <input type="text" id="user-input" placeholder="Inject candidate signal data..." onkeypress="if(event.key==='Enter') sendTurn()" disabled>
                        <button class="btn btn-primary" id="send-btn" onclick="sendTurn()" disabled>ANALYZE</button>
                    </div>
                    <div class="action-deck">
                        <button class="btn btn-ghost" id="skip-btn" onclick="skipQuestion()" disabled><span>⏩</span> SKIP</button>
                        <button class="btn btn-ghost" id="next-btn" onclick="forceNext()" disabled><span>⏭️</span> FORCE NEXT</button>
                    </div>
                </div>
            </main>

            <script>
                /* Enhanced Three.js Background (Neural Mesh) */
                const scene = new THREE.Scene();
                const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
                const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('three-canvas'), alpha: true, antialias: true });
                renderer.setSize(window.innerWidth, window.innerHeight);

                const geometry = new THREE.SphereGeometry(10, 32, 32);
                const material = new THREE.PointsMaterial({ size: 0.04, color: 0x6366f1, transparent: true, opacity: 0.3 });
                const points = new THREE.Points(geometry, material);
                scene.add(points);

                // Add some floating nodes
                const nodeCount = 50;
                const nodeGeo = new THREE.BufferGeometry();
                const nodePos = new Float32Array(nodeCount * 3);
                for(let i=0; i<nodeCount*3; i++) nodePos[i] = (Math.random() - 0.5) * 25;
                nodeGeo.setAttribute('position', new THREE.BufferAttribute(nodePos, 3));
                const nodeMat = new THREE.PointsMaterial({ size: 0.1, color: 0xa855f7, transparent: true, opacity: 0.6 });
                const nodes = new THREE.Points(nodeGeo, nodeMat);
                scene.add(nodes);

                camera.position.z = 12;

                function animate() {
                    requestAnimationFrame(animate);
                    points.rotation.y += 0.001;
                    nodes.rotation.x += 0.0005;
                    nodes.rotation.y += 0.0008;
                    renderer.render(scene, camera);
                }
                animate();

                window.addEventListener('resize', () => {
                    camera.aspect = window.innerWidth / window.innerHeight;
                    camera.updateProjectionMatrix();
                    renderer.setSize(window.innerWidth, window.innerHeight);
                });

                /* Formalized Interview Content */
                const questions = {
                    software: [
                        "Could you please explain the technical distinctions between optimistic and pessimistic locking strategies, and specify the scenarios where each would be most appropriate?",
                        "How would you approach the architectural design of a highly available, distributed rate-limiting system that must handle millions of requests per second?",
                        "In your professional experience, what are the primary architectural trade-offs to consider when migrating from a monolithic structure to a microservices ecosystem?"
                    ],
                    data: [
                        "Could you elaborate on the theoretical implications of the 'curse of dimensionality' in high-dimensional feature spaces and its effect on model performance?",
                        "How do you formally define and manage the bias-variance trade-off when optimizing complex predictive models for generalization?",
                        "What is your systematic approach to identifying and mitigating non-random missing data patterns in large-scale enterprise datasets?"
                    ],
                    ml: [
                        "Could you provide a rigorous comparative analysis of Transformer architectures versus Recurrent Neural Networks for large-scale sequential data processing?",
                        "Could you explain the mathematical foundations and the gradient descent optimization process specifically within Gradient Boosting Machines?",
                        "What methodologies would you employ to detect and resolve training-serving skew in production machine learning pipelines?"
                    ],
                    product: [
                        "Could you describe your formal framework for prioritizing features within a complex product roadmap that has multiple competing stakeholders?",
                        "Can you share a specific instance where you led a data-driven pivot, and describe the methodology used to validate the new strategic direction?",
                        "What key performance indicators would you define to rigorously measure the long-term success and user engagement of a cross-platform notification system?"
                    ],
                    cyber: [
                        "Could you please elaborate on your methodology for architecting a Zero Trust security framework within a heterogeneous enterprise environment?",
                        "How would you approach the technical mitigation of a sophisticated Advanced Persistent Threat (APT) targeting critical infrastructure?",
                        "What are the core cryptographic principles you would employ to ensure end-to-end data integrity in a distributed ledger system?"
                    ],
                    cloud: [
                        "Could you explain your strategy for managing complex multi-cloud deployments while ensuring consistent security and compliance standards?",
                        "How do you approach the optimization of serverless architectures to balance latency requirements with cost-efficiency in high-traffic scenarios?",
                        "What is your systematic process for implementing robust Disaster Recovery (DR) and business continuity plans in a cloud-native ecosystem?"
                    ],
                    quantum: [
                        "Could you please explain the theoretical principles behind Shor's algorithm and its implications for contemporary RSA encryption?",
                        "How do you define and manage decoherence in superconducting qubits to maintain computational fidelity in a quantum processor?",
                        "What is your understanding of the Variational Quantum Eigensolver (VQE) and its application in molecular simulation?"
                    ],
                    systems: [
                        "How would you design a consensus algorithm that maintains Byzantine Fault Tolerance in a network with high latency and significant node churn?",
                        "Could you discuss the trade-offs between strong consistency and eventual consistency in the design of a globally distributed database?",
                        "What are the primary architectural challenges in optimizing memory-mapped I/O for low-latency financial trading systems?"
                    ]
                };

                let turnCount = 0, followUpCount = 0, currentQuestionIdx = 0;
                const sessionId = "sim-" + Math.random().toString(36).substring(2, 11);

                window.addEventListener('DOMContentLoaded', () => {
                    ['score', 'conf', 'rel', 'fat'].forEach(id => {
                        const el = document.getElementById('i-'+id);
                        if(el) el.addEventListener('input', (e) => document.getElementById('v-'+id).innerText = parseFloat(e.target.value).toFixed(2));
                    });
                });

                function startInterview() {
                    const domain = document.getElementById('i-domain').value;
                    document.getElementById('obs-deck').style.opacity = '1';
                    addMessage(`<b>SYSTEM:</b> Session initialized. Target Domain: ${domain.toUpperCase()}`, 'bot-message');
                    addMessage(`<b>Lead Interviewer:</b> "Welcome. To begin our assessment: ${questions[domain][0]}"`, 'bot-message');
                    ['user-input', 'send-btn', 'skip-btn', 'next-btn'].forEach(id => document.getElementById(id).disabled = false);
                    document.getElementById('start-btn').disabled = true;
                    document.getElementById('i-domain').disabled = true;
                }

                function skipQuestion() {
                    addMessage("<i>[Requesting question skip]</i>", 'user-message');
                    const domain = document.getElementById('i-domain').value;
                    currentQuestionIdx++;
                    const nextQ = questions[domain][currentQuestionIdx % questions[domain].length];
                    addMessage(`<b>Lead Interviewer:</b> "Understood. Let us pivot to a different topic: ${nextQ}"`, 'bot-message');
                }

                function forceNext() {
                    addMessage("<i>[Forcing sequence progression]</i>", 'user-message');
                    const domain = document.getElementById('i-domain').value;
                    currentQuestionIdx++;
                    const nextQ = questions[domain][currentQuestionIdx % questions[domain].length];
                    addMessage(`<b>Lead Interviewer:</b> "Acknowledged. Moving the discussion forward: ${nextQ}"`, 'bot-message');
                }

                async function sendTurn() {
                    const input = document.getElementById('user-input');
                    const text = input.value.trim() || "[Candidate Signal Injected]";
                    addMessage(text, 'user-message');
                    input.value = '';
                    const btn = document.getElementById('send-btn');
                    btn.disabled = true;

                    const payload = {
                        session_id: sessionId,
                        score: parseFloat(document.getElementById('i-score').value),
                        confidence: parseFloat(document.getElementById('i-conf').value),
                        topic_relevance: parseFloat(document.getElementById('i-rel').value),
                        sentiment: "positive", 
                        response_time: 45.0, 
                        follow_up_count: followUpCount, 
                        attempts: 1, 
                        candidate_fatigue: parseFloat(document.getElementById('i-fat').value),
                        contradiction_detected: false, 
                        question_difficulty: "medium",
                        question_type: "technical",
                        answer_length: text.length || 10
                    };

                    try {
                        const response = await fetch('/api/v1/decide', {
                            method: 'POST', headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(payload)
                        });
                        
                        if (!response.ok) {
                            const errorData = await response.json();
                            addMessage(`<b>[ERROR]</b> Intelligence Core rejected request: ${response.status} ${response.statusText}<br><small>${JSON.stringify(errorData)}</small>`, 'bot-message');
                            btn.disabled = false;
                            return;
                        }

                        const data = await response.json();
                        turnCount++;
                        if(data.action === 'follow_up') followUpCount++; else followUpCount = 0;

                        document.getElementById('s-comp').innerText = data.composite_score.toFixed(4);
                        document.getElementById('s-rule').innerText = data.rule_triggered;
                        document.getElementById('s-trace').innerHTML = data.decision_trace.map(t => `<div class="trace-line">${t}</div>`).join('');
                        document.getElementById('s-trace').scrollTop = document.getElementById('s-trace').scrollHeight;

                        let botText = data.explanation;
                        if(data.action === 'next_question') {
                            currentQuestionIdx++;
                            const domain = document.getElementById('i-domain').value;
                            botText = `<b>[ANALYSIS COMPLETE]</b> ${botText} <br><br><b>Lead Interviewer:</b> "${questions[domain][currentQuestionIdx % questions[domain].length]}"`;
                        } else if(data.action === 'follow_up') {
                            botText = `<b>[INSUFFICIENT SIGNAL]</b> ${botText} <br><br><b>Lead Interviewer:</b> "I would appreciate it if you could provide additional depth and specific examples regarding your previous point."`;
                        } else {
                            botText = `<b>[SESSION TERMINATED]</b> ${botText} <br><br><b>Lead Interviewer:</b> "Thank you for your time. The assessment is now complete."`;
                        }
                        addMessage(botText, 'bot-message');
                        if(data.action === 'end_interview') { 
                            ['user-input', 'send-btn', 'skip-btn', 'next-btn'].forEach(id => document.getElementById(id).disabled = true);
                        }
                    } catch (e) { 
                        console.error(e);
                        addMessage("<b>[ERROR]</b> Connection to intelligence core severed. Please check server logs.", 'bot-message'); 
                    }
                    finally { btn.disabled = false; input.focus(); }
                }

                function addMessage(text, className) {
                    const win = document.getElementById('chat-container');
                    const div = document.createElement('div');
                    div.className = 'message ' + className;
                    div.innerHTML = text;
                    win.appendChild(div);
                    win.scrollTop = win.scrollHeight;
                }
                function resetSim() { location.reload(); }
            </script>
        </body>
        </html>
        """)

    @app.on_event("startup")
    async def startup_event():
        logger.info("Starting up AI Decision Engine")
        registry.initialize(settings.rules_file_path)
        logger.info(f"Loaded {len(registry.get_rules())} rules from {settings.rules_file_path}")

    return app

app = create_app()
