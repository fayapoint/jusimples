// JuSimples Admin Logs Panel
// Handles displaying search and ask logs in the admin panel

class LogsPanel {
    constructor() {
        this.searchLogsPage = 1;
        this.askLogsPage = 1;
        this.logsPerPage = 10;
        this.searchLogs = [];
        this.askLogs = [];
        this.searchLogsTotal = 0;
        this.askLogsTotal = 0;
        
        // Filters
        this.searchFilter = "";
        this.searchStatus = "all";
        this.askFilter = "";
        this.askStatus = "all";
        
        // Initialize the panel
        this.init();
    }
    
    init() {
        // Set up tab switching
        document.querySelectorAll('.logs-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                e.preventDefault();
                this.switchTab(tab.dataset.tab);
            });
        });
        
        // Set up pagination
        document.getElementById('search-logs-prev')?.addEventListener('click', () => this.changePage('search', -1));
        document.getElementById('search-logs-next')?.addEventListener('click', () => this.changePage('search', 1));
        document.getElementById('ask-logs-prev')?.addEventListener('click', () => this.changePage('ask', -1));
        document.getElementById('ask-logs-next')?.addEventListener('click', () => this.changePage('ask', 1));
        
        // Set up filters for search logs
        const searchFilterInput = document.querySelector('#search-logs-content .filter-group input');
        if (searchFilterInput) {
            searchFilterInput.addEventListener('input', this.debounce(() => {
                this.searchFilter = searchFilterInput.value.trim();
                this.searchLogsPage = 1;
                this.loadSearchLogs();
            }, 300));
        }
        
        const searchStatusSelect = document.querySelector('#search-logs-content .filter-group select');
        if (searchStatusSelect) {
            searchStatusSelect.addEventListener('change', () => {
                this.searchStatus = searchStatusSelect.value;
                this.searchLogsPage = 1;
                this.loadSearchLogs();
            });
        }
        
        // Set up filters for ask logs
        const askFilterInput = document.querySelector('#ask-logs-content .filter-group input');
        if (askFilterInput) {
            askFilterInput.addEventListener('input', this.debounce(() => {
                this.askFilter = askFilterInput.value.trim();
                this.askLogsPage = 1;
                this.loadAskLogs();
            }, 300));
        }
        
        const askStatusSelect = document.querySelector('#ask-logs-content .filter-group select');
        if (askStatusSelect) {
            askStatusSelect.addEventListener('change', () => {
                this.askStatus = askStatusSelect.value;
                this.askLogsPage = 1;
                this.loadAskLogs();
            });
        }
        
        // Load logs when the logs page is shown
        document.addEventListener('pageChanged', (e) => {
            if (e.detail.page === 'logs') {
                this.loadAllLogs();
            }
        });
    }
    
    switchTab(tabName) {
        // Hide all content tabs
        document.querySelectorAll('.logs-content-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        
        // Deactivate all tabs
        document.querySelectorAll('.logs-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        
        // Show the selected content tab
        document.getElementById(`${tabName}-logs-content`).classList.add('active');
        
        // Activate the selected tab
        document.querySelector(`.logs-tab[data-tab="${tabName}"]`).classList.add('active');
    }
    
    async loadAllLogs() {
        await Promise.all([
            this.loadSearchLogs(),
            this.loadAskLogs()
        ]);
    }
    
    async loadSearchLogs() {
        try {
            const response = await adminApi.getSearchLogs(
                this.searchLogsPage, 
                this.logsPerPage, 
                this.searchFilter, 
                this.searchStatus
            );
            this.searchLogs = response.logs || [];
            this.searchLogsTotal = response.total || 0;
            this.renderSearchLogs();
            this.updateSearchPagination();
        } catch (error) {
            console.error("Error loading search logs:", error);
            document.getElementById('search-logs-container').innerHTML = `
                <div class="alert alert-danger">Error loading search logs: ${error.message}</div>
            `;
        }
    }
    
    async loadAskLogs() {
        try {
            const response = await adminApi.getAskLogs(
                this.askLogsPage, 
                this.logsPerPage,
                this.askFilter,
                this.askStatus
            );
            this.askLogs = response.logs || [];
            this.askLogsTotal = response.total || 0;
            this.renderAskLogs();
            this.updateAskPagination();
        } catch (error) {
            console.error("Error loading ask logs:", error);
            document.getElementById('ask-logs-container').innerHTML = `
                <div class="alert alert-danger">Error loading ask logs: ${error.message}</div>
            `;
        }
    }
    
    renderSearchLogs() {
        const container = document.getElementById('search-logs-container');
        if (!container) return;
        
        if (this.searchLogs.length === 0) {
            container.innerHTML = '<div class="empty-state">No search logs found</div>';
            return;
        }
        
        let html = `
            <table class="logs-table">
                <thead>
                    <tr>
                        <th>Timestamp</th>
                        <th>Query</th>
                        <th>Results</th>
                        <th>Success</th>
                        <th>Duration (ms)</th>
                        <th>Tokens</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        this.searchLogs.forEach(log => {
            const timestamp = new Date(log.created_at).toLocaleString();
            const success = log.success ? '<span class="badge success">Yes</span>' : '<span class="badge error">No</span>';
            
            html += `
                <tr>
                    <td>${timestamp}</td>
                    <td>${log.query || ''}</td>
                    <td>${log.total || 0}</td>
                    <td>${success}</td>
                    <td>${log.duration_ms || 0}</td>
                    <td>${log.tokens || 0}</td>
                </tr>
            `;
        });
        
        html += `
                </tbody>
            </table>
        `;
        
        container.innerHTML = html;
    }
    
    renderAskLogs() {
        const container = document.getElementById('ask-logs-container');
        if (!container) return;
        
        if (this.askLogs.length === 0) {
            container.innerHTML = '<div class="empty-state">No ask logs found</div>';
            return;
        }
        
        let html = `
            <table class="logs-table">
                <thead>
                    <tr>
                        <th>Timestamp</th>
                        <th>Question</th>
                        <th>Sources</th>
                        <th>Success</th>
                        <th>Duration (ms)</th>
                        <th>Tokens</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        this.askLogs.forEach(log => {
            const timestamp = new Date(log.created_at).toLocaleString();
            const success = log.success ? '<span class="badge success">Yes</span>' : '<span class="badge error">No</span>';
            
            html += `
                <tr>
                    <td>${timestamp}</td>
                    <td>${log.question || ''}</td>
                    <td>${log.total_sources || 0}</td>
                    <td>${success}</td>
                    <td>${log.duration_ms || 0}</td>
                    <td>${log.tokens_total || 0}</td>
                </tr>
            `;
        });
        
        html += `
                </tbody>
            </table>
        `;
        
        container.innerHTML = html;
    }
    
    updateSearchPagination() {
        const totalPages = Math.ceil(this.searchLogsTotal / this.logsPerPage);
        document.getElementById('search-logs-page-indicator').textContent = `Page ${this.searchLogsPage} of ${totalPages}`;
        
        // Disable previous button on first page
        const prevButton = document.getElementById('search-logs-prev');
        if (prevButton) {
            prevButton.disabled = this.searchLogsPage <= 1;
        }
        
        // Disable next button on last page
        const nextButton = document.getElementById('search-logs-next');
        if (nextButton) {
            nextButton.disabled = this.searchLogsPage >= totalPages;
        }
    }
    
    updateAskPagination() {
        const totalPages = Math.ceil(this.askLogsTotal / this.logsPerPage);
        document.getElementById('ask-logs-page-indicator').textContent = `Page ${this.askLogsPage} of ${totalPages}`;
        
        // Disable previous button on first page
        const prevButton = document.getElementById('ask-logs-prev');
        if (prevButton) {
            prevButton.disabled = this.askLogsPage <= 1;
        }
        
        // Disable next button on last page
        const nextButton = document.getElementById('ask-logs-next');
        if (nextButton) {
            nextButton.disabled = this.askLogsPage >= totalPages;
        }
    }
    
    changePage(logType, delta) {
        if (logType === 'search') {
            const newPage = this.searchLogsPage + delta;
            if (newPage > 0) {
                this.searchLogsPage = newPage;
                this.loadSearchLogs();
            }
        } else if (logType === 'ask') {
            const newPage = this.askLogsPage + delta;
            if (newPage > 0) {
                this.askLogsPage = newPage;
                this.loadAskLogs();
            }
        }
    }
    
    // Debounce function to limit how often a function is called
    debounce(func, wait) {
        let timeout;
        return function() {
            const context = this;
            const args = arguments;
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                func.apply(context, args);
            }, wait);
        };
    }
}

// Initialize logs panel when the document is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.logsPanel = new LogsPanel();
});
