const totalQuestions = 10; // Replace with the actual number of questions
let answeredQuestions = 0;

function updateProgressBar() {
  const progressPercentage = (answeredQuestions / totalQuestions) * 100;
  const progressText = `Questions Answered: ${answeredQuestions} of ${totalQuestions}`;

  const progressBarElement = document.getElementById('progress-bar');
  progressBarElement.style.width = `${progressPercentage}%`;

  const progressTextElement = document.getElementById('progress-text');
  progressTextElement.textContent = progressText;
}

// Update the progress bar initially
updateProgressBar();

// Update the progress bar when an answer is submitted
function handleAnswerSubmission(correctAnswer) {
  // Increment the answered questions count
  answeredQuestions++;

  // Update the progress bar
  updateProgressBar();

  // Check if all questions have been answered
  if (answeredQuestions === totalQuestions) {
    // Quiz is finished, display completion message or redirect to completion page
    alert('Quiz completed!');
  }
}
