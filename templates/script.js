document.getElementById("uploadForm").addEventListener("submit", function(event) {
    event.preventDefault();

    let formData = new FormData();
    let imageFile = document.getElementById("imageInput").files[0];
    let textInput = document.getElementById("textInput").value;

    if (imageFile) {
        formData.append("image", imageFile);
    }
    formData.append("text_input", textInput);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        let resultDiv = document.getElementById("results");
        resultDiv.innerHTML = `<h2>Suggested Songs:</h2><ul>` +
            data.songs.map(song => `<li>${song}</li>`).join("") +
            `</ul><h2>Suggested Captions:</h2><ul>` +
            data.captions.map(cap => `<li>${cap}</li>`).join("") + `</ul>`;

        if (data.image_url) {
            resultDiv.innerHTML += `<img src="${data.image_url}" alt="Uploaded Image" width="200">`;
        }
    })
    .catch(error => console.error("Error:", error));
});