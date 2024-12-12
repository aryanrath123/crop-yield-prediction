const form = document.querySelector("#predictionForm");
const resultDiv = document.querySelector("#result");
const loadingDiv = document.querySelector("#loading");

// Handle form submission
form.addEventListener("submit", (event) => {
  event.preventDefault(); // Prevent default form submission

  // Hide the result and show the loading spinner
  resultDiv.classList.add("d-none");
  loadingDiv.style.display = "block";

  // Collect form data
  const formData = new FormData(form);

  // Send data via AJAX
  fetch("/predict", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      loadingDiv.style.display = "none"; // Hide the loading spinner
      if (data.error) {
        // Display error message
        resultDiv.textContent = data.error;
        resultDiv.classList.remove("alert-success");
        resultDiv.classList.add("alert-danger");
      } else {
        // Display prediction result
        resultDiv.innerHTML = `
                    <h4>Predicted Yield for ${data.crop}</h4>
                    <p><strong>Yield:</strong> ${data.predicted_yield.toFixed(
                      2
                    )}</p>
                    <p><strong>Inputs:</strong></p>
                    <ul>
                        <li>Precipitation: ${
                          data.inputs.precipitation
                        } mm/day</li>
                        <li>Specific Humidity: ${
                          data.inputs.specific_humidity
                        } g/kg</li>
                        <li>Relative Humidity: ${
                          data.inputs.relative_humidity
                        }%</li>
                        <li>Temperature: ${data.inputs.temperature}°C</li>
                    </ul>
                `;
        resultDiv.classList.remove("alert-danger");
        resultDiv.classList.add("alert-success");
      }
      resultDiv.classList.remove("d-none");
    })
    .catch((error) => {
      loadingDiv.style.display = "none"; // Hide the loading spinner
      resultDiv.textContent = "An error occurred while predicting yield.";
      resultDiv.classList.remove("alert-success");
      resultDiv.classList.add("alert-danger");
      resultDiv.classList.remove("d-none");
    });
});
