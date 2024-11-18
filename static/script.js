const socket = io();

function fetchInventory() {
    fetch('/inventory')
        .then(res => res.json())
        .then(data => {
            const tbody = document.querySelector('#inventory-table tbody');
            tbody.innerHTML = ''; // Clear existing rows
            data.forEach(item => {
                const row = `
                    <tr>
                        <td>${item.name}</td>
                        <td>${item.stock_level}</td>
                        <td>
                            <button onclick="deleteItem('${item.name}')">Delete</button>
                        </td>
                    </tr>`;
                tbody.innerHTML += row;

                // Check stock levels
                if (item.stock_level < 5) {
                    socket.emit('check_stock', item);
                }
            });
        });
}

function deleteItem(name) {
    fetch(`/inventory/${name}`, { method: 'DELETE' })
        .then(() => fetchInventory());
}

socket.on('low_stock_alert', data => {
    const alertDiv = document.getElementById('alerts');
    alertDiv.innerHTML = `<p>${data.message}</p>`;
});

document.addEventListener('DOMContentLoaded', fetchInventory);
