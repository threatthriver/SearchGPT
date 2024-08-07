const form = document.getElementById('search-form');
const responseLines = document.getElementById('response-lines');

form.addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent default form submission

    const query = form.query.value; // Get the query from the input field

    try {
        const response = await fetch('/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `query=${query}`
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        responseLines.innerHTML = ''; // Clear previous response

        if (data.length === 1 && data[0] === "No results found.") {
            // Handle the case where no results are found
            const p = document.createElement('p');
            p.textContent = "No results found.";
            responseLines.appendChild(p);
        } else {
            // Display the response line by line
            data.forEach(line => {
                const p = document.createElement('p');
                p.textContent = line;
                responseLines.appendChild(p);
            });
        }
    } catch (error) {
        console.error('Error fetching response:', error);
        // Handle the error appropriately, e.g., display an error message to the user
        responseLines.innerHTML = '';
        const p = document.createElement('p');
        p.textContent = "An error occurred. Please try again later.";
        responseLines.appendChild(p);
    }
});