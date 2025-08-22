// JuSimples Admin API Integration
// Handles all API calls to fetch admin panel data

class AdminAPI {
    constructor() {
        this.baseUrl = '';
    }

    // Basic fetch wrapper with error handling
    async fetchApi(endpoint, options = {}) {
        try {
            const response = await fetch(this.baseUrl + endpoint, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.status} ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`Error fetching ${endpoint}:`, error);
            throw error;
        }
    }

    // Dashboard Stats
    async getDashboardStats() {
        return await this.fetchApi('/admin/api/dashboard-stats');
    }

    // Analytics Data
    async getAnalyticsOverview() {
        return await this.fetchApi('/admin/api/analytics/overview');
    }

    // Search Logs
    async getSearchLogs(page = 1, limit = 10, query = '', status = 'all') {
        let url = `/admin/api/search-logs?page=${page}&limit=${limit}`;
        if (query) url += `&query=${encodeURIComponent(query)}`;
        if (status !== 'all') url += `&status=${status}`;
        return await this.fetchApi(url);
    }

    // Ask Logs
    async getAskLogs(page = 1, limit = 10, query = '', status = 'all') {
        let url = `/admin/api/ask-logs?page=${page}&limit=${limit}`;
        if (query) url += `&query=${encodeURIComponent(query)}`;
        if (status !== 'all') url += `&status=${status}`;
        return await this.fetchApi(url);
    }

    // Knowledge Base
    async getKnowledgeBase() {
        return await this.fetchApi('/admin/api/knowledge-base');
    }

    // Recent Activity
    async getRecentActivity() {
        return await this.fetchApi('/admin/api/recent-activity');
    }

    // Chart Data
    async getChartData() {
        return await this.fetchApi('/admin/api/chart-data');
    }

    // Database Stats
    async getDatabaseStats() {
        return await this.fetchApi('/admin/api/database/overview');
    }

    // Log Search History
    async logSearch(query, options = {}) {
        return await this.fetchApi('/admin/api/log-search', {
            method: 'POST',
            body: JSON.stringify({
                query,
                ...options
            })
        });
    }

    // Log Ask History
    async logAsk(question, options = {}) {
        return await this.fetchApi('/admin/api/log-ask', {
            method: 'POST',
            body: JSON.stringify({
                question,
                ...options
            })
        });
    }
}

// Initialize the API
const adminApi = new AdminAPI();
