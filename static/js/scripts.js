function submitEntry() {
    const message = document.getElementById('message').value;

    if (message.trim().length > 0) {
        // Use Fetch API to post data to the backend
        fetch('/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Clear the textarea
                document.getElementById('message').value = '';
                // Append new entry to the list
                addEntryToList(data.entry);
            }
        });
    }
}

function addEntryToList(entry) {
    const list = document.querySelector('.guestbook-list');
    const listItem = document.createElement('div');
    listItem.className = 'guestbook-item';
    listItem.innerHTML = `<time>${entry.timestamp}</time><p>${entry.message}</p>`;
    list.insertBefore(listItem, list.firstChild);
}

// Function to load existing entries
function loadEntries() {
    fetch('/entries')
        .then(response => response.json())
        .then(data => {
            data.entries.forEach(entry => addEntryToList(entry));
        });
}

// Load entries when the page loads
window.onload = loadEntries;
