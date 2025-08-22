/**
 * OpenAI Dashboard JavaScript
 * Handles data loading, visualization, and interaction for the OpenAI API Dashboard
 */

class OpenAIDashboard {
    constructor() {
        this.charts = {};
        this.data = {
            tokenUsage: {},
            requests: {},
            models: {},
            errors: []
        };
        this.init();
    }

    init() {
        // Initialize dashboard when DOM is loaded
        document.addEventListener('DOMContentLoaded', () => {
            this.setupEventListeners();
            this.loadAllData();
            
            // Set up auto-refresh every 5 minutes
            setInterval(() => this.loadAllData(), 5 * 60 * 1000);
        });
    }

    setupEventListeners() {
        // Mobile menu toggle
        const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
        if (mobileMenuToggle) {
            mobileMenuToggle.addEventListener('click', () => {
                document.getElementById('sidebar').classList.toggle('active');
            });
        }

        // Test connection button
        const testConnectionBtn = document.getElementById('test-connection-btn');
        if (testConnectionBtn) {
            testConnectionBtn.addEventListener('click', () => this.testApiConnection());
        }

        // Refresh button
        const refreshBtn = document.getElementById('refresh-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.loadAllData());
        }

        // Fullscreen button
        const fullscreenBtn = document.getElementById('fullscreen-btn');
        if (fullscreenBtn) {
            fullscreenBtn.addEventListener('click', () => this.toggleFullscreen());
        }

        // View all logs button
        const viewAllLogsBtn = document.getElementById('view-all-logs-btn');
        if (viewAllLogsBtn) {
            viewAllLogsBtn.addEventListener('click', () => {
                window.location.href = '/admin/logs';
            });
        }

        // API Calls tabs
        document.querySelectorAll('.api-calls-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                // Remove active class from all tabs
                document.querySelectorAll('.api-calls-tab').forEach(t => t.classList.remove('active'));
                
                // Add active class to clicked tab
                e.target.classList.add('active');
                
                // Hide all content tabs
                document.querySelectorAll('.api-calls-content').forEach(content => {
                    content.classList.remove('active');
                });
                
                // Show the corresponding content tab
                const tabName = e.target.getAttribute('data-tab');
                document.getElementById(`${tabName}-calls-content`).classList.add('active');
            });
        });
    }

    loadAllData() {
        this.loadApiStatus();
        this.loadTokenUsage();
        this.loadRequestStats();
        this.loadModelUsage();
        this.loadRecentErrors();
        this.loadRecentApiCalls();
    }

    testApiConnection() {
        const statusCard = document.getElementById('openaiStatusCard');
        const statusIndicator = document.getElementById('api-status-indicator');
        const detailedStatus = document.getElementById('detailed-status');
        
        statusCard.classList.add('loading');
        statusIndicator.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Testing...';
        
        fetch('/admin/api/test-openai-connection')
            .then(response => response.json())
            .then(data => {
                statusCard.classList.remove('loading');
                
                if (data.success) {
                    statusIndicator.className = 'api-status online';
                    statusIndicator.innerHTML = '<i class="fas fa-circle"></i> Connected';
                    detailedStatus.textContent = 'Operational';
                    detailedStatus.className = 'text-success';
                    
                    // Update connection details
                    document.getElementById('api-latency').textContent = `${data.latency}ms`;
                    document.getElementById('api-last-verified').textContent = new Date().toLocaleTimeString();
                    
                    // Show success message
                    this.showNotification('Connection test successful!', 'success');
                } else {
                    statusIndicator.className = 'api-status offline';
                    statusIndicator.innerHTML = '<i class="fas fa-circle"></i> Disconnected';
                    detailedStatus.textContent = 'Error: ' + data.message;
                    detailedStatus.className = 'text-danger';
                    
                    // Show error message
                    this.showNotification('Connection test failed: ' + data.message, 'error');
                }
                
                // Update API key info
                document.getElementById('api-key-masked').textContent = data.api_key_masked || 'sk-***************';
                document.getElementById('api-current-model').textContent = data.model || 'Unknown';
                document.getElementById('api-client-version').textContent = data.version || 'Unknown';
            })
            .catch(error => {
                console.error('Error testing API connection:', error);
                statusCard.classList.remove('loading');
                statusIndicator.className = 'api-status offline';
                statusIndicator.innerHTML = '<i class="fas fa-circle"></i> Error';
                detailedStatus.textContent = 'Connection Error';
                detailedStatus.className = 'text-danger';
                
                this.showNotification('Failed to test connection. Please try again later.', 'error');
            });
    }

    loadApiStatus() {
        fetch('/admin/api/openai-status')
            .then(response => response.json())
            .then(data => {
                const statusIndicator = document.getElementById('api-status-indicator');
                const detailedStatus = document.getElementById('detailed-status');
                
                if (data.initialized) {
                    statusIndicator.className = 'api-status online';
                    statusIndicator.innerHTML = '<i class="fas fa-circle"></i> Connected';
                    detailedStatus.textContent = 'Operational';
                    detailedStatus.className = 'text-success';
                } else {
                    statusIndicator.className = 'api-status offline';
                    statusIndicator.innerHTML = '<i class="fas fa-circle"></i> Disconnected';
                    detailedStatus.textContent = 'Error: ' + data.error;
                    detailedStatus.className = 'text-danger';
                }
                
                // Update API key info
                document.getElementById('api-key-masked').textContent = data.api_key_masked || 'sk-***************';
                document.getElementById('api-current-model').textContent = data.model || 'Unknown';
                document.getElementById('api-client-version').textContent = data.version || 'Unknown';
                document.getElementById('api-last-verified').textContent = data.last_verified || 'Unknown';
                document.getElementById('api-latency').textContent = data.latency ? `${data.latency}ms` : 'Unknown';
            })
            .catch(error => {
                console.error('Error loading API status:', error);
            });
    }

    loadTokenUsage() {
        fetch('/admin/api/token-usage')
            .then(response => response.json())
            .then(data => {
                this.data.tokenUsage = data;
                
                // Update metrics
                document.getElementById('total-tokens').textContent = this.formatNumber(data.total_tokens || 0);
                document.getElementById('prompt-tokens').textContent = this.formatNumber(data.prompt_tokens || 0);
                document.getElementById('completion-tokens').textContent = this.formatNumber(data.completion_tokens || 0);
                
                // Update progress bar
                const usagePercentage = data.percentage || 0;
                const tokenProgress = document.getElementById('token-progress');
                tokenProgress.style.width = `${usagePercentage}%`;
                document.getElementById('token-limit-info').textContent = `${usagePercentage}% of monthly limit`;
                
                // Update change indicators
                document.getElementById('prompt-token-change').textContent = this.formatChange(data.prompt_tokens_change);
                document.getElementById('completion-token-change').textContent = this.formatChange(data.completion_tokens_change);
                
                // Render chart
                this.renderTokensChart(data.history || []);
            })
            .catch(error => {
                console.error('Error loading token usage:', error);
            });
    }

    loadRequestStats() {
        fetch('/admin/api/request-stats')
            .then(response => response.json())
            .then(data => {
                this.data.requests = data;
                
                // Update metrics
                document.getElementById('total-requests').textContent = this.formatNumber(data.total_requests || 0);
                document.getElementById('avg-response-time').textContent = `${data.avg_response_time || 0}ms`;
                document.getElementById('success-rate').textContent = `${data.success_rate || 0}%`;
                document.getElementById('error-rate').textContent = `${data.error_rate || 0}%`;
                
                // Update change indicators
                document.getElementById('requests-change').textContent = this.formatChange(data.requests_change);
                document.getElementById('response-time-change').textContent = this.formatChange(data.response_time_change, true);
                document.getElementById('success-rate-change').textContent = this.formatChange(data.success_rate_change);
                document.getElementById('error-rate-change').textContent = this.formatChange(data.error_rate_change, true);
                
                // Render chart
                this.renderRequestsChart(data.history || []);
            })
            .catch(error => {
                console.error('Error loading request stats:', error);
            });
    }

    loadModelUsage() {
        fetch('/admin/api/model-usage')
            .then(response => response.json())
            .then(data => {
                this.data.models = data;
                
                // Render pie chart
                this.renderModelsPieChart(data.models || []);
                
                // Render model cards
                this.renderModelCards(data.models || []);
            })
            .catch(error => {
                console.error('Error loading model usage:', error);
            });
    }

    loadRecentErrors() {
        fetch('/admin/api/recent-errors')
            .then(response => response.json())
            .then(data => {
                this.data.errors = data.errors || [];
                this.renderErrorList(data.errors || []);
            })
            .catch(error => {
                console.error('Error loading recent errors:', error);
            });
    }

    loadRecentApiCalls() {
        // Load search API calls
        fetch('/admin/api/search-logs?limit=5')
            .then(response => response.json())
            .then(data => {
                this.renderApiCalls(data.logs || [], 'search-api-logs');
            })
            .catch(error => {
                console.error('Error loading search API calls:', error);
            });
        
        // Load ask API calls
        fetch('/admin/api/ask-logs?limit=5')
            .then(response => response.json())
            .then(data => {
                this.renderApiCalls(data.logs || [], 'ask-api-logs');
            })
            .catch(error => {
                console.error('Error loading ask API calls:', error);
            });
    }

    renderTokensChart(history) {
        const ctx = document.getElementById('tokens-chart');
        
        if (!ctx) return;
        
        // Destroy previous chart if it exists
        if (this.charts.tokens) {
            this.charts.tokens.destroy();
        }
        
        const dates = history.map(item => item.date);
        const promptTokens = history.map(item => item.prompt_tokens);
        const completionTokens = history.map(item => item.completion_tokens);
        
        this.charts.tokens = new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [
                    {
                        label: 'Prompt Tokens',
                        data: promptTokens,
                        borderColor: 'rgba(var(--primary-color-rgb), 0.8)',
                        backgroundColor: 'rgba(var(--primary-color-rgb), 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'Completion Tokens',
                        data: completionTokens,
                        borderColor: 'rgba(var(--info-color-rgb), 0.8)',
                        backgroundColor: 'rgba(var(--info-color-rgb), 0.1)',
                        tension: 0.4,
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Token Usage Over Time'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    renderRequestsChart(history) {
        const ctx = document.getElementById('requests-chart');
        
        if (!ctx) return;
        
        // Destroy previous chart if it exists
        if (this.charts.requests) {
            this.charts.requests.destroy();
        }
        
        const dates = history.map(item => item.date);
        const requests = history.map(item => item.requests);
        const successRate = history.map(item => item.success_rate);
        
        this.charts.requests = new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [
                    {
                        label: 'Requests',
                        data: requests,
                        borderColor: 'rgba(var(--primary-color-rgb), 0.8)',
                        backgroundColor: 'rgba(var(--primary-color-rgb), 0.1)',
                        tension: 0.4,
                        fill: true,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Success Rate (%)',
                        data: successRate,
                        borderColor: 'rgba(var(--success-color-rgb), 0.8)',
                        backgroundColor: 'rgba(var(--success-color-rgb), 0.1)',
                        tension: 0.4,
                        fill: false,
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'API Requests Over Time'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        type: 'linear',
                        display: true,
                        position: 'left',
                    },
                    y1: {
                        beginAtZero: true,
                        type: 'linear',
                        display: true,
                        position: 'right',
                        min: 0,
                        max: 100,
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                }
            }
        });
    }

    renderModelsPieChart(models) {
        const ctx = document.getElementById('models-pie-chart');
        
        if (!ctx) return;
        
        // Destroy previous chart if it exists
        if (this.charts.models) {
            this.charts.models.destroy();
        }
        
        const labels = models.map(model => model.name);
        const data = models.map(model => model.usage);
        const backgroundColors = [
            'rgba(75, 192, 192, 0.8)',
            'rgba(54, 162, 235, 0.8)',
            'rgba(153, 102, 255, 0.8)',
            'rgba(255, 159, 64, 0.8)',
            'rgba(255, 99, 132, 0.8)',
            'rgba(255, 206, 86, 0.8)'
        ];
        
        this.charts.models = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: backgroundColors.slice(0, models.length),
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                    },
                    title: {
                        display: true,
                        text: 'API Usage by Model'
                    }
                }
            }
        });
    }

    renderModelCards(models) {
        const container = document.getElementById('models-container');
        
        if (!container) return;
        
        // Clear existing content
        container.innerHTML = '';
        
        // Create a card for each model
        models.forEach(model => {
            const modelCard = document.createElement('div');
            modelCard.className = 'model-card';
            modelCard.innerHTML = `
                <h4>${model.name}</h4>
                <div class="model-stats">
                    <div class="model-stat">
                        <div class="model-stat-value">${this.formatNumber(model.requests)}</div>
                        <div>Requests</div>
                    </div>
                    <div class="model-stat">
                        <div class="model-stat-value">${this.formatNumber(model.tokens)}</div>
                        <div>Tokens</div>
                    </div>
                    <div class="model-stat">
                        <div class="model-stat-value">${model.avg_response_time}ms</div>
                        <div>Avg Time</div>
                    </div>
                    <div class="model-stat">
                        <div class="model-stat-value">${model.success_rate}%</div>
                        <div>Success</div>
                    </div>
                </div>
            `;
            container.appendChild(modelCard);
        });
        
        // Add a message if no models are available
        if (models.length === 0) {
            const noData = document.createElement('div');
            noData.className = 'text-center text-muted';
            noData.textContent = 'No model usage data available.';
            container.appendChild(noData);
        }
    }

    renderErrorList(errors) {
        const container = document.getElementById('errors-container');
        
        if (!container) return;
        
        // Clear existing content
        container.innerHTML = '';
        
        // Create an item for each error
        errors.forEach(error => {
            const errorItem = document.createElement('div');
            errorItem.className = 'error-item';
            errorItem.innerHTML = `
                <div class="error-type">${error.type || 'Unknown Error'}</div>
                <div class="error-message">${error.message || 'No error message'}</div>
                <div class="error-timestamp">${error.timestamp || 'Unknown time'}</div>
            `;
            container.appendChild(errorItem);
        });
        
        // Add a message if no errors are available
        if (errors.length === 0) {
            const noErrors = document.createElement('div');
            noErrors.className = 'text-center text-success';
            noErrors.innerHTML = '<i class="fas fa-check-circle"></i> No recent errors';
            container.appendChild(noErrors);
        }
    }

    renderApiCalls(logs, containerId) {
        const container = document.getElementById(containerId);
        
        if (!container) return;
        
        // Clear existing content
        container.innerHTML = '';
        
        // Create an item for each API call
        logs.forEach(log => {
            const apiCall = document.createElement('div');
            apiCall.className = `log-item ${log.success ? 'success' : 'error'}`;
            
            // Determine if it's a search or ask log
            const isSearch = containerId.includes('search');
            
            apiCall.innerHTML = `
                <div class="log-header">
                    <div class="log-timestamp">${log.timestamp || 'Unknown time'}</div>
                    <div class="log-status">${log.success ? '<i class="fas fa-check-circle"></i> Success' : '<i class="fas fa-times-circle"></i> Failed'}</div>
                </div>
                <div class="log-content">
                    <div class="log-query">${isSearch ? (log.query || 'No query') : (log.question || 'No question')}</div>
                    ${log.model ? `<div class="log-model">Model: ${log.model}</div>` : ''}
                    ${log.tokens ? `<div class="log-tokens">Tokens: ${log.tokens}</div>` : ''}
                    ${log.response_time ? `<div class="log-response-time">Response time: ${log.response_time}ms</div>` : ''}
                </div>
            `;
            container.appendChild(apiCall);
        });
        
        // Add a message if no logs are available
        if (logs.length === 0) {
            const noLogs = document.createElement('div');
            noLogs.className = 'text-center text-muted';
            noLogs.textContent = 'No recent API calls.';
            container.appendChild(noLogs);
        }
    }

    formatNumber(number) {
        return new Intl.NumberFormat().format(number);
    }

    formatChange(change, isReversed = false) {
        if (!change) return 'No change';
        
        const value = parseFloat(change);
        const isPositive = isReversed ? value < 0 : value > 0;
        const className = isPositive ? 'positive' : 'negative';
        const sign = value > 0 ? '+' : '';
        
        return `<span class="${className}">${sign}${value}% from last week</span>`;
    }

    toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(err => {
                console.error(`Error attempting to enable fullscreen mode: ${err.message}`);
            });
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            }
        }
    }

    showNotification(message, type = 'info') {
        // This function could be implemented to show a notification
        // For simplicity, we'll just log to console
        console.log(`[${type.toUpperCase()}] ${message}`);
    }
}

// Initialize the OpenAI Dashboard
const openaiDashboard = new OpenAIDashboard();
