function displayData(data) {
    const dataTable = document.getElementById('data-table');
    const mocks = data.mocks;

    // Clear existing data
    dataTable.innerHTML = '';

    // Create table header
    if (mocks.length > 0) {
        const headerRow = document.createElement('div');
        headerRow.className = 'row header';
        Object.keys(mocks[0]).forEach(key => {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.textContent = key;
            headerRow.appendChild(cell);
        });
        dataTable.appendChild(headerRow);
    }

    // Create table rows
    mocks.forEach(item => {
        const row = document.createElement('div');
        row.className = 'row';
        Object.values(item).forEach(value => {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.textContent = value;
            row.appendChild(cell);
        });
        dataTable.appendChild(row);
    });

    // Display total count
    const totalRow = document.createElement('div');
    totalRow.className = 'row';
    const totalCell = document.createElement('div');
    totalCell.className = 'cell';
    totalCell.colSpan = Object.keys(mocks[0]).length;
    totalCell.textContent = `Total: ${data.total}`;
    totalRow.appendChild(totalCell);
    dataTable.appendChild(totalRow);
}


function mockList() {
    const api = new ApiConnector();
    api.listMocks().then(data => {
        displayData(data);
    });
}

class ApiConnector {
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