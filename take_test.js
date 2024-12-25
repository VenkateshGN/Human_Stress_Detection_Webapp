// Variables 
let currentQuestion = 0;
const questions = [
    "What is your favorite color?",
    "What do you enjoy doing in your free time?",
    "What is your dream job?",
    "Describe your ideal vacation.",
    "Who inspires you the most?",
    "What is your favorite book or movie?",
    "What are your hobbies?",
    "What is your happiest memory?",
    "Where do you see yourself in 5 years?",
    "What do you value most in life?",
    "How do you handle stress?",
    "What is your favorite meal?",
    "What do you like about your job/studies?",
    "Describe a goal you’ve achieved recently.",
    "What motivates you to work hard?"
];

let recorder, audioBlob, audioURL;
let timerInterval, audioSeconds = 0;
let progressBar = document.getElementById('progress-bar');

// Get DOM elements
const questionElement = document.getElementById("question");
const timerElement = document.getElementById("audio-timer");
const playButton = document.getElementById("play-audio");
const stopButton = document.getElementById("stop-recording");
const startButton = document.getElementById("start-recording");
const nextButton = document.getElementById("next-question");
const submitButton = document.getElementById("submit-button");
const flashMessage = document.getElementById("flash-message");

// Update Question
function updateQuestion() {
    questionElement.textContent = `Question ${currentQuestion + 1}: ${questions[currentQuestion]}`;
    // Hide Submit button until the last question
    if (currentQuestion === questions.length - 1) {
        submitButton.style.display = "block";
        nextButton.style.display = "none";  // Hide Next button on the last question
    } else {
        submitButton.style.display = "none";
        nextButton.style.display = "block";
    }
}

// Format time for the timer
function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs < 10 ? "0" : ""}${secs}`;
}

// Start Recording
startButton.addEventListener("click", () => {
    startButton.disabled = true;  // Disable Start button
    stopButton.disabled = false;  // Enable Stop button
    playButton.disabled = true;  // Disable Play button until recording is done
    audioSeconds = 0;
    timerElement.textContent = "0:00";
    progressBar.style.width = "0%";

    navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
        recorder = new MediaRecorder(stream);
        recorder.start();

        // Timer
        timerInterval = setInterval(() => {
            audioSeconds++;
            timerElement.textContent = formatTime(audioSeconds);

            // Update progress bar
            const progress = (audioSeconds / 100) * 100;  // Arbitrary max duration for demo
            progressBar.style.width = progress + "%";
        }, 1000);

        recorder.addEventListener("dataavailable", (event) => {
            audioBlob = event.data;
            audioURL = URL.createObjectURL(audioBlob);
            playButton.disabled = false; // Enable play button after recording
        });
    }).catch((error) => {
        console.error("Error accessing the microphone: ", error);
    });
});

// Stop Recording
stopButton.addEventListener("click", () => {
    stopButton.disabled = true;  // Disable Stop button once clicked
    startButton.disabled = false; // Enable Start button for next recording

    recorder.stop();  // Stop the recording
    clearInterval(timerInterval); // Stop the timer
});

// Play Audio
playButton.addEventListener("click", () => {
    const audio = new Audio(audioURL);
    audio.play();

    // Reset progress bar when audio starts playing
    progressBar.style.width = "0%";
    audio.addEventListener('timeupdate', function () {
        const progress = (audio.currentTime / audio.duration) * 100;
        progressBar.style.width = progress + "%";
    });

    // Ensure play button is disabled after playback is done
    audio.onended = function() {
        playButton.disabled = true;
    };
});

// Navigation
nextButton.addEventListener("click", () => {
    if (currentQuestion < questions.length - 1) {
        currentQuestion++;
        updateQuestion();
        resetRecordingState(); // Reset recording states for the next question
    }
});

// Submit Action
submitButton.addEventListener("click", () => {
    flashMessage.textContent = "Your answers have been submitted!";
    flashMessage.style.display = "block";  // Show flash message
    // Optionally, add an action for submission, like sending data to a server
});

// Reset all states when moving to the next question
function resetRecordingState() {
    // Reset UI elements for the next question
    stopButton.disabled = true;
    startButton.disabled = false;
    playButton.disabled = true;
    progressBar.style.width = "0%";
    timerElement.textContent = "0:00";
    audioSeconds = 0;
}

// Initial question update
updateQuestion();
