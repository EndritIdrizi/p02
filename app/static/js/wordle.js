// Predefined word to check against - To be replaced with word from database
const savedWord = document.getElementById("word").getAttributeContent("content");

function checkWord() {
  const userInput = document.getElementById("wordInput").value.toLowerCase();
  const resultContainer = document.getElementById("results");
  const errorElement = document.getElementById("error-message"); 

  // Clear previous error message
  errorElement.textContent = ""; 

  // Validate input length and check for non-letter characters
  if (userInput.length !== 5 || !/^[a-zA-Z]{5}$/.test(userInput)) {
    errorElement.textContent = "Please enter a valid 5-letter word (only letters allowed).";
    errorElement.style.color = "red";
    return;
  }

  const letterCount = {};
  for (const letter of savedWord) {
    letterCount[letter] = (letterCount[letter] || 0) + 1;
  }

  // Array to track used positions for green and yellow
  const usedLetters = Array(5).fill(false);

  // Create a result row for the current guess
  const resultRow = document.createElement("div");
  resultRow.classList.add("result-row");

  // First pass: Check for correct letters (green)
  for (let i = 0; i < savedWord.length; i++) {
    const letter = userInput[i];
    const span = document.createElement("span");
    span.textContent = letter;
    span.style.color = "black";
    span.style.padding = "10px";
    span.style.margin = "5px";
    span.style.fontSize = "50px";

    if (letter === savedWord[i]) {
      span.style.backgroundColor = "green"; //correct positon
      letterCount[letter]--; 
      usedLetters[i] = true; //mark as used
    }

    resultRow.appendChild(span); //add to the result row
  }

  // Second pass: Check for letters that are in the word but in the wrong position (yellow)
  for (let i = 0; i < savedWord.length; i++) {
    const letter = userInput[i];
    const span = resultRow.children[i]; // Get the span created in the first pass

    if (!usedLetters[i] && savedWord.includes(letter) && letterCount[letter] > 0) {
      span.style.backgroundColor = "yellow"; //wrong position but in the word
      letterCount[letter]--; 
      usedLetters[i] = true; //mark as used
    }
  }

  // Third pass: Letters that are not in the word (red)
  for (let i = 0; i < savedWord.length; i++) {
    const letter = userInput[i];
    const span = resultRow.children[i]; // Get the span created in the first pass

    if (!usedLetters[i]) {
      span.style.backgroundColor = "red"; //not in word
    }
  }

  // Append the result row to the result container
  resultContainer.appendChild(resultRow);

  // Clear the input field for the next guess
  document.getElementById("wordInput").value = "";
}

// Add event listener to the button
document.getElementById("checkButton").addEventListener("click", checkWord);
