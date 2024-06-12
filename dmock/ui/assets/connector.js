export class ApiConnector {
    constructor() {
    }

    async listMocks() {
        return await fetch('/api/mocks').then(response => response.json());
    }

    async getMock(id) {
        return await fetch(`/api/mocks/${id}`).then(response => response.json());
    }

    async getMockRules(id) {
        return await fetch(`/api/mocks/${id}/rules`).then(response => response.json());
    }

    async getMockLog(id) {
        return await fetch(`/api/mocks/${id}/logs`).then(response => response.json());
    }

    async getMockRule(id, ruleId) {
        return await fetch(`/api/mocks/${id}/rules/${ruleId}`).then(response => response.json());
    }

    async createMock(mock) {
        return await fetch('/api/mocks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(mock)
        }).then(response => response.json());
    }

    async deleteMock(id) {
        return await fetch(`/api/mocks/${id}`, {
            method: 'DELETE'
        }).then(response => response.json());
    }

    async updateMock(mock) {
        return await fetch(`/api/mocks/${mock.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(mock)
        }).then(response => response.json());
    }

    async createMockRule(id, rule) {
        return await fetch(`/api/mocks/${id}/rules`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(rule)
        }).then(response => response.json());
    }

    async updateMockRule(id, rule) {
        return await fetch(`/api/mocks/${id}/rules/${rule.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(rule)
        }).then(response => response.json());
    }

    async deleteMockRule(id, ruleId) {
        return await fetch(`/api/mocks/${id}/rules/${ruleId}`, {
            method: 'DELETE'
        }).then(response => response.json());
    }

    async setMockStatus(id, status) {
        return await fetch(`/api/mocks/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({status: status})
        }).then(response => response.json());
    }

    async setMockRuleStatus(id, ruleId, isActive) {
        return await fetch(`/api/mocks/${id}/rules/${ruleId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({isActive: isActive})
        }).then(response => response.json());
    }
}
