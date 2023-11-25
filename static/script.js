// Function to fetch data from API and populate the table
async function fetchData(apiUrl, industry) {
    try {
        //highlight the industry
        // Remove the 'active' class from all buttons
        var buttons = document.getElementsByClassName('top-bar')[0].getElementsByTagName('button');
        for (var i = 0; i < buttons.length; i++) {
            buttons[i].classList.remove('active');
        }

        // Add the 'active' class to the clicked button
        document.getElementById('nav_' + industry).classList.add('active');

        const response = await fetch(apiUrl);
        const jsonData = await response.json();

        // Extract stock data from the "data" array
        const stockData = jsonData.data;
        const preferenceData = jsonData.preference;

        // Populate the table
        var id = 'stockTable';
        const table = document.getElementById(id);
        const tbody = table.getElementsByTagName('tbody')[0];
        tbody.innerHTML = ''; // Clear existing rows

        stockData.forEach(stock => {
            const row = tbody.insertRow();
            // Add more cells as needed based on the structure of the stock data

            stock.forEach((value, index) => {
                const cell = row.insertCell(index);
                cell.textContent = value;
            });
        });

        //populate the required graphs
        var piechart = document.getElementById('pieChart');
        piechart.src = './images/' + industry + '_market_cap.png';
        var barGraph1 = document.getElementById('barGraph1');
        barGraph1.src = './images/' + industry + '_pe.png';
        var barGraph2 = document.getElementById('barGraph2');
        barGraph2.src = './images/' + industry + '_net_profits.png';
        var barGraph3 = document.getElementById('barGraph3');
        barGraph3.src = './images/' + industry + '_sales.png';

        //suggestion logic:

        // Threshold to consider a company for suggestion
        const suggestionThreshold = 0.25;

        // Print preferenceData for comparison
        preferenceData.forEach(company => {
            console.log(`${company[0]}: ${company[1]}`);
        });

        // Filter companies with scores above the threshold
        const suggestedCompanies = preferenceData
            .filter(company => company[1] > suggestionThreshold);

        // Sort the suggested companies by score in descending order
        suggestedCompanies.sort((a, b) => b[1] - a[1]);

        // Total amount to distribute (e.g., 100)
        const totalAmount = 100;

        let suggestionMessage;

        if (suggestedCompanies.length > 0) {
            // Normalize scores
            const maxScore = Math.max(...suggestedCompanies.map(company => company[1]));
            const normalizedScores = suggestedCompanies.map(company => ({
                name: company[0],
                score: company[1] / maxScore
            }));

            // Calculate the total of normalized scores
            const totalNormalizedScore = normalizedScores.reduce((acc, company) => acc + company.score, 0);

            // Distribute the total amount based on normalized scores
            const distribution = normalizedScores.reduce((acc, company) => {
                const share = (company.score / totalNormalizedScore) * totalAmount;
                acc[company.name] = share;
                return acc;
            }, {});
            suggestionMessage = suggestedCompanies.length + " of the companies are outperforming.Its suggested to invest in them."
            console.log(distribution);

            // Update suggestion message content
            const suggestionMessageElement = document.getElementById("suggestionMessage");
            suggestionMessageElement.textContent = suggestionMessage;

            // Update distribution list content
            const distributionListElement = document.getElementById("distributionList");
            distributionListElement.innerHTML = ""; // Clear existing content

            // Loop through the distribution object and create list items
            for (const company in distribution) {
                const listItemElement = document.createElement("li");
                listItemElement.textContent = `${company}: ${distribution[company]}%`;
                distributionListElement.appendChild(listItemElement);
            }
        } else {
            // No company above the threshold, suggest top 3 companies equally
            const top3Companies = preferenceData
                .sort((a, b) => b[1] - a[1])
                .slice(0, 3);

            const maxScore = Math.max(...top3Companies.map(company => company[1]));
            const normalizedScores = top3Companies.map(company => ({
                name: company[0],
                score: company[1] / maxScore
            }));

            // Calculate the total of normalized scores
            const totalNormalizedScore = normalizedScores.reduce((acc, company) => acc + company.score, 0);

            // Distribute the total amount based on normalized scores
            const distribution = normalizedScores.reduce((acc, company) => {
                const share = (company.score / totalNormalizedScore) * totalAmount;
                acc[company.name] = Number(share.toFixed(2));
                return acc;
            }, {});
            suggestionMessage = "No one of the companies are outperforming others. Its wise to split the share among 3 of the top"
            console.log(distribution);

            // Update suggestion message content
            const suggestionMessageElement = document.getElementById("suggestionMessage");
            suggestionMessageElement.textContent = suggestionMessage;

            // Update distribution list content
            const distributionListElement = document.getElementById("distributionList");
            distributionListElement.innerHTML = ""; // Clear existing content

            // Loop through the distribution object and create list items
            for (const company in distribution) {
                const listItemElement = document.createElement("li");

                listItemElement.textContent = `${company}: ${distribution[company]}%`;
                distributionListElement.appendChild(listItemElement);
            }
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Call the fetchData function for each industry
fetchData('http://localhost:8000/get_data/computer_software', 'computer_software');