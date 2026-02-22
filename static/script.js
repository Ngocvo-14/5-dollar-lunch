/**
 * 5-Dollar Lunch App - Frontend JavaScript
 * Handles all user interactions and backend communication
 */

// Function 1: Load and display all menu items
function searchItems() {
    console.log('🔍 Searching for items...');

    // Make GET request to backend /search route
    fetch('/search')
        .then(response => response.json())
        .then(data => {
            console.log('📦 Received data:', data);

            if (data.success) {
                displayResults(data.items);
            } else {
                alert('❌ Error loading items: ' + data.error);
            }
        })
        .catch(error => {
            console.error('❌ Fetch error:', error);
            alert('Failed to load items. Make sure MongoDB is connected!');
        });
}

// Function 2: Display items on the page
function displayResults(items) {
    const resultsDiv = document.getElementById('results');

    // Clear previous results
    resultsDiv.innerHTML = '';

    // Check if no items found
    if (items.length === 0) {
        resultsDiv.innerHTML = `
            <div class="empty-state">
                <p>📭 No lunch items found</p>
                <p>Add your first item above!</p>
            </div>
        `;
        return;
    }

    // Create a card for each item
    items.forEach(item => {
        const itemCard = document.createElement('div');
        itemCard.className = 'item-card';

        itemCard.innerHTML = `
            <div class="item-info">
                <h3>${item.name}</h3>
                <p class="price">$${item.price.toFixed(2)}</p>
            </div>
            <div class="item-actions">
                <button 
                    onclick="editItem('${item._id}', '${item.name}', ${item.price})" 
                    class="btn-edit"
                >
                    ✏️ Edit
                </button>
                <button 
                    onclick="deleteItem('${item._id}')" 
                    class="btn-delete"
                >
                    🗑️ Delete
                </button>
            </div>
        `;

        resultsDiv.appendChild(itemCard);
    });

    console.log(`✅ Displayed ${items.length} items`);
}

// Function 3: Add new item
function addItem() {
    // Get input values
    const nameInput = document.getElementById('itemName');
    const priceInput = document.getElementById('itemPrice');

    const name = nameInput.value.trim();
    const price = parseFloat(priceInput.value);

    // Validate inputs
    if (!name) {
        alert('⚠️ Please enter an item name!');
        nameInput.focus();
        return;
    }

    if (!price || price <= 0) {
        alert('⚠️ Please enter a valid price!');
        priceInput.focus();
        return;
    }

    if (price > 5.00) {
        alert('⚠️ Price must be $5.00 or less!');
        priceInput.focus();
        return;
    }

    console.log('➕ Adding item:', { name, price });

    // Make POST request to backend /add route
    fetch('/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: name,
            price: price
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('✅ ' + data.message);

                // Clear input fields
                nameInput.value = '';
                priceInput.value = '';

                // Refresh the list
                searchItems();
            } else {
                alert('❌ Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('❌ Error:', error);
            alert('Failed to add item!');
        });
}

// Function 4: Edit existing item
function editItem(id, currentName, currentPrice) {
    // Prompt user for new values
    const newName = prompt('✏️ Edit item name:', currentName);
    if (newName === null) return; // User cancelled

    const newPriceStr = prompt('✏️ Edit price:', currentPrice);
    if (newPriceStr === null) return; // User cancelled

    const newPrice = parseFloat(newPriceStr);

    // Validate
    if (!newName.trim()) {
        alert('⚠️ Name cannot be empty!');
        return;
    }

    if (!newPrice || newPrice <= 0 || newPrice > 5.00) {
        alert('⚠️ Price must be between $0.01 and $5.00!');
        return;
    }

    console.log('✏️ Updating item:', id);

    // Make PUT request to backend
    fetch(`/update/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: newName.trim(),
            price: newPrice
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('✅ ' + data.message);
                searchItems(); // Refresh the list
            } else {
                alert('❌ Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('❌ Error:', error);
            alert('Failed to update item!');
        });
}

// Function 5: Delete item
function deleteItem(id) {
    // Confirm deletion
    if (!confirm('🗑️ Are you sure you want to delete this item?')) {
        return; // User cancelled
    }

    console.log('🗑️ Deleting item:', id);

    // Make DELETE request to backend
    fetch(`/delete/${id}`, {
        method: 'DELETE'
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('✅ ' + data.message);
                searchItems(); // Refresh the list
            } else {
                alert('❌ Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('❌ Error:', error);
            alert('Failed to delete item!');
        });
}

// Auto-load items when page loads
window.addEventListener('load', function() {
    console.log('🚀 Page loaded! Ready to search items.');
    // Uncomment the line below to auto-load items on page load
    // searchItems();
});

// Allow adding item with Enter key
document.addEventListener('DOMContentLoaded', function() {
    const priceInput = document.getElementById('itemPrice');
    if (priceInput) {
        priceInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                addItem();
            }
        });
    }
});