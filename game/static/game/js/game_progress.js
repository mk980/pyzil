const progressBar = document.querySelector('.progress-bar');
let progress = 0; // Initialize progress variable

// Update progress based on game progress
// For example, if answering questions correctly increases progress
function updateProgress() {
  progress += 10; // Increase progress by 10%
  progressBar.style.width = progress + '%'; // Update progress bar width
}

// Update progress when the game progresses
// For example, after answering a question correctly
document.getElementById('answerForm').addEventListener('submit', () => {
  updateProgress();
});
