const fileBox = document.getElementById("fileBox");
const fileInput = document.getElementById("fileInput");
const form = document.getElementById("uploadForm");
const resultDiv = document.getElementById("result");
const progressContainer = document.getElementById("progressContainer");
const progressBar = document.getElementById("progressBar");
const browseText = document.getElementById("browseText");
const fileName = document.getElementById("fileName");

// Open file dialog when clicking "browse"
browseText.onclick = () => fileInput.click();

// Drag & drop styling
fileBox.addEventListener("dragover", (e) => {
  e.preventDefault();
  fileBox.style.background = "rgba(255,255,255,0.1)";
});

fileBox.addEventListener("dragleave", () => {
  fileBox.style.background = "transparent";
});

fileBox.addEventListener("drop", (e) => {
  e.preventDefault();
  fileBox.style.background = "transparent";
  fileInput.files = e.dataTransfer.files;
  displayFileInfo(fileInput.files[0]);
});

// Show filename when selecting via dialog
fileInput.addEventListener("change", () => {
  displayFileInfo(fileInput.files[0]);
});

// Display filename only
function displayFileInfo(file) {
  if (file) {
    fileName.textContent = `📄 ${file.name} (${(file.size / 1024).toFixed(2)} KB)`;
  }
}

// Upload form
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const file = fileInput.files[0];
  if (!file) {
    alert("Please select a file first!");
    return;
  }

  resultDiv.innerHTML = "";
  progressContainer.style.display = "block";
  progressBar.style.width = "0%";

  const formData = new FormData();
  formData.append("file", file);

  try {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "https://fileuploader-bvid.onrender.com/upload", true);

    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable) {
        const percent = (event.loaded / event.total) * 100;
        progressBar.style.width = percent + "%";
      }
    };

    xhr.onload = () => {
      if (xhr.status === 200) {
        const data = JSON.parse(xhr.responseText);
        resultDiv.innerHTML = `
          ✅ <strong>Upload successful!</strong><br>
          <a href="${data.url}" target="_blank">${data.url}</a>
        `;
      } else {
        console.log("File size too large",xhr.statusText)
        resultDiv.innerHTML = `❌ Error: ${xhr.statusText}`;
      }
      progressContainer.style.display = "none";
    };

    xhr.onerror = () => {
      resultDiv.innerHTML = "❌ Upload failed!";
      progressContainer.style.display = "none";
    };

    xhr.send(formData);
  } catch (err) {
    resultDiv.innerHTML = `❌ ${err.message}`;
    progressContainer.style.display = "none";
  }
});
