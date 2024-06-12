import {ApiConnector} from './connector.js';
import {Grid, h} from "./gridjs.6.2.0.js";

// events
document.addEventListener('DOMContentLoaded', () => {
    doTheData();

    // Get the modal
    const modal = document.getElementById("newEntityModal");

    // Get the button that opens the modal
    const btn = document.getElementById("newEntityButton");

    // Get the <span> element that closes the modal
    const span = document.getElementsByClassName("close")[0];

    // When the user clicks the button, open the modal
    btn.onclick = () => {
        modal.style.display = "block";
    }

    // When the user clicks on <span> (x), close the modal
    span.onclick = () => {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    }

    // Handle form submission
    const form = document.getElementById("newEntityForm");
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const entityName = document.getElementById("entityName").value;
        const entityDescription = document.getElementById("entityDescription").value;

        console.log("Entity Name:", entityName);
        console.log("Entity Description:", entityDescription);

        // Here you would typically send the form data to the server
        // For example, using fetch:
        /*
        fetch('/your-endpoint', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: entityName,
                description: entityDescription
            })
        }).then(response => response.json())
          .then(data => {
              console.log('Success:', data);
          })
          .catch((error) => {
              console.error('Error:', error);
          });
        */

        // Close the modal after submitting the form
        modal.style.display = "none";
    });
});


function doTheData() {
    new Grid({
            columns: [
                "Id",
                "Method",
                "Name",
                "URL",
                {
                    name: "Status",
                    formatter: (cell) => {
                        return h('span',
                            {
                                className: 'mockStatus ' + cell,
                            },
                            cell);
                    }
                },
                "Labels",
                {
                    name: "Created At",
                    formatter: (cell) => convertDate(cell)
                },
                {
                    name: "Updated At",
                    formatter: (cell) => convertDate(cell)
                },
                "Request Count",
                {
                    name: 'Edit',
                    formatter: (cell, row) => {
                        return h('button',
                            {
                                // TODO: add cool styles
                                className: 'py-2 mb-4 px-4 border rounded-md text-white bg-blue-600',
                                onClick: () => window.location.href = `/ui/mocks/${row.cells[0].data}`,
                            },
                            'Edit');
                    }
                },
            ],
            search: true,
            sort: true,
            resizable: true,
            server: {
                url: '/api/mocks',
                then:
                    data => data.mocks.map(mock => [
                        mock.id,
                        mock.method,
                        mock.name,
                        mock.url,
                        mock.status,
                        mock.labels,
                        mock.createdAt,
                        mock.updatedAt,
                        mock.requestsCount]),
            }
        }
    ).render(document.getElementById("wrapper"));
}

// const connector = new ApiConnector();
// connector.listMocks().then(data => {
//     displayData(data);
// });

function convertDate(isoString) {
    const date = new Date(isoString);
    const locale = navigator.language || navigator.languages[0]
    const format = {
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        hour12: false
    };
    return date.toLocaleString(locale, format);
}

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
