const BACKEND_URL = "";

async function indexPDF() {
  const fileInput = document.getElementById("pdfFile");

  if (!fileInput.files.length) {
    alert("Please select a PDF file");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  const response = await fetch(`${BACKEND_URL}/index-pdf`, {
    method: "POST",
    body: formData
  });

  if (!response.ok) {
    alert("Failed to index PDF");
    return;
  }

  const data = await response.json();
  alert(`Indexed ${data.chunks_indexed} chunks`);
}

async function askQuestion() {
  console.log("ASK BUTTON CLICKED");
  const questionInput = document.getElementById("question");
  const loadingDiv = document.getElementById("loading");
  const askBtn = document.getElementById("askBtn");
  const enablePlanning =document.getElementById("enablePlanning").checked;
  

  const question = questionInput.value;

  if (!question.trim()) {
    alert("Please enter a question");
    return;
  }

  // Clear previous output
  document.getElementById("plan").innerText = "";
  document.getElementById("answer").innerText = "";
  //document.getElementById("subQuestions").innerHTML = "";

  // Disable UI elements
  askBtn.disabled = true;
  questionInput.disabled = true;
  loadingDiv.style.display = "block";

  try {
    const response = await fetch(`/qa`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 
        question,
        enable_planning: enablePlanning
    })
    });

    if (!response.ok) {
      throw new Error("Request failed");
    }

    const data = await response.json();
    document.getElementById("plan").innerText =data.plan || "Planning disabled"

    //document.getElementById("plan").innerText = data.plan || "";
    document.getElementById("answer").innerText = data.answer || "";
    //document.getElementById("context").innerText = data.context || "";

    // Render sub-questions
    const subQuestionsList = document.getElementById("subQuestions");
    subQuestionsList.innerHTML = "";

    if (Array.isArray(data.sub_questions)) {
        data.sub_questions.forEach((sq, index) => {
        const li = document.createElement("li");
        li.innerText = `${index + 1}. ${sq}`;
        subQuestionsList.appendChild(li);
    });
}       

  } catch (error) {
    alert("Error while processing the question");
  } finally {
    // Re-enable UI elements
    askBtn.disabled = false;
    questionInput.disabled = false;
    loadingDiv.style.display = "none";
  }
}

//document.getElementById("plan").innerText =
  //data.plan || "Planning disabled";

//renderSubQuestions(data.sub_questions || []);
