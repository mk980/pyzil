const divContainer = document.querySelector('#nextButton', '#answerButton');


function show() {
    divContainer.style.display = 'block';
}

function hide() {
    divContainer.style.display = 'none';
}
document.getElementById('answerButton').addEventListener("click", show);

document.getElementById('nextButton').addEventListener("click", hide);