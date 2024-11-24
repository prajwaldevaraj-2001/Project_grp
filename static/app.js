const socket = io.connect("http://localhost:5000");

function fetchInventory() {
    fetch("/api/products")
        .then(response => response.json())
        .then(data => {
            const inventoryDiv = document.getElementById("inventory");
            inventoryDiv.innerHTML = data.map(product => `
                <p>${product.Name}: ${product.StockLevel} units</p>
            `).join("");
        });
}

// Listen for real-time updates
socket.on("update", (data) => {
    console.log("Real-time update:", data);
    fetchInventory();
});

// Initial data fetch
fetchInventory();
