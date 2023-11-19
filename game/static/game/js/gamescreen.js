 function highlightAnswer(selectedOption) {
    const correctAnswer = document.querySelector('input[name="correct_answer"]').value;

    // Reset the styling for all answer options
    const answerOptions = document.querySelectorAll('.form-check');
    for (const option of answerOptions) {
        option.style.backgroundColor = '';
    }

    // Highlight the selected option
    if (selectedOption.value === correctAnswer) {
        selectedOption.parentElement.style.backgroundColor = 'green';
        document.getElementById('nextButton').style.display = 'block'; // Show Next Question button
    } else {
        selectedOption.parentElement.style.backgroundColor = 'red';
        document.getElementById('nextButton').style.display = 'none'; // Hide Next Question button
    }
}