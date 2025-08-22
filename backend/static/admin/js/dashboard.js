// JuSimples Admin Dashboard - Core JavaScript Module

class AdminDashboard {
    constructor() {
        this.currentPage = 'dashboard';
        this.charts = {};
        this.refreshInterval = null;
        this.settings = {
            autoRefresh: true,
            refreshRate: 30000,
            animations: true,
            theme: 'dark'
        };
        // Page state
        this.kbState = {
            documents: [],
            categories: [],
            filtered: [],
            page: 1,
            pageSize: 10,
            search: '',
            category: 'all',
            selected: new Set(),
            sort: { key: 'title', dir: 'asc' }
        };
        this.logsState = { entries: [], filtered: [], page: 1, pageSize: 10, search: '', level: 'all', sort: { key: 'timestamp', dir: 'desc' } };
        this.usersState = { users: [], filtered: [], page: 1, pageSize: 10, search: '', role: 'all', selected: new Set(), sort: { key: 'name', dir: 'asc' } };
        
        // Monitoring state
        this.monitoring = { autoRefresh: false, intervalMs: 10000 };
        this.monitoringInterval = null;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadDashboard();
        this.startAutoRefresh();
        this.initCharts();
    }

    setupEventListeners() {
        // Mobile menu toggle
        document.getElementById('mobile-menu-toggle')?.addEventListener('click', () => {
            document.getElementById('sidebar').classList.toggle('open');
        });

        // Page navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const page = link.dataset.page;
                this.navigateToPage(page);
            });
        });

        // Refresh button
        document.getElementById('refresh-btn')?.addEventListener('click', () => {
            this.refreshData();
        });

        // Fullscreen toggle
        document.getElementById('fullscreen-btn')?.addEventListener('click', () => {
            this.toggleFullscreen();
        });

        // Knowledge Base: Add document
        document.getElementById('kb-add-btn')?.addEventListener('click', () => {
            document.getElementById('kb-file-input')?.click();
        });

        // Knowledge Base: File input change -> upload
        document.getElementById('kb-file-input')?.addEventListener('change', async (e) => {
            const file = e.target.files?.[0];
            if (!file) return;
            try {
                await this.uploadKnowledgeDocument(file);
                // reset input to allow same file re-upload later
                e.target.value = '';
            } catch (err) {
                console.error(err);
                this.showNotification('Upload failed', 'error');
            }
        });

        // Knowledge Base: Reindex
        document.getElementById('kb-reindex-btn')?.addEventListener('click', async () => {
            try {
                const res = await fetch('/admin/api/knowledge-base/reindex', { method: 'POST' });
                const data = await res.json();
                if (data?.success) this.showNotification('Reindexing started', 'success');
                else this.showNotification(data?.message || 'Reindex request sent', 'info');
            } catch (err) {
                console.error(err);
                this.showNotification('Failed to start reindex', 'error');
            }
        });
    }

    navigateToPage(pageName) {
        // Update active nav
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
            if (link.dataset.page === pageName) {
                link.classList.add('active');
            }
        });

        // Hide all pages
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });

        // Show selected page
        const page = document.getElementById(`${pageName}-page`);
        if (page) {
            const prev = this.currentPage;
            if (prev === 'monitoring') {
                this.stopMonitoringAutoRefresh();
            }
            page.classList.add('active');
            this.currentPage = pageName;
            this.loadPageContent(pageName);
            this.updatePageTitle(pageName);
        }
    }

    updatePageTitle(pageName) {
        const titles = {
            dashboard: 'Dashboard Overview',
            knowledge: 'Knowledge Base Management',
            training: 'Training & Fine-tuning',
            database: 'Database Management',
            analytics: 'Analytics & Reports',
            llm: 'LLM Configuration',
            monitoring: 'System Monitoring',
            users: 'User Management',
            logs: 'System Logs',
            settings: 'System Settings',
            openai: 'OpenAI Dashboard',
            lextml: 'LexML API'
        };

        const titleElement = document.getElementById('page-title');
        if (titleElement) {
            const icon = document.querySelector(`.nav-link[data-page="${pageName}"] i`);
            titleElement.innerHTML = `
                ${icon ? icon.outerHTML : ''}
                <span>${titles[pageName] || pageName}</span>
            `;
        }
    }

    async loadPageContent(pageName) {
        const loaders = {
            dashboard: () => this.loadDashboardContent(),
            knowledge: () => this.loadKnowledgeContent(),
            training: () => this.loadTrainingContent(),
            database: () => this.loadDatabaseContent(),
            analytics: () => this.loadAnalyticsContent(),
            llm: () => this.loadLLMContent(),
            monitoring: () => this.loadMonitoringContent(),
            users: () => this.loadUsersContent(),
            logs: () => this.loadLogsContent(),
            settings: () => this.loadSettingsContent(),
            openai: () => this.loadOpenAIContent(),
            lextml: () => this.loadLexMLContent()
        };

        if (loaders[pageName]) {
            await loaders[pageName]();
        }
    }

    async loadDashboard() {
        try {
            const response = await fetch('/admin/api/dashboard-stats');
            const data = await response.json();
            this.updateDashboardStats(data);
        } catch (error) {
            console.error('Error loading dashboard:', error);
        }
    }

    updateDashboardStats(data) {
        // Update stat cards
        const stats = {
            'total-queries': data.totalQueries || 0,
            'active-users': data.activeUsers || 0,
            'knowledge-docs': data.knowledgeDocs || 0,
            'response-time': data.avgResponseTime || '0ms',
            'success-rate': data.successRate || '0%',
            'system-health': data.systemHealth || 'Checking...'
        };

        Object.entries(stats).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                this.animateValue(element, value);
            }
        });
    }

    animateValue(element, value) {
        if (typeof value === 'number') {
            const start = parseInt(element.textContent) || 0;
            const duration = 1000;
            const startTime = performance.now();
            
            const update = (currentTime) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                
                const current = start + (value - start) * this.easeOutQuart(progress);
                element.textContent = Math.round(current).toLocaleString();
                
                if (progress < 1) {
                    requestAnimationFrame(update);
                }
            };
            
            requestAnimationFrame(update);
        } else {
            element.textContent = value;
        }
    }

    easeOutQuart(t) {
        return 1 - Math.pow(1 - t, 4);
    }

    // ---------- UI Utilities ----------
    ensureModalRoot() {
        let root = document.getElementById('app-modal-root');
        if (!root) {
            root = document.createElement('div');
            root.id = 'app-modal-root';
            document.body.appendChild(root);
        }
        return root;
    }

    openModal(html) {
        const root = this.ensureModalRoot();
        root.innerHTML = `
          <div class="modal-overlay" style="position:fixed;inset:0;background:rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center;z-index:1000;">
            <div class="modal" style="background:#111827;border:1px solid #2d2f53;border-radius:12px;min-width:320px;max-width:520px;padding:16px;box-shadow:0 10px 30px rgba(0,0,0,.5)">
              ${html}
            </div>
          </div>`;
        const overlay = root.querySelector('.modal-overlay');
        overlay.addEventListener('click', (e)=>{ if (e.target === overlay) this.closeModal(); });
    }

    closeModal() {
        const root = document.getElementById('app-modal-root');
        if (root) root.innerHTML = '';
    }

    confirmModal(message, { confirmText = 'Confirm', cancelText = 'Cancel' } = {}) {
        return new Promise((resolve) => {
            this.openModal(`
              <div class="modal-header" style="font-weight:600;margin-bottom:12px">Confirm</div>
              <div style="margin-bottom:16px;color:#c0c4ff">${message}</div>
              <div style="display:flex;gap:8px;justify-content:flex-end">
                <button class="btn btn-secondary" id="modal-cancel">${cancelText}</button>
                <button class="btn btn-danger" id="modal-confirm">${confirmText}</button>
              </div>
            `);
            document.getElementById('modal-cancel').addEventListener('click', ()=>{ this.closeModal(); resolve(false); });
            document.getElementById('modal-confirm').addEventListener('click', ()=>{ this.closeModal(); resolve(true); });
        });
    }

    promptModal(title, defaultValue = '') {
        return new Promise((resolve) => {
            const inputId = 'modal-input-' + Math.random().toString(36).slice(2);
            this.openModal(`
              <div class="modal-header" style="font-weight:600;margin-bottom:12px">${title}</div>
              <input id="${inputId}" class="form-input" style="width:100%;margin-bottom:12px" value="${(defaultValue||'').replace(/"/g,'&quot;')}" />
              <div style="display:flex;gap:8px;justify-content:flex-end">
                <button class="btn btn-secondary" id="modal-cancel">Cancel</button>
                <button class="btn btn-primary" id="modal-ok">OK</button>
              </div>
            `);
            const input = document.getElementById(inputId);
            setTimeout(()=> input?.focus(), 0);
            document.getElementById('modal-cancel').addEventListener('click', ()=>{ this.closeModal(); resolve(null); });
            const done = ()=>{ const v = input?.value ?? null; this.closeModal(); resolve(v); };
            document.getElementById('modal-ok').addEventListener('click', done);
            input?.addEventListener('keydown', (e)=>{ if (e.key==='Enter') done(); });
        });
    }

    debounce(fn, delay = 300) {
        let t;
        return (...args)=>{
            clearTimeout(t);
            t = setTimeout(()=> fn.apply(this, args), delay);
        };
    }

    compareValues(a, b, dir = 'asc') {
        const na = (a===null || a===undefined);
        const nb = (b===null || b===undefined);
        if (na && nb) return 0;
        if (na) return dir==='asc' ? -1 : 1;
        if (nb) return dir==='asc' ? 1 : -1;
        const sa = ('' + a).toLowerCase();
        const sb = ('' + b).toLowerCase();
        if (sa < sb) return dir==='asc' ? -1 : 1;
        if (sa > sb) return dir==='asc' ? 1 : -1;
        return 0;
    }

    initCharts() {
        // Initialize all charts when dashboard loads
        this.initQueryVolumeChart();
        this.initResponseTimeChart();
        this.initCategoryChart();
        this.initSystemMetricsChart();
    }

    initQueryVolumeChart() {
        const ctx = document.getElementById('query-volume-chart');
        if (!ctx) return;

        this.charts.queryVolume = new Chart(ctx, {
            type: 'line',
            data: {
                labels: this.generateTimeLabels(24),
                datasets: [{
                    label: 'Queries',
                    data: Array(24).fill(0).map(() => Math.floor(Math.random() * 100)),
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: this.getChartOptions()
        });
    }

    initResponseTimeChart() {
        const ctx = document.getElementById('response-time-chart');
        if (!ctx) return;

        this.charts.responseTime = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['< 100ms', '100-500ms', '500-1000ms', '> 1000ms'],
                datasets: [{
                    label: 'Responses',
                    data: [45, 30, 20, 5],
                    backgroundColor: ['#10b981', '#3b82f6', '#f59e0b', '#ef4444']
                }]
            },
            options: this.getChartOptions()
        });
    }

    initCategoryChart() {
        const ctx = document.getElementById('category-chart');
        if (!ctx) return;

        this.charts.category = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Trabalhista', 'Civil', 'Penal', 'Tributário', 'Outros'],
                datasets: [{
                    data: [30, 25, 20, 15, 10],
                    backgroundColor: ['#6366f1', '#8b5cf6', '#3b82f6', '#10b981', '#f59e0b']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#a0a0c0' }
                    }
                }
            }
        });
    }

    initSystemMetricsChart() {
        const ctx = document.getElementById('system-metrics-chart');
        if (!ctx) return;

        this.charts.systemMetrics = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['CPU', 'Memory', 'Disk', 'Network', 'Database', 'Cache'],
                datasets: [{
                    label: 'Current',
                    data: [45, 62, 38, 71, 55, 82],
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.2)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100,
                        ticks: { color: '#6b7280' },
                        grid: { color: 'rgba(255, 255, 255, 0.05)' }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }

    getChartOptions() {
        return {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#1e1e3f',
                    titleColor: '#fff',
                    bodyColor: '#a0a0c0',
                    borderColor: '#6366f1',
                    borderWidth: 1
                }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#6b7280' }
                },
                y: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#6b7280' }
                }
            }
        };
    }

    generateTimeLabels(hours) {
        const labels = [];
        const now = new Date();
        for (let i = hours - 1; i >= 0; i--) {
            const time = new Date(now - i * 3600000);
            labels.push(time.getHours() + ':00');
        }
        return labels;
    }

    async loadDashboardContent() {
        // Update charts with latest data
        this.updateCharts();
        
        // Load activity feed
        this.loadActivityFeed();
        
        // Update real-time metrics
        this.updateRealtimeMetrics();
    }

    async updateCharts() {
        // Simulate updating chart data
        if (this.charts.queryVolume) {
            this.charts.queryVolume.data.datasets[0].data = Array(24).fill(0).map(() => Math.floor(Math.random() * 100));
            this.charts.queryVolume.update();
        }
    }

    loadActivityFeed() {
        const feed = document.getElementById('activity-feed');
        if (!feed) return;

        const activities = [
            { icon: 'fa-question', text: 'New legal query received', time: '2 min ago', type: 'info' },
            { icon: 'fa-check', text: 'Document indexed successfully', time: '5 min ago', type: 'success' },
            { icon: 'fa-user', text: 'User session started', time: '12 min ago', type: 'info' },
            { icon: 'fa-database', text: 'Database backup completed', time: '1 hour ago', type: 'success' }
        ];

        feed.innerHTML = activities.map(activity => `
            <div class="feed-item">
                <div class="feed-icon bg-${activity.type}">
                    <i class="fas ${activity.icon}"></i>
                </div>
                <div class="feed-content">
                    <div>${activity.text}</div>
                    <div class="feed-time">${activity.time}</div>
                </div>
            </div>
        `).join('');
    }

    updateRealtimeMetrics() {
        // Simulate real-time updates
        setInterval(() => {
            const responseTime = document.getElementById('response-time');
            if (responseTime) {
                const time = Math.floor(Math.random() * 500) + 100;
                responseTime.textContent = `${time}ms`;
            }
        }, 3000);
    }

    async refreshData() {
        this.showNotification('Refreshing data...', 'info');
        await this.loadDashboard();
        await this.loadPageContent(this.currentPage);
        this.showNotification('Data refreshed successfully', 'success');
    }

    toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen();
        } else {
            document.exitFullscreen();
        }
    }

    startAutoRefresh() {
        if (this.settings.autoRefresh) {
            this.refreshInterval = setInterval(() => {
                this.refreshData();
            }, this.settings.refreshRate);
        }
    }

    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'error' ? 'exclamation-circle' : type === 'success' ? 'check-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    }

    // Page-specific content loaders
    async loadKnowledgeContent() {
        const res = await fetch('/admin/api/knowledge-base');
        const data = await res.json();
        this.kbState.documents = data.documents || [];
        this.kbState.categories = ['all', ...(data.categories || [])];
        this.kbState.page = 1;
        this.kbState.selected.clear();

        const container = document.getElementById('knowledge-content');
        if (!container) return;
        container.innerHTML = `
            <div class="card">
              <div class="toolbar">
                <div class="controls">
                  <input id="kb-search" class="form-input" placeholder="Search documents..." />
                  <div id="kb-chips" class="chips"></div>
                </div>
              </div>

              <div class="table-wrapper">
                <table class="data-table">
                  <thead>
                    <tr>
                      <th><input type="checkbox" id="kb-select-all" class="checkbox"/></th>
                      <th class="sortable" data-sort="title">Title</th>
                      <th class="sortable" data-sort="category">Category</th>
                      <th class="sortable" data-sort="keywords">Keywords</th>
                      <th class="sortable" data-sort="created">Created</th>
                      <th class="sortable" data-sort="modified">Updated</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody id="kb-tbody"></tbody>
                </table>
              </div>

              <div class="toolbar">
                <div class="controls">
                  <button id="kb-delete-selected" class="btn btn-danger btn-sm" disabled><i class="fas fa-trash"></i> Delete Selected</button>
                  <button id="kb-export" class="btn btn-secondary btn-sm"><i class="fas fa-file-export"></i> Export</button>
                </div>
                <div id="kb-pagination" class="pagination"></div>
              </div>
            </div>
        `;

        // Render chips and table
        this.renderKbChips();
        this.applyKnowledgeFilters();
        this.bindKnowledgeActions();
    }

    async loadTrainingContent() {
        const container = document.getElementById('training-content');
        if (!container) return;
        const res = await fetch('/admin/api/training/status');
        const data = await res.json();
        container.innerHTML = `
          <div class="card">
            <div class="card-header">
              <div class="card-title"><i class="fas fa-brain"></i> Training & Fine-tuning</div>
              <div class="table-actions">
                <button id="train-start" class="btn btn-success btn-sm"><i class="fas fa-play"></i> Start</button>
                <button id="train-stop" class="btn btn-danger btn-sm"><i class="fas fa-stop"></i> Stop</button>
              </div>
            </div>
            <div class="stats-grid">
              <div class="stat-card"><div class="stat-label">Model</div><div class="stat-value">${data.currentModel}</div></div>
              <div class="stat-card"><div class="stat-label">Status</div><div class="stat-value">${data.trainingStatus}</div></div>
              <div class="stat-card"><div class="stat-label">Accuracy</div><div class="stat-value">${data.accuracy}%</div></div>
              <div class="stat-card"><div class="stat-label">Loss</div><div class="stat-value">${data.loss}</div></div>
            </div>
            <h4 style="margin:16px 0 8px">Datasets</h4>
            <table class="data-table">
              <thead><tr><th>Name</th><th>Size</th><th>Status</th></tr></thead>
              <tbody>
                ${(data.datasets||[]).map(d=>`<tr><td>${d.name}</td><td>${d.size}</td><td>${d.status}</td></tr>`).join('')}
              </tbody>
            </table>
          </div>`;
        document.getElementById('train-start')?.addEventListener('click', ()=> this.showNotification('Training job started (mock)', 'success'));
        document.getElementById('train-stop')?.addEventListener('click', ()=> this.showNotification('Training stop requested (mock)', 'info'));
    }

    async loadDatabaseContent() {
        const res = await fetch('/admin/api/database/overview');
        const data = await res.json();
        const c = document.getElementById('database-content');
        if (!c) return;
        c.innerHTML = `
          <div class="stats-grid">
            <div class="stat-card"><div class="stat-label">Documents</div><div class="stat-value">${data.counts?.legal_chunks || 0}</div></div>
            <div class="stat-card"><div class="stat-label">Search Logs</div><div class="stat-value">${data.counts?.search_logs || 0}</div></div>
            <div class="stat-card"><div class="stat-label">Ask Logs</div><div class="stat-value">${data.counts?.ask_logs || 0}</div></div>
            <div class="stat-card"><div class="stat-label">Users</div><div class="stat-value">${data.counts?.users || 0}</div></div>
          </div>
          <div class="card">
            <div class="card-title"><i class="fas fa-database"></i> Size</div>
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin-top:12px;">
              <div class="stat-card"><div class="stat-label">Total</div><div class="stat-value">${data.size?.total}</div></div>
              <div class="stat-card"><div class="stat-label">Used</div><div class="stat-value">${data.size?.used}</div></div>
              <div class="stat-card"><div class="stat-label">Free</div><div class="stat-value">${data.size?.free}</div></div>
            </div>
          </div>
          <div class="card">
            <div class="card-title"><i class="fas fa-tachometer-alt"></i> Performance</div>
            <div class="stats-grid" style="margin-top:12px;">
              <div class="stat-card"><div class="stat-label">Avg Query Time</div><div class="stat-value">${data.performance?.avgQueryTime}</div></div>
              <div class="stat-card"><div class="stat-label">Slow Queries</div><div class="stat-value">${data.performance?.slowQueries}</div></div>
              <div class="stat-card"><div class="stat-label">Connections</div><div class="stat-value">${data.performance?.connections}</div></div>
            </div>
          </div>`;
    }

    async loadAnalyticsContent() {
        const c = document.getElementById('analytics-content');
        if (!c) return;

        // Show loading state
        c.innerHTML = `
          <div class="loading-container" style="text-align: center; padding: 40px;">
            <i class="fas fa-spinner fa-spin" style="font-size: 24px; margin-bottom: 16px;"></i>
            <div>Loading analytics data...</div>
          </div>
        `;

        try {
            // Load analytics data from multiple endpoints
            const [overviewRes, trendsRes, realtimeRes, ragRes] = await Promise.all([
                fetch('/admin/api/analytics/overview'),
                fetch('/admin/api/analytics/trends'), 
                fetch('/admin/api/analytics/realtime'),
                fetch('/admin/api/rag/performance')
            ]);
            
            const [overview, trends, realtime, ragData] = await Promise.all([
                overviewRes.json(),
                trendsRes.json(), 
                realtimeRes.json(),
                ragRes.json()
            ]);

            // Create analytics dashboard with proper pagination controls
            c.innerHTML = `
              <div class="analytics-header" style="display: flex; justify-content: between; align-items: center; margin-bottom: 20px;">
                <h2 style="margin: 0;">Analytics Dashboard</h2>
                <div class="analytics-controls" style="display: flex; gap: 12px; align-items: center;">
                  <select id="analytics-period" class="form-select" style="min-width: 120px;">
                    <option value="24h">Last 24 hours</option>
                    <option value="7d" selected>Last 7 days</option>
                    <option value="30d">Last 30 days</option>
                  </select>
                  <button onclick="dashboard.loadAnalyticsContent()" class="btn btn-secondary">
                    <i class="fas fa-refresh"></i> Refresh
                  </button>
                </div>
              </div>

              <div class="stats-grid">
                <div class="stat-card">
                  <div class="stat-label">Total Queries</div>
                  <div class="stat-value">${overview.total_queries || 0}</div>
                  <div class="stat-change positive">+${realtime.queries_last_5min || 0} in last 5min</div>
                </div>
                <div class="stat-card">
                  <div class="stat-label">Success Rate</div>
                  <div class="stat-value">${Math.round(overview.success_rate || 0)}%</div>
                  <div class="stat-change ${overview.success_rate >= 95 ? 'positive' : 'negative'}">
                    ${overview.success_rate >= 95 ? 'Excellent' : 'Needs attention'}
                  </div>
                </div>
                <div class="stat-card">
                  <div class="stat-label">Avg Response Time</div>
                  <div class="stat-value">${Math.round(overview.avg_response_time || 0)}ms</div>
                  <div class="stat-change ${overview.avg_response_time <= 1000 ? 'positive' : 'negative'}">
                    ${overview.avg_response_time <= 1000 ? 'Fast' : 'Slow'}
                  </div>
                </div>
                <div class="stat-card">
                  <div class="stat-label">Active Sessions</div>
                  <div class="stat-value">${realtime.active_sessions || 0}</div>
                  <div class="stat-change neutral">Real-time</div>
                </div>
              </div>

              <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-top: 20px;">
                <div class="card">
                  <div class="card-header">
                    <div class="card-title"><i class="fas fa-chart-line"></i> Query Trends (24h)</div>
                  </div>
                  <div style="height: 300px; padding: 16px;">
                    <canvas id="trendsChart" width="400" height="200"></canvas>
                  </div>
                </div>

                <div class="card">
                  <div class="card-header">
                    <div class="card-title"><i class="fas fa-clock"></i> Recent Activity</div>
                  </div>
                  <div class="recent-activity" style="max-height: 300px; overflow-y: auto;">
                    ${realtime.latest_queries?.slice(0, 10).map(q => `
                      <div class="activity-item" style="display: flex; justify-content: space-between; padding: 8px 16px; border-bottom: 1px solid #e5e7eb;">
                        <div>
                          <div style="font-weight: 500; color: #1f2937;">${q.query?.substring(0, 50) || 'Query'}...</div>
                          <div style="font-size: 12px; color: #6b7280;">${q.session_id || 'Unknown session'}</div>
                        </div>
                        <span class="status-badge ${q.success ? 'success' : 'error'}" style="font-size: 11px;">
                          ${q.success ? 'Success' : 'Error'}
                        </span>
                      </div>
                    `).join('') || '<div style="text-align: center; color: #6b7280; padding: 40px;">No recent activity</div>'}
                  </div>
                </div>
              </div>

              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;">
                <div class="card">
                  <div class="card-header">
                    <div class="card-title"><i class="fas fa-tags"></i> Top Categories</div>
                  </div>
                  <div style="padding: 16px;">
                    ${overview.top_categories?.slice(0, 8).map(cat => `
                      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="font-weight: 500;">${cat.category}</span>
                        <div style="display: flex; align-items: center; gap: 8px;">
                          <div style="background: #e5e7eb; height: 8px; width: 100px; border-radius: 4px; overflow: hidden;">
                            <div style="background: #3b82f6; height: 100%; width: ${Math.min(100, (cat.count / Math.max(1, overview.top_categories[0]?.count || 1)) * 100)}%; transition: width 0.3s ease;"></div>
                          </div>
                          <span style="font-weight: 600; color: #1f2937; min-width: 30px;">${cat.count}</span>
                        </div>
                      </div>
                    `).join('') || '<div style="text-align: center; color: #6b7280;">No category data available</div>'}
                  </div>
                </div>

                <div class="card">
                  <div class="card-header">
                    <div class="card-title"><i class="fas fa-robot"></i> RAG Performance</div>
                  </div>
                  <div style="padding: 16px;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px;">
                      <div style="text-align: center; padding: 12px; background: #f9fafb; border-radius: 6px;">
                        <div style="font-size: 24px; font-weight: 700; color: #1f2937;">${ragData.data?.llm_performance?.total_calls || 0}</div>
                        <div style="font-size: 12px; color: #6b7280;">LLM Calls</div>
                      </div>
                      <div style="text-align: center; padding: 12px; background: #f9fafb; border-radius: 6px;">
                        <div style="font-size: 24px; font-weight: 700; color: #1f2937;">$${ragData.data?.llm_performance?.total_cost?.toFixed(4) || '0.0000'}</div>
                        <div style="font-size: 12px; color: #6b7280;">Total Cost</div>
                      </div>
                    </div>
                    <div style="border-top: 1px solid #e5e7eb; padding-top: 12px;">
                      <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                        <span style="font-size: 14px; color: #6b7280;">Avg Tokens/Request</span>
                        <span style="font-weight: 600;">${ragData.data?.llm_performance?.avg_tokens_per_request || 0}</span>
                      </div>
                      <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                        <span style="font-size: 14px; color: #6b7280;">Success Rate</span>
                        <span style="font-weight: 600; color: ${ragData.data?.llm_performance?.success_rate >= 95 ? '#10b981' : '#ef4444'};">
                          ${ragData.data?.llm_performance?.success_rate || 0}%
                        </span>
                      </div>
                      <div style="display: flex; justify-content: space-between;">
                        <span style="font-size: 14px; color: #6b7280;">Context Quality</span>
                        <span style="font-weight: 600;">${ragData.data?.context_quality?.good_context_rate || 0}%</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            `;

            // Initialize trends chart
            this.initTrendsChart(trends);

            // Add period change handler (no infinite scroll needed)
            const periodSelect = document.getElementById('analytics-period');
            if (periodSelect) {
                periodSelect.addEventListener('change', () => {
                    this.loadAnalyticsContent();
                });
            }
            
        } catch (error) {
            console.error('Error loading analytics:', error);
            c.innerHTML = `
              <div class="card">
                <div class="card-header">
                  <div class="card-title"><i class="fas fa-exclamation-triangle"></i> Analytics Error</div>
                </div>
                <div style="text-align: center; padding: 40px;">
                  <p>Failed to load analytics data. Please try refreshing the page.</p>
                  <button onclick="dashboard.loadAnalyticsContent()" class="btn btn-primary">
                    <i class="fas fa-refresh"></i> Retry
                  </button>
                </div>
              </div>
            `;
        }
    }

    initTrendsChart(trends) {
        // Destroy existing charts to prevent memory leaks
        if (this.charts.analyticsHourly) {
            this.charts.analyticsHourly.destroy();
        }
        if (this.charts.analyticsDaily) {
            this.charts.analyticsDaily.destroy();
        }
        
        // Initialize trends chart 
        const trendsCtx = document.getElementById('trendsChart');
        if (trendsCtx && trends) {
            if (this.charts.trends) {
                this.charts.trends.destroy();
            }
            
            const labels = trends.map(t => new Date(t.hour).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }));
            const queryData = trends.map(t => t.total_queries || 0);
            const responseData = trends.map(t => t.avg_response_time || 0);
            
            this.charts.trends = new Chart(trendsCtx, {
                type: 'line',
                data: {
                    labels,
                    datasets: [{
                        label: 'Total Queries',
                        data: queryData,
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        fill: true,
                        tension: 0.4,
                        yAxisID: 'y'
                    }, {
                        label: 'Avg Response Time (ms)',
                        data: responseData,
                        borderColor: '#ef4444',
                        backgroundColor: 'rgba(239, 68, 68, 0.1)',
                        fill: false,
                        yAxisID: 'y1'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            type: 'linear',
                            display: true,
                            position: 'left',
                            title: { display: true, text: 'Queries' }
                        },
                        y1: {
                            type: 'linear',
                            display: true,
                            position: 'right',
                            title: { display: true, text: 'Response Time (ms)' },
                            grid: { drawOnChartArea: false }
                        }
                    }
                }
            });
        }
    }

    async loadLLMContent() {
        const c = document.getElementById('llm-content');
        if (!c) return;
        
        // Show loading state
        c.innerHTML = `
          <div class="loading-container" style="text-align: center; padding: 40px;">
            <i class="fas fa-spinner fa-spin" style="font-size: 24px; margin-bottom: 16px;"></i>
            <div>Loading LLM configuration and performance data...</div>
          </div>
        `;
        
        try {
            const res = await fetch('/admin/api/llm/config');
            const cfg = await res.json();
            
            // Create comprehensive LLM dashboard
            c.innerHTML = `
              <div class="stats-grid" style="margin-bottom: 20px;">
                <div class="stat-card ${cfg.status === 'connected' ? 'success' : 'warning'}">
                  <div class="stat-label">Connection Status</div>
                  <div class="stat-value">${cfg.status === 'connected' ? 'Connected' : 'Not Configured'}</div>
                </div>
                <div class="stat-card">
                  <div class="stat-label">Total Requests (7d)</div>
                  <div class="stat-value">${cfg.usage_stats?.total_requests || 0}</div>
                </div>
                <div class="stat-card">
                  <div class="stat-label">Success Rate</div>
                  <div class="stat-value">${cfg.usage_stats?.success_rate || '0%'}</div>
                </div>
                <div class="stat-card">
                  <div class="stat-label">Total Cost (7d)</div>
                  <div class="stat-value">${cfg.usage_stats?.total_cost || '$0.00'}</div>
                </div>
              </div>
              
              <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-bottom: 20px;">
                <form id="llm-form" class="card">
                  <div class="card-header">
                    <div class="card-title"><i class="fas fa-robot"></i> LLM Configuration</div>
                    <button type="submit" class="btn btn-primary btn-sm"><i class="fas fa-save"></i> Save Configuration</button>
                  </div>
                  
                  <div class="form-group">
                    <label class="form-label">Active Model</label>
                    <select name="activeModel" class="form-select">
                      ${cfg.available_models?.map(model => `
                        <option value="${model.id}" ${model.id === cfg.activeModel ? 'selected' : ''}>
                          ${model.name} - ${model.description}
                        </option>
                      `).join('') || ''}
                    </select>
                  </div>
                  
                  <div class="form-group">
                    <label class="form-label">API Key Status</label>
                    <input disabled class="form-input" value="${cfg.apiKey || 'Not Set'}" />
                    <small style="color: #6b7280; font-size: 12px;">Configure API key via environment variables</small>
                  </div>
                  
                  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                    <div class="form-group">
                      <label class="form-label">Temperature</label>
                      <input name="temperature" type="number" step="0.1" min="0" max="2" class="form-input" value="${cfg.temperature}" />
                      <small style="color: #6b7280; font-size: 12px;">Controls randomness (0-2)</small>
                    </div>
                    <div class="form-group">
                      <label class="form-label">Max Tokens</label>
                      <input name="maxTokens" type="number" min="1" max="8192" class="form-input" value="${cfg.maxTokens}" />
                      <small style="color: #6b7280; font-size: 12px;">Maximum response length</small>
                    </div>
                  </div>
                  
                  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                    <div class="form-group">
                      <label class="form-label">Top P</label>
                      <input name="topP" type="number" step="0.1" min="0" max="1" class="form-input" value="${cfg.topP}" />
                      <small style="color: #6b7280; font-size: 12px;">Nuclear sampling (0-1)</small>
                    </div>
                    <div class="form-group">
                      <label class="form-label">Frequency Penalty</label>
                      <input name="frequencyPenalty" type="number" step="0.1" min="-2" max="2" class="form-input" value="${cfg.frequencyPenalty}" />
                      <small style="color: #6b7280; font-size: 12px;">Reduce repetition (-2 to 2)</small>
                    </div>
                  </div>
                  
                  <div class="form-group">
                    <label class="form-label">System Prompt</label>
                    <textarea name="systemPrompt" class="form-textarea" rows="4" placeholder="Enter system prompt to guide the AI's behavior...">${cfg.systemPrompt || ''}</textarea>
                    <small style="color: #6b7280; font-size: 12px;">Instructions that guide the AI's responses</small>
                  </div>
                </form>
                
                <div class="card">
                  <div class="card-header">
                    <div class="card-title"><i class="fas fa-chart-bar"></i> Performance Metrics (7d)</div>
                  </div>
                  <div style="padding: 16px;">
                    <div class="metric-row" style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                      <span>Avg Response Time:</span>
                      <strong>${cfg.usage_stats?.avg_response_time || '0ms'}</strong>
                    </div>
                    <div class="metric-row" style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                      <span>Total Tokens Used:</span>
                      <strong>${cfg.usage_stats?.total_tokens || 0}</strong>
                    </div>
                    <div class="metric-row" style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                      <span>Successful Requests:</span>
                      <strong>${cfg.usage_stats?.successful_requests || 0}</strong>
                    </div>
                    <div class="metric-row" style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                      <span>Models Used:</span>
                      <strong>${cfg.usage_stats?.models_used || 0}</strong>
                    </div>
                  </div>
                </div>
              </div>
              
              ${cfg.recent_errors && cfg.recent_errors.length > 0 ? `
                <div class="card">
                  <div class="card-header">
                    <div class="card-title"><i class="fas fa-exclamation-triangle"></i> Recent Errors (7d)</div>
                  </div>
                  <div style="max-height: 200px; overflow-y: auto;">
                    ${cfg.recent_errors.map(error => `
                      <div style="display: flex; justify-content: space-between; padding: 8px 16px; border-bottom: 1px solid #e5e7eb;">
                        <span style="flex: 1; font-size: 14px; color: #374151;">${error.error}</span>
                        <span style="font-weight: 600; color: #ef4444;">${error.count}x</span>
                      </div>
                    `).join('')}
                  </div>
                </div>
              ` : ''}
              
              <div class="card">
                <div class="card-header">
                  <div class="card-title"><i class="fas fa-info-circle"></i> Model Information</div>
                </div>
                <div class="model-info" style="padding: 16px;">
                  <h4 style="margin: 0 0 12px 0; color: #374151;">Available Models:</h4>
                  ${cfg.available_models?.map(model => `
                    <div class="model-card" style="padding: 12px; margin-bottom: 8px; border: 1px solid #e5e7eb; border-radius: 6px; ${model.id === cfg.activeModel ? 'background-color: #f0f9ff; border-color: #6366f1;' : ''}">
                      <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                          <strong style="color: #1f2937;">${model.name}</strong>
                          ${model.id === cfg.activeModel ? '<span style="color: #6366f1; font-size: 12px; margin-left: 8px;">(Active)</span>' : ''}
                          <div style="font-size: 14px; color: #6b7280; margin-top: 4px;">${model.description}</div>
                        </div>
                      </div>
                    </div>
                  `).join('') || '<p style="color: #6b7280;">No model information available</p>'}
                </div>
              </div>
            `;
            
            // Bind form submission
            document.getElementById('llm-form')?.addEventListener('submit', async (e) => {
                e.preventDefault();
                const form = e.currentTarget;
                const payload = Object.fromEntries(new FormData(form).entries());
                
                // Convert numeric fields
                payload.temperature = parseFloat(payload.temperature);
                payload.maxTokens = parseInt(payload.maxTokens, 10);
                payload.topP = parseFloat(payload.topP);
                payload.frequencyPenalty = parseFloat(payload.frequencyPenalty);
                
                try {
                    const resp = await fetch('/admin/api/llm/config', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });
                    
                    const result = await resp.json();
                    
                    if (resp.ok) {
                        this.showNotification(result.message || 'LLM configuration updated successfully', 'success');
                        // Reload the page to show updated config
                        setTimeout(() => this.loadLLMContent(), 1000);
                    } else {
                        this.showNotification(result.error || 'Failed to update LLM configuration', 'error');
                    }
                } catch (error) {
                    console.error('Error updating LLM config:', error);
                    this.showNotification('Failed to update LLM configuration', 'error');
                }
            });
            
        } catch (error) {
            console.error('Error loading LLM content:', error);
            c.innerHTML = `
              <div class="card">
                <div class="card-header">
                  <div class="card-title"><i class="fas fa-exclamation-triangle"></i> LLM Configuration Error</div>
                </div>
                <div style="text-align: center; padding: 40px;">
                  <p>Failed to load LLM configuration. Please check your connection and try again.</p>
                  <button onclick="dashboard.loadLLMContent()" class="btn btn-primary">
                    <i class="fas fa-refresh"></i> Retry
                  </button>
                </div>
              </div>
            `;
        }
    }

    async loadRAGMonitoring() {
        try {
            const [ragRes, vectorRes, librariesRes] = await Promise.all([
                fetch('/admin/api/rag/performance'),
                fetch('/admin/api/vector/health'),
                fetch('/admin/api/libraries/metrics')
            ]);
            
            const [ragData, vectorData, librariesData] = await Promise.all([
                ragRes.json(),
                vectorRes.json(),
                librariesRes.json()
            ]);
            
            return { ragData, vectorData, librariesData };
        } catch (error) {
            console.error('Error loading RAG monitoring data:', error);
            return null;
        }
    }

    async loadLibrariesContent() {
        const c = document.getElementById('libraries-content');
        if (!c) return;
        
        // Show loading state
        c.innerHTML = `
          <div class="loading-container" style="text-align: center; padding: 40px;">
            <i class="fas fa-spinner fa-spin" style="font-size: 24px; margin-bottom: 16px;"></i>
            <div>Loading API libraries monitoring...</div>
          </div>
        `;
        
        try {
            const res = await fetch('/admin/api/libraries/metrics');
            const data = await res.json();
            
            c.innerHTML = `
              <div class="stats-grid" style="margin-bottom: 20px;">
                <div class="stat-card">
                  <div class="stat-label">Total APIs</div>
                  <div class="stat-value">${data.data?.total_apis || 0}</div>
                </div>
                <div class="stat-card">
                  <div class="stat-label">Total Calls (7d)</div>
                  <div class="stat-value">${data.data?.api_metrics?.reduce((sum, api) => sum + api.total_calls, 0) || 0}</div>
                </div>
                <div class="stat-card">
                  <div class="stat-label">Success Rate</div>
                  <div class="stat-value">${data.data?.api_metrics?.length > 0 ? 
                    Math.round(data.data.api_metrics.reduce((sum, api) => sum + api.success_rate, 0) / data.data.api_metrics.length) : 0}%</div>
                </div>
                <div class="stat-card">
                  <div class="stat-label">Total Cost (7d)</div>
                  <div class="stat-value">$${data.data?.api_metrics?.reduce((sum, api) => sum + api.total_cost, 0).toFixed(4) || '0.0000'}</div>
                </div>
              </div>
              
              <div class="card">
                <div class="card-header">
                  <div class="card-title"><i class="fas fa-plug"></i> External API Libraries</div>
                </div>
                <div class="api-libraries-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; padding: 16px;">
                  ${data.data?.api_metrics?.map(api => `
                    <div class="api-card" style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 16px;">
                      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <h4 style="margin: 0; color: #1f2937; text-transform: uppercase;">${api.api_name}</h4>
                        <span class="status-badge ${api.success_rate >= 95 ? 'success' : api.success_rate >= 80 ? 'warning' : 'error'}" 
                              style="padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600;">
                          ${api.success_rate >= 95 ? 'Healthy' : api.success_rate >= 80 ? 'Warning' : 'Error'}
                        </span>
                      </div>
                      <div class="api-metrics" style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                        <div>
                          <div style="font-size: 12px; color: #6b7280;">Total Calls</div>
                          <div style="font-weight: 600; color: #1f2937;">${api.total_calls}</div>
                        </div>
                        <div>
                          <div style="font-size: 12px; color: #6b7280;">Success Rate</div>
                          <div style="font-weight: 600; color: #1f2937;">${api.success_rate}%</div>
                        </div>
                        <div>
                          <div style="font-size: 12px; color: #6b7280;">Avg Response</div>
                          <div style="font-weight: 600; color: #1f2937;">${api.avg_response_time}ms</div>
                        </div>
                        <div>
                          <div style="font-size: 12px; color: #6b7280;">Total Cost</div>
                          <div style="font-weight: 600; color: #1f2937;">$${api.total_cost.toFixed(4)}</div>
                        </div>
                      </div>
                    </div>
                  `).join('') || '<div style="text-align: center; color: #6b7280; padding: 40px;">No API usage data available</div>'}
                </div>
              </div>
              
              ${data.data?.api_errors?.length > 0 ? `
                <div class="card" style="margin-top: 20px;">
                  <div class="card-header">
                    <div class="card-title"><i class="fas fa-exclamation-triangle"></i> Recent API Errors</div>
                  </div>
                  <div style="max-height: 300px; overflow-y: auto;">
                    ${data.data.api_errors.map(error => `
                      <div style="display: flex; justify-content: space-between; padding: 12px 16px; border-bottom: 1px solid #e5e7eb;">
                        <div>
                          <div style="font-weight: 600; color: #1f2937;">${error.api_name}</div>
                          <div style="font-size: 14px; color: #6b7280;">${error.error}</div>
                        </div>
                        <span style="font-weight: 600; color: #ef4444;">${error.count}x</span>
                      </div>
                    `).join('')}
                  </div>
                </div>
              ` : ''}
              
              <div class="card" style="margin-top: 20px;">
                <div class="card-header">
                  <div class="card-title"><i class="fas fa-info-circle"></i> Supported APIs</div>
                </div>
                <div style="padding: 16px;">
                  <div class="supported-apis" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;">
                    <div class="api-info" style="text-align: center; padding: 16px; border: 1px solid #e5e7eb; border-radius: 6px;">
                      <i class="fas fa-gavel" style="font-size: 24px; color: #6366f1; margin-bottom: 8px;"></i>
                      <h4 style="margin: 0 0 4px 0;">LexML</h4>
                      <p style="margin: 0; font-size: 14px; color: #6b7280;">Legal document repository</p>
                    </div>
                    <div class="api-info" style="text-align: center; padding: 16px; border: 1px solid #e5e7eb; border-radius: 6px;">
                      <i class="fas fa-balance-scale" style="font-size: 24px; color: #10b981; margin-bottom: 8px;"></i>
                      <h4 style="margin: 0 0 4px 0;">JusBrasil</h4>
                      <p style="margin: 0; font-size: 14px; color: #6b7280;">Legal database integration</p>
                    </div>
                    <div class="api-info" style="text-align: center; padding: 16px; border: 1px solid #e5e7eb; border-radius: 6px;">
                      <i class="fas fa-university" style="font-size: 24px; color: #f59e0b; margin-bottom: 8px;"></i>
                      <h4 style="margin: 0 0 4px 0;">STF/STJ</h4>
                      <p style="margin: 0; font-size: 14px; color: #6b7280;">Supreme court decisions</p>
                    </div>
                  </div>
                </div>
              </div>
            `;
            
        } catch (error) {
            console.error('Error loading libraries content:', error);
            c.innerHTML = `
              <div class="card">
                <div class="card-header">
                  <div class="card-title"><i class="fas fa-exclamation-triangle"></i> Libraries Monitoring Error</div>
                </div>
                <div style="text-align: center; padding: 40px;">
                  <p>Failed to load API libraries data. Please try refreshing the page.</p>
                  <button onclick="dashboard.loadLibrariesContent()" class="btn btn-primary">
                    <i class="fas fa-refresh"></i> Retry
                  </button>
                </div>
              </div>
            `;
        }
    }

    async loadMonitoringContent() {
        const c = document.getElementById('monitoring-content');
        if (!c) return;
        const res = await fetch('/admin/api/monitoring/metrics');
        const m = await res.json();
        c.innerHTML = `
          <div class="toolbar" style="margin-bottom:12px;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;">
            <div class="controls" style="display:flex;align-items:center;gap:12px;">
              <label class="switch"><input id="monitoring-auto" type="checkbox" ${this.monitoring.autoRefresh?'checked':''} /><span class="slider"></span><span class="label">Auto-refresh</span></label>
              <select id="monitoring-interval" class="form-select" style="min-width:120px;">
                <option value="5000" ${this.monitoring.intervalMs===5000?'selected':''}>Every 5s</option>
                <option value="10000" ${this.monitoring.intervalMs===10000?'selected':''}>Every 10s</option>
                <option value="30000" ${this.monitoring.intervalMs===30000?'selected':''}>Every 30s</option>
              </select>
            </div>
          </div>
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-label">CPU Usage</div>
              <div id="cpu-usage" class="stat-value">${m.cpu?.usage}%</div>
              <div class="progress-bar"><div id="cpu-fill" class="progress-fill" style="width:${m.cpu?.usage||0}%"></div></div>
            </div>
            <div class="stat-card">
              <div class="stat-label">Memory Used</div>
              <div id="mem-usage" class="stat-value">${m.memory?.used}%</div>
              <div class="progress-bar"><div id="mem-fill" class="progress-fill" style="width:${m.memory?.used||0}%"></div></div>
            </div>
            <div class="stat-card">
              <div class="stat-label">Disk Used</div>
              <div id="disk-usage" class="stat-value">${m.disk?.used}%</div>
              <div class="progress-bar"><div id="disk-fill" class="progress-fill" style="width:${m.disk?.used||0}%"></div></div>
            </div>
          </div>
          <div class="card" style="margin-top:16px;">
            <div class="card-title"><i class="fas fa-server"></i> Services</div>
            <div id="services-chips" class="chips" style="margin-top:12px;">
              ${Object.entries(m.services||{}).map(([k,v])=>`<span class="chip ${v==='running'?'active':''}">${k}: ${v}</span>`).join('')}
            </div>
          </div>`;

        // Controls
        const autoEl = c.querySelector('#monitoring-auto');
        const intervalEl = c.querySelector('#monitoring-interval');
        autoEl?.addEventListener('change', () => {
            this.monitoring.autoRefresh = !!autoEl.checked;
            if (this.monitoring.autoRefresh) this.startMonitoringAutoRefresh(); else this.stopMonitoringAutoRefresh();
        });
        intervalEl?.addEventListener('change', () => {
            const ms = parseInt(intervalEl.value, 10) || 10000;
            this.monitoring.intervalMs = ms;
            if (this.monitoring.autoRefresh) {
                this.startMonitoringAutoRefresh();
            }
        });

        // Ensure current state
        if (this.monitoring.autoRefresh) this.startMonitoringAutoRefresh(); else this.stopMonitoringAutoRefresh();
    }

    updateMonitoringUI(m) {
        const c = document.getElementById('monitoring-content');
        if (!c) return;
        const cpu = m.cpu?.usage ?? 0;
        const mem = m.memory?.used ?? 0;
        const disk = m.disk?.used ?? 0;
        const cpuVal = c.querySelector('#cpu-usage');
        const cpuFill = c.querySelector('#cpu-fill');
        const memVal = c.querySelector('#mem-usage');
        const memFill = c.querySelector('#mem-fill');
        const diskVal = c.querySelector('#disk-usage');
        const diskFill = c.querySelector('#disk-fill');
        if (cpuVal) cpuVal.textContent = `${cpu}%`;
        if (cpuFill) cpuFill.style.width = `${cpu}%`;
        if (memVal) memVal.textContent = `${mem}%`;
        if (memFill) memFill.style.width = `${mem}%`;
        if (diskVal) diskVal.textContent = `${disk}%`;
        if (diskFill) diskFill.style.width = `${disk}%`;
        const chips = c.querySelector('#services-chips');
        if (chips && m.services) {
            chips.innerHTML = Object.entries(m.services).map(([k,v])=>`<span class="chip ${v==='running'?'active':''}">${k}: ${v}</span>`).join('');
        }
    }

    startMonitoringAutoRefresh() {
        this.stopMonitoringAutoRefresh();
        if (!this.monitoring.autoRefresh) return;
        this.monitoringInterval = setInterval(async () => {
            try {
                const res = await fetch('/admin/api/monitoring/metrics');
                const m = await res.json();
                this.updateMonitoringUI(m);
            } catch (e) {
                console.error('Monitoring auto-refresh error', e);
            }
        }, this.monitoring.intervalMs || 10000);
    }

    stopMonitoringAutoRefresh() {
        if (this.monitoringInterval) {
            clearInterval(this.monitoringInterval);
            this.monitoringInterval = null;
        }
    }

    async loadUsersContent() {
        const c = document.getElementById('users-content');
        if (!c) return;
        const res = await fetch('/admin/api/users');
        const data = await res.json();
        this.usersState.users = data.users || [];
        this.usersState.page = 1; this.usersState.selected.clear();
        c.innerHTML = `
          <div class="card">
            <div class="toolbar">
              <div class="controls">
                <input id="users-search" class="form-input" placeholder="Search users..." />
                <select id="users-role" class="form-select">
                  <option value="all">All Roles</option>
                  ${[...new Set((data.users||[]).map(u=>u.role))].map(r=>`<option value="${r}">${r}</option>`).join('')}
                </select>
              </div>
              <div class="controls">
                <button id="users-export" class="btn btn-secondary btn-sm"><i class="fas fa-file-export"></i> Export</button>
              </div>
            </div>
            <table class="data-table">
              <thead><tr>
                <th><input type="checkbox" id="users-select-all" class="checkbox"/></th>
                <th class="sortable" data-sort="name">Name</th>
                <th class="sortable" data-sort="email">Email</th>
                <th class="sortable" data-sort="role">Role</th>
                <th class="sortable" data-sort="status">Status</th>
                <th class="sortable" data-sort="lastLogin">Last Login</th>
              </tr></thead>
              <tbody id="users-tbody"></tbody>
            </table>
            <div class="toolbar"><div></div><div id="users-pagination" class="pagination"></div></div>
          </div>`;
        this.applyUsersFilters();
        // Bind events
        c.querySelector('#users-search').addEventListener('input', this.debounce((e)=>{ this.usersState.search = e.target.value.trim().toLowerCase(); this.usersState.page=1; this.applyUsersFilters(); }, 300));
        c.querySelector('#users-role').addEventListener('change', (e)=>{ this.usersState.role = e.target.value; this.usersState.page=1; this.applyUsersFilters(); });
        c.querySelector('#users-select-all').addEventListener('change', (e)=>{ const checked=e.target.checked; (c.querySelectorAll('.user-row input.checkbox')||[]).forEach(ch=>{ ch.checked=checked; this.usersState.selected[checked?'add':'delete'](parseInt(ch.dataset.id,10)); }); });
        c.querySelector('#users-export').addEventListener('click', async ()=>{ const r = await fetch('/admin/api/export/users'); const j = await r.json(); if (r.ok && j.downloadUrl) window.open(j.downloadUrl, '_blank'); else this.showNotification(j.error || 'Export failed', 'error'); });
        c.querySelectorAll('th.sortable').forEach(th => {
            th.style.cursor = 'pointer';
            th.addEventListener('click', ()=>{
                const k = th.getAttribute('data-sort');
                if (!k) return;
                if (this.usersState.sort.key === k) this.usersState.sort.dir = (this.usersState.sort.dir === 'asc' ? 'desc' : 'asc');
                else this.usersState.sort = { key: k, dir: 'asc' };
                this.usersState.page = 1;
                this.applyUsersFilters();
            });
        });
    }

    async loadLogsContent() {
        try {
            // The logs panel JS will handle the logs loading and display
            // This just triggers a custom event to notify the logs panel that the logs page is active
            const event = new CustomEvent('pageChanged', { 
                detail: { page: 'logs' }
            });
            document.dispatchEvent(event);
            
            // Update recent activity on the logs page
            const recentActivity = await adminApi.getRecentActivity();
            this.updateRecentActivity(recentActivity.activity || []);
        } catch (error) {
            console.error('Error loading logs content:', error);
        }
    }

    async loadSettingsContent() {
        const c = document.getElementById('settings-content');
        if (!c) return;
        const res = await fetch('/admin/api/settings');
        const s = await res.json();
        c.innerHTML = `
          <form id="settings-form" class="card">
            <div class="card-header"><div class="card-title"><i class="fas fa-cog"></i> Settings</div>
              <button type="submit" class="btn btn-primary btn-sm"><i class="fas fa-save"></i> Save</button>
            </div>
            <div class="stats-grid">
              <div>
                <h4 style="margin-bottom:8px">General</h4>
                <div class="form-group"><label class="form-label">System Name</label><input name="systemName" class="form-input" value="${s.general?.systemName||''}" /></div>
                <div class="form-group"><label class="form-label">Timezone</label><input name="timezone" class="form-input" value="${s.general?.timezone||''}" /></div>
              </div>
              <div>
                <h4 style="margin-bottom:8px">Security</h4>
                <label class="switch"><input id="twoFactorEnabled" type="checkbox" ${s.security?.twoFactorEnabled?'checked':''} /><span class="slider"></span><span class="label">Two-factor Authentication</span></label>
                <div class="form-group"><label class="form-label">Session Timeout (min)</label><input name="sessionTimeout" type="number" class="form-input" value="${s.security?.sessionTimeout||30}" /></div>
              </div>
              <div>
                <h4 style="margin-bottom:8px">Notifications</h4>
                <label class="switch"><input id="emailEnabled" type="checkbox" ${s.notifications?.emailEnabled?'checked':''} /><span class="slider"></span><span class="label">Email</span></label>
                <label class="switch"><input id="slackEnabled" type="checkbox" ${s.notifications?.slackEnabled?'checked':''} /><span class="slider"></span><span class="label">Slack</span></label>
                <div class="form-group"><label class="form-label">Webhook URL</label><input id="webhookUrl" class="form-input" value="${s.notifications?.webhookUrl||''}" /></div>
              </div>
              <div>
                <h4 style="margin-bottom:8px">Backup</h4>
                <label class="switch"><input id="autoBackup" type="checkbox" ${s.backup?.autoBackup?'checked':''} /><span class="slider"></span><span class="label">Auto Backup</span></label>
                <div class="form-group"><label class="form-label">Frequency</label><input id="backupFrequency" class="form-input" value="${s.backup?.backupFrequency||''}" /></div>
                <div class="form-group"><label class="form-label">Retention Days</label><input id="retentionDays" type="number" class="form-input" value="${s.backup?.retentionDays||30}" /></div>
              </div>
            </div>
          </form>`;
        c.querySelector('#settings-form').addEventListener('submit', async (e)=>{
            e.preventDefault();
            const payload = {
              general: { systemName: c.querySelector('input[name="systemName"]').value, timezone: c.querySelector('input[name="timezone"]').value },
              security: { twoFactorEnabled: c.querySelector('#twoFactorEnabled').checked, sessionTimeout: parseInt(c.querySelector('input[name="sessionTimeout"]').value,10)||30, passwordPolicy: 'strong' },
              notifications: { emailEnabled: c.querySelector('#emailEnabled').checked, slackEnabled: c.querySelector('#slackEnabled').checked, webhookUrl: c.querySelector('#webhookUrl').value },
              backup: { autoBackup: c.querySelector('#autoBackup').checked, backupFrequency: c.querySelector('#backupFrequency').value, retentionDays: parseInt(c.querySelector('#retentionDays').value,10)||30 }
            };
            const resp = await fetch('/admin/api/settings', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) });
            const out = await resp.json();
            if (resp.ok) this.showNotification(out.message || 'Settings updated', 'success'); else this.showNotification(out.error||'Failed to update settings','error');
        });
    }

    renderKbChips() {
        const chips = document.getElementById('kb-chips');
        if (!chips) return;
        chips.innerHTML = this.kbState.categories.map(cat=>`<span class="chip ${this.kbState.category===cat?'active':''}" data-cat="${cat}">${cat}</span>`).join('');
        chips.querySelectorAll('.chip').forEach(ch=> ch.addEventListener('click', ()=>{ this.kbState.category = ch.dataset.cat; this.kbState.page=1; this.renderKbChips(); this.applyKnowledgeFilters(); }));
    }

    applyKnowledgeFilters() {
        const term = this.kbState.search.trim().toLowerCase();
        const cat = this.kbState.category;
        let filtered = this.kbState.documents.filter(d =>
            (!term || (d.title||'').toLowerCase().includes(term) || (d.keywords||[]).join(' ').toLowerCase().includes(term)) &&
            (cat==='all' || d.category===cat)
        );
        // sort
        const { key, dir } = this.kbState.sort || { key:'title', dir:'asc' };
        filtered.sort((a,b)=>{
            let va, vb;
            if (key === 'keywords') { va = (a.keywords||[])[0] || ''; vb = (b.keywords||[])[0] || ''; }
            else { va = a[key]; vb = b[key]; }
            return this.compareValues(va, vb, dir);
        });
        this.kbState.filtered = filtered;
        this.renderKnowledgeTable();
        this.renderKbPagination();
    }

    renderKnowledgeTable() {
        const tbody = document.getElementById('kb-tbody');
        if (!tbody) return;
        const start = (this.kbState.page-1)*this.kbState.pageSize;
        const rows = this.kbState.filtered.slice(start, start+this.kbState.pageSize).map(doc=>`
            <tr class="kb-row">
              <td><input type="checkbox" class="checkbox kb-select" data-id="${doc.id}" ${this.kbState.selected.has(doc.id)?'checked':''} /></td>
              <td>${doc.title}</td>
              <td>${doc.category}</td>
              <td>${(doc.keywords||[]).slice(0,3).join(', ')}</td>
              <td>${doc.created||'-'}</td>
              <td>${doc.modified||'-'}</td>
              <td class="table-actions">
                <button class="btn btn-sm btn-primary kb-edit-btn" data-id="${doc.id}"><i class="fas fa-edit"></i></button>
                <button class="btn btn-sm btn-danger kb-delete-btn" data-id="${doc.id}"><i class="fas fa-trash"></i></button>
              </td>
            </tr>
        `).join('');
        tbody.innerHTML = rows || '<tr><td colspan="7" style="color:var(--text-secondary)">No documents</td></tr>';
        this.bindKnowledgeRowActions();
        this.updateKbBulkButton();
    }

    renderKbPagination() {
        const el = document.getElementById('kb-pagination'); if (!el) return;
        const totalPages = Math.max(1, Math.ceil(this.kbState.filtered.length / this.kbState.pageSize));
        const buttons = [];
        for (let i=1;i<=totalPages;i++) buttons.push(`<button class="page-btn ${i===this.kbState.page?'active':''}" data-p="${i}">${i}</button>`);
        el.innerHTML = buttons.join('');
        el.querySelectorAll('.page-btn').forEach(b=> b.addEventListener('click', ()=>{ this.kbState.page = parseInt(b.dataset.p,10); this.renderKnowledgeTable(); this.renderKbPagination(); }));
    }

    bindKnowledgeActions() {
        // Search (debounced)
        const kbSearchEl = document.getElementById('kb-search');
        kbSearchEl?.addEventListener('input', this.debounce((e)=>{ this.kbState.search = e.target.value; this.kbState.page=1; this.applyKnowledgeFilters(); }, 300));

        // Sorting
        document.querySelectorAll('th.sortable').forEach(th => {
            th.style.cursor = 'pointer';
            th.addEventListener('click', ()=>{
                const k = th.getAttribute('data-sort');
                if (!k) return;
                if (this.kbState.sort.key === k) this.kbState.sort.dir = (this.kbState.sort.dir === 'asc' ? 'desc' : 'asc');
                else this.kbState.sort = { key: k, dir: 'asc' };
                this.kbState.page = 1;
                this.applyKnowledgeFilters();
            });
        });

        // Select all (affects current table rows)
        document.getElementById('kb-select-all')?.addEventListener('change', (e)=>{
            const checked = e.target.checked;
            document.querySelectorAll('.kb-select').forEach(ch=>{ ch.checked = checked; const id = ch.getAttribute('data-id'); this.kbState.selected[checked?'add':'delete'](id); });
            this.updateKbBulkButton();
        });

        // Bulk delete
        document.getElementById('kb-delete-selected')?.addEventListener('click', async ()=>{
            if (!this.kbState.selected.size) return;
            const ok = await this.confirmModal(`Delete ${this.kbState.selected.size} documents?`, { confirmText: 'Delete' });
            if (!ok) return;
            for (const id of Array.from(this.kbState.selected)) {
                try { await fetch(`/admin/api/knowledge-base/${id}`, { method:'DELETE' }); } catch {}
            }
            this.showNotification('Selected documents deleted', 'success');
            await this.loadKnowledgeContent();
        });

        // Export
        document.getElementById('kb-export')?.addEventListener('click', async ()=>{
            const res = await fetch('/admin/api/export/knowledge');
            const data = await res.json();
            if (res.ok && data.downloadUrl) window.open(data.downloadUrl, '_blank'); else this.showNotification(data.error || 'Export failed', 'error');
        });
    }

    // Bind handlers for dynamic table rows (called on each table render)
    bindKnowledgeRowActions() {
        // Row selection
        document.querySelectorAll('.kb-select').forEach(chk=>{
            chk.addEventListener('change', (e)=>{
                const id = e.target.getAttribute('data-id');
                if (e.target.checked) this.kbState.selected.add(id); else this.kbState.selected.delete(id);
                this.updateKbBulkButton();
            });
        });

        // Edit buttons
        document.querySelectorAll('.kb-edit-btn').forEach(btn => {
            btn.addEventListener('click', async () => {
                const id = btn.getAttribute('data-id');
                if (!id) return;
                try {
                    const res = await fetch(`/admin/api/knowledge-base/${id}`);
                    const doc = await res.json();
                    const newTitle = await this.promptModal('Edit title', doc?.title || '');
                    if (newTitle === null) return; // canceled
                    const payload = { ...doc, title: newTitle };
                    await fetch(`/admin/api/knowledge-base/${id}`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });
                    this.showNotification('Document updated', 'success');
                    await this.loadKnowledgeContent();
                } catch (err) {
                    console.error(err);
                    this.showNotification('Failed to update document', 'error');
                }
            });
        });

        // Delete buttons
        document.querySelectorAll('.kb-delete-btn').forEach(btn => {
            btn.addEventListener('click', async () => {
                const id = btn.getAttribute('data-id');
                if (!id) return;
                const confirmDel = await this.confirmModal('Delete this document?', { confirmText: 'Delete' });
                if (!confirmDel) return;
                try {
                    await fetch(`/admin/api/knowledge-base/${id}`, { method: 'DELETE' });
                    this.showNotification('Document deleted', 'success');
                    await this.loadKnowledgeContent();
                } catch (err) {
                    console.error(err);
                    this.showNotification('Failed to delete document', 'error');
                }
            });
        });
    }

    updateKbBulkButton() {
        const btn = document.getElementById('kb-delete-selected');
        if (btn) btn.disabled = this.kbState.selected.size === 0;
    }

    async uploadKnowledgeDocument(file) {
        const form = new FormData();
        form.append('file', file);
        try {
            this.showNotification('Uploading document...', 'info');
            const res = await fetch('/admin/api/knowledge-base/upload', {
                method: 'POST',
                body: form
            });
            const data = await res.json();
            if (res.ok && data?.success) {
                this.showNotification('Document uploaded', 'success');
                await this.loadKnowledgeContent();
            } else {
                throw new Error(data?.error || 'Upload failed');
            }
        } catch (err) {
            console.error(err);
            this.showNotification('Upload failed', 'error');
        }
    }

    async reindexKnowledgeBase() {
        try {
            const res = await fetch('/admin/api/knowledge-base/reindex', { method: 'POST' });
            const data = await res.json();
            if (res.ok && data?.success) this.showNotification('Reindexing started', 'success');
            else this.showNotification('Reindex request sent', 'info');
        } catch (err) {
            console.error(err);
            this.showNotification('Failed to start reindex', 'error');
        }
    }

    renderLogs(entries) {
        return entries.map(log => `
            <div class="feed-item">
                <div class="feed-content">
                    <div class="feed-time">${log.timestamp}</div>
                    <div>${log.level}: ${log.message}</div>
                </div>
            </div>
        `).join('');
    }

    applyLogsFilters() {
        const term = this.logsState.search;
        const level = this.logsState.level;
        const all = this.logsState.entries;
        let filtered = all.filter(l => (!term || (l.message||'').toLowerCase().includes(term)) && (level==='all' || l.level===level));
        const { key, dir } = this.logsState.sort || { key: 'timestamp', dir: 'desc' };
        filtered.sort((a,b)=> this.compareValues(a[key], b[key], dir));
        this.logsState.filtered = filtered;
        const tbody = document.getElementById('logs-tbody');
        const start = (this.logsState.page-1)*this.logsState.pageSize;
        const rows = filtered.slice(start, start+this.logsState.pageSize).map(l=>`<tr><td>${l.timestamp}</td><td>${l.level}</td><td>${l.message}</td></tr>`).join('');
        tbody.innerHTML = rows || '<tr><td colspan="3" style="color:var(--text-secondary)">No logs</td></tr>';
        const pag = document.getElementById('logs-pagination');
        const pages = Math.max(1, Math.ceil(filtered.length/this.logsState.pageSize));
        pag.innerHTML = Array.from({length: pages}, (_,i)=>`<button class="page-btn ${i+1===this.logsState.page?'active':''}" data-p="${i+1}">${i+1}</button>`).join('');
        pag.querySelectorAll('.page-btn').forEach(b=> b.addEventListener('click', ()=>{ this.logsState.page = parseInt(b.dataset.p,10); this.applyLogsFilters(); }));
    }

    applyUsersFilters() {
        const term = this.usersState.search;
        const role = this.usersState.role;
        let filtered = this.usersState.users.filter(u => (!term || (u.name+u.email).toLowerCase().includes(term)) && (role==='all' || u.role===role));
        const { key, dir } = this.usersState.sort || { key: 'name', dir: 'asc' };
        filtered.sort((a,b)=> this.compareValues(a[key], b[key], dir));
        this.usersState.filtered = filtered;
        const tbody = document.getElementById('users-tbody'); if (!tbody) return;
        const start = (this.usersState.page-1)*this.usersState.pageSize;
        const rows = filtered.slice(start, start+this.usersState.pageSize).map(u=>`
            <tr class="user-row">
              <td><input type="checkbox" class="checkbox" data-id="${u.id}" /></td>
              <td>${u.name}</td><td>${u.email}</td><td>${u.role}</td><td>${u.status}</td><td>${u.lastLogin}</td>
            </tr>`).join('');
        tbody.innerHTML = rows || '<tr><td colspan="6" style="color:var(--text-secondary)">No users</td></tr>';
        const pag = document.getElementById('users-pagination');
        const pages = Math.max(1, Math.ceil(filtered.length/this.usersState.pageSize));
        pag.innerHTML = Array.from({length: pages}, (_,i)=>`<button class="page-btn ${i+1===this.usersState.page?'active':''}" data-p="${i+1}">${i+1}</button>`).join('');
        pag.querySelectorAll('.page-btn').forEach(b=> b.addEventListener('click', ()=>{ this.usersState.page = parseInt(b.dataset.p,10); this.applyUsersFilters(); }));
    }
    
    async loadOpenAIContent() {
        try {
            const c = document.getElementById('openai-content');
            if (!c) return;
            
            // Show loading state
            c.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Loading OpenAI dashboard...</div>';
            
            // Fetch OpenAI configuration and stats
            const res = await fetch('/admin-v2/api/openai/status');
            const data = await res.json();
            
            if (!res.ok) throw new Error(data.error || 'Failed to load OpenAI dashboard');
            
            // Create dashboard content
            c.innerHTML = `
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-icon bg-primary">
                            <i class="fas fa-key"></i>
                        </div>
                        <div class="stat-content">
                            <div class="stat-label">API Status</div>
                            <div class="stat-value">${data.status ? '<span class="badge success">Active</span>' : '<span class="badge danger">Inactive</span>'}</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon bg-success">
                            <i class="fas fa-terminal"></i>
                        </div>
                        <div class="stat-content">
                            <div class="stat-label">Model</div>
                            <div class="stat-value">${data.model || 'Unknown'}</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon bg-info">
                            <i class="fas fa-coins"></i>
                        </div>
                        <div class="stat-content">
                            <div class="stat-label">Tokens Used</div>
                            <div class="stat-value">${data.totalTokens?.toLocaleString() || '0'}</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon bg-warning">
                            <i class="fas fa-tachometer-alt"></i>
                        </div>
                        <div class="stat-content">
                            <div class="stat-label">Avg Response Time</div>
                            <div class="stat-value">${data.avgResponseTime || '0ms'}</div>
                        </div>
                    </div>
                </div>
                
                <div class="card mt-4">
                    <div class="card-header">
                        <div class="card-title"><i class="fas fa-cog"></i> API Configuration</div>
                    </div>
                    <div class="card-body">
                        <form id="openai-config-form">
                            <div class="form-group">
                                <label>API Key</label>
                                <div class="input-group">
                                    <input type="password" id="openai-api-key" class="form-input" value="${data.hasApiKey ? '••••••••••••••••••••••••••' : ''}" placeholder="Enter OpenAI API Key">
                                    <button type="button" class="btn btn-secondary" id="toggle-api-key">
                                        <i class="fas fa-eye"></i>
                                    </button>
                                </div>
                                <small class="form-text">Your API key is encrypted and stored securely.</small>
                            </div>
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save"></i> Save Configuration
                            </button>
                        </form>
                    </div>
                </div>
                
                <div class="card mt-4">
                    <div class="card-header">
                        <div class="card-title"><i class="fas fa-chart-bar"></i> Usage Stats</div>
                    </div>
                    <div class="card-body">
                        <canvas id="openai-usage-chart" style="width:100%; height:300px;"></canvas>
                    </div>
                </div>
                
                <div class="card mt-4">
                    <div class="card-header">
                        <div class="card-title"><i class="fas fa-exclamation-triangle"></i> Recent Errors</div>
                    </div>
                    <div class="card-body">
                        <div class="table-container">
                            <table class="table">
                                <thead>
                                    <tr>
                                        <th>Time</th>
                                        <th>Error</th>
                                        <th>Details</th>
                                    </tr>
                                </thead>
                                <tbody id="openai-errors-tbody">
                                    ${data.errors && data.errors.length > 0 ? 
                                        data.errors.map(err => `<tr>
                                            <td>${err.timestamp || 'Unknown'}</td>
                                            <td>${err.error || 'Unknown error'}</td>
                                            <td>${err.details || 'No details'}</td>
                                        </tr>`).join('') : 
                                        '<tr><td colspan="3" class="text-center">No recent errors</td></tr>'
                                    }
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            `;
            
            // Set up event handlers
            const toggleBtn = document.getElementById('toggle-api-key');
            const apiKeyInput = document.getElementById('openai-api-key');
            if (toggleBtn && apiKeyInput) {
                toggleBtn.addEventListener('click', () => {
                    const type = apiKeyInput.getAttribute('type');
                    apiKeyInput.setAttribute('type', type === 'password' ? 'text' : 'password');
                    toggleBtn.innerHTML = `<i class="fas fa-${type === 'password' ? 'eye-slash' : 'eye'}"></i>`;
                });
            }
            
            const form = document.getElementById('openai-config-form');
            if (form) {
                form.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const apiKey = document.getElementById('openai-api-key').value;
                    if (!apiKey) {
                        this.showNotification('API key is required', 'error');
                        return;
                    }
                    
                    try {
                        this.showNotification('Updating API configuration...', 'info');
                        const res = await fetch('/admin-v2/api/openai/config', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ api_key: apiKey })
                        });
                        
                        const result = await res.json();
                        if (res.ok) {
                            this.showNotification(result.message || 'API configuration updated', 'success');
                            setTimeout(() => this.loadOpenAIContent(), 1000);
                        } else {
                            this.showNotification(result.error || 'Failed to update configuration', 'error');
                        }
                    } catch (error) {
                        console.error('Error updating OpenAI config:', error);
                        this.showNotification('An error occurred while updating configuration', 'error');
                    }
                });
            }
            
            // Initialize charts if data is available
            if (data.usageHistory && window.Chart) {
                const ctx = document.getElementById('openai-usage-chart')?.getContext('2d');
                if (ctx) {
                    new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: data.usageHistory.map(entry => entry.date),
                            datasets: [{
                                label: 'Tokens Used',
                                data: data.usageHistory.map(entry => entry.tokens),
                                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                                borderColor: 'rgba(54, 162, 235, 1)',
                                borderWidth: 1,
                                tension: 0.4
                            }]
                        },
                        options: {
                            scales: {
                                y: { beginAtZero: true }
                            },
                            responsive: true,
                            maintainAspectRatio: false
                        }
                    });
                }
            }
        } catch (error) {
            console.error('Error loading OpenAI dashboard:', error);
            const c = document.getElementById('openai-content');
            if (c) {
                c.innerHTML = `
                <div class="error-state">
                    <div class="error-icon">
                        <i class="fas fa-exclamation-circle"></i>
                    </div>
                    <div class="error-message">
                        <h3>Failed to load OpenAI dashboard</h3>
                        <p>${error.message || 'An unknown error occurred'}</p>
                    </div>
                    <button onclick="dashboard.loadOpenAIContent()" class="btn btn-primary">
                        <i class="fas fa-refresh"></i> Retry
                    </button>
                </div>`;
            }
        }
    }
    
    async loadLexMLContent() {
        try {
            const c = document.getElementById('lextml-content');
            if (!c) return;
            
            // Show loading state
            c.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Loading LexML API data...</div>';
            
            // Fetch LexML API data
            const res = await fetch('/admin-v2/api/lextml/status');
            const data = await res.json();
            
            if (!res.ok) throw new Error(data.error || 'Failed to load LexML API data');
            
            // Create dashboard content
            c.innerHTML = `
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-icon bg-primary">
                            <i class="fas fa-balance-scale"></i>
                        </div>
                        <div class="stat-content">
                            <div class="stat-label">API Status</div>
                            <div class="stat-value">${data.status ? '<span class="badge success">Available</span>' : '<span class="badge danger">Unavailable</span>'}</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon bg-success">
                            <i class="fas fa-search"></i>
                        </div>
                        <div class="stat-content">
                            <div class="stat-label">Total Queries</div>
                            <div class="stat-value">${data.totalQueries?.toLocaleString() || '0'}</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon bg-info">
                            <i class="fas fa-database"></i>
                        </div>
                        <div class="stat-content">
                            <div class="stat-label">Available Documents</div>
                            <div class="stat-value">${data.documentCount?.toLocaleString() || '0'}</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon bg-warning">
                            <i class="fas fa-clock"></i>
                        </div>
                        <div class="stat-content">
                            <div class="stat-label">Avg Response Time</div>
                            <div class="stat-value">${data.avgResponseTime || '0ms'}</div>
                        </div>
                    </div>
                </div>
                
                <div class="card mt-4">
                    <div class="card-header">
                        <div class="card-title"><i class="fas fa-search"></i> LexML Search</div>
                    </div>
                    <div class="card-body">
                        <form id="lextml-search-form">
                            <div class="form-group">
                                <label>Search Legal Documents</label>
                                <div class="input-group">
                                    <input type="text" id="lextml-search-input" class="form-input" placeholder="Enter search query...">
                                    <button type="submit" class="btn btn-primary">
                                        <i class="fas fa-search"></i> Search
                                    </button>
                                </div>
                                <small class="form-text">Search for legal documents, provisions, jurisprudence, etc.</small>
                            </div>
                        </form>
                        <div id="lextml-search-results" class="mt-4" style="display:none;">
                            <h4>Search Results</h4>
                            <div class="table-container">
                                <table class="table">
                                    <thead>
                                        <tr>
                                            <th>Document</th>
                                            <th>Type</th>
                                            <th>Date</th>
                                            <th>Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody id="lextml-results-tbody">
                                        <!-- Results will be populated here -->
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="card mt-4">
                    <div class="card-header">
                        <div class="card-title"><i class="fas fa-plus-circle"></i> Add Document to LexML</div>
                    </div>
                    <div class="card-body">
                        <form id="lextml-add-form">
                            <div class="form-group">
                                <label>Document Title</label>
                                <input type="text" id="lextml-doc-title" class="form-input" placeholder="Enter document title">
                            </div>
                            <div class="form-group">
                                <label>Document Type</label>
                                <select id="lextml-doc-type" class="form-select">
                                    <option value="">Select document type</option>
                                    <option value="law">Law</option>
                                    <option value="decree">Decree</option>
                                    <option value="resolution">Resolution</option>
                                    <option value="jurisprudence">Jurisprudence</option>
                                    <option value="other">Other</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Document Content</label>
                                <textarea id="lextml-doc-content" class="form-textarea" rows="6" placeholder="Enter document content"></textarea>
                            </div>
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save"></i> Add Document
                            </button>
                        </form>
                    </div>
                </div>
            `;
            
            // Set up event handlers for search form
            const searchForm = document.getElementById('lextml-search-form');
            if (searchForm) {
                searchForm.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const query = document.getElementById('lextml-search-input').value;
                    if (!query) {
                        this.showNotification('Please enter a search query', 'warning');
                        return;
                    }
                    
                    try {
                        this.showNotification('Searching...', 'info');
                        const res = await fetch('/admin-v2/api/lextml/search', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ query })
                        });
                        
                        const results = await res.json();
                        const resultsContainer = document.getElementById('lextml-search-results');
                        const tbody = document.getElementById('lextml-results-tbody');
                        
                        if (resultsContainer && tbody) {
                            resultsContainer.style.display = 'block';
                            
                            if (results.documents && results.documents.length > 0) {
                                tbody.innerHTML = results.documents.map(doc => `
                                    <tr>
                                        <td>${doc.title || 'Untitled'}</td>
                                        <td>${doc.type || 'Unknown'}</td>
                                        <td>${doc.date || '-'}</td>
                                        <td>
                                            <button class="btn btn-sm btn-primary" onclick="dashboard.viewDocument('${doc.id}')"><i class="fas fa-eye"></i></button>
                                        </td>
                                    </tr>
                                `).join('');
                            } else {
                                tbody.innerHTML = '<tr><td colspan="4" class="text-center">No documents found</td></tr>';
                            }
                        }
                    } catch (error) {
                        console.error('Error searching LexML:', error);
                        this.showNotification('An error occurred during search', 'error');
                    }
                });
            }
            
            // Set up event handlers for add form
            const addForm = document.getElementById('lextml-add-form');
            if (addForm) {
                addForm.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const title = document.getElementById('lextml-doc-title').value;
                    const type = document.getElementById('lextml-doc-type').value;
                    const content = document.getElementById('lextml-doc-content').value;
                    
                    if (!title || !type || !content) {
                        this.showNotification('All fields are required', 'warning');
                        return;
                    }
                    
                    try {
                        this.showNotification('Adding document...', 'info');
                        const res = await fetch('/admin-v2/api/lextml/add', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ title, type, content })
                        });
                        
                        const result = await res.json();
                        if (res.ok) {
                            this.showNotification(result.message || 'Document added successfully', 'success');
                            addForm.reset();
                        } else {
                            this.showNotification(result.error || 'Failed to add document', 'error');
                        }
                    } catch (error) {
                        console.error('Error adding document:', error);
                        this.showNotification('An error occurred while adding document', 'error');
                    }
                });
            }
        } catch (error) {
            console.error('Error loading LexML API content:', error);
            const c = document.getElementById('lextml-content');
            if (c) {
                c.innerHTML = `
                <div class="error-state">
                    <div class="error-icon">
                        <i class="fas fa-exclamation-circle"></i>
                    </div>
                    <div class="error-message">
                        <h3>Failed to load LexML API data</h3>
                        <p>${error.message || 'An unknown error occurred'}</p>
                    </div>
                    <button onclick="dashboard.loadLexMLContent()" class="btn btn-primary">
                        <i class="fas fa-refresh"></i> Retry
                    </button>
                </div>`;
            }
        }
    }
    
    viewDocument(docId) {
        // This is a stub for viewing LexML documents
        // Implement as needed based on backend capabilities
        alert(`Viewing document with ID: ${docId}`);
        // In a real implementation, you would fetch the document and show in a modal
    }
}

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new AdminDashboard();
});
