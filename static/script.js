const fileInput = document.getElementById("file-input");
const browseBtn = document.getElementById("browse-button");
const rectangleParent = document.querySelector(".rectangle-parent");
const dragDropArea = document.getElementById("drag-drop-area");
const fileInfo = document.getElementById("filename-display");
const uploadForm = document.getElementById("upload-form");
const submitButton = document.getElementById("submit-button");
const uploadedImage = document.getElementById("uploadedImage");

// Event listener for browse button
browseBtn.addEventListener("click", () => {
  fileInput.click();
});

// Event listener for file input change
fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  displayFileName(file);
  displayImage(file);
});

// Function to handle file input change
function handleFileInput(file) {
  const reader = new FileReader();
  reader.onload = function () {
      uploadedImage.src = reader.result;
      uploadedImage.style.display = "block";
  };
  reader.readAsDataURL(file);
  fileInfo.textContent = file.name;
}

// Event listeners for drag and drop area
rectangleParent.addEventListener("dragover", (event) => {
  event.preventDefault();
  rectangleParent.style.border = "2px dashed #4CAF50";
});

rectangleParent.addEventListener("dragleave", () => {
  rectangleParent.style.border = "2px dashed #ccc";
});


rectangleParent.addEventListener("drop", (event) => {
  event.preventDefault();
  rectangleParent.style.border = "2px dashed #ccc";
  
  const file = event.dataTransfer.files[0];
  
  // Check if a file was dropped
  if (file) {
    // Check if the file is an image
    if (file.type.startsWith("image")) {
      fileInput.files = event.dataTransfer.files;
      handleFileInput(file);
    } else {
      alert("Please select an image file.");
    }
  }
});

// Funciton to validate form
function validateForm() {
  var fileInput = document.getElementById('file-input');
  var file = fileInput.files[0];
  if (!file) {
      alert("Please select a file.");
      return false; // Prevent form submission
  }
  return true; 
}

// Event listener for submit button
document.getElementById("submit-button-id").addEventListener("click", function() {

  var file = fileInput.files[0];
  if (!file) {
      alert("Please select an image to continue.");
      event.preventDefault();
  } else {
      document.getElementById("upload-form").submit();
  }
});

// Function to display file name
function displayFileName(file) {
  if (file) {
    fileInfo.textContent = file.name;
  } else {
    fileInfo.textContent = "No file selected";
  }
}

// Function to display image preview
function displayImage(file) {
  const reader = new FileReader();
  reader.onload = function () {
    uploadedImage.src = reader.result;
    uploadedImage.style.display = "block";
  };
  if (file) {
    reader.readAsDataURL(file);
  }
}

//Validating non-image file
document.getElementById("file-input").addEventListener("change", function () {
  const file = this.files[0];
  const fileType = file.type.split("/")[0];

  if (fileType !== "image") {
    alert("Please select an image file.");
    this.value = ""; 
  }
});

// Event listener for delete button
document.getElementById("delete-btn").addEventListener("click", function() {
  document.getElementById("file-input").value = "";
  document.getElementById("uploadedImage").src = "";
  document.getElementById("uploadedImage").style.display = "none";
  document.getElementById("filename-display").textContent = "No file selected";
});
