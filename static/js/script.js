const generateBtn = document.getElementById("generateBtn");
const copyBtn = document.getElementById("copyBtn");

const storyOutput = document.getElementById("storyOutput");
const loading = document.getElementById("loading");


generateBtn.addEventListener("click", generateStory);


async function generateStory() {

    const topic = document.getElementById("topic").value;
    const genre = document.getElementById("genre").value;
    const characters = document.getElementById("characters").value;
    const setting = document.getElementById("setting").value;
    const mood = document.getElementById("mood").value;
    const length = document.getElementById("length").value;


    // Make sure the user entered a topic

    if (!topic.trim()) {

        alert("Please enter a story topic.");

        return;
    }


    // Show loading

    loading.classList.remove("hidden");

    storyOutput.innerHTML = "";

    generateBtn.disabled = true;


    try {

        const response = await fetch("/generate", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                topic: topic,

                genre: genre,

                characters: characters,

                setting: setting,

                mood: mood,

                length: length

            })

        });


        const data = await response.json();


        if (data.success) {

            storyOutput.textContent = data.story;

        } else {

            storyOutput.textContent =
                "Error: " + data.error;

        }


    } catch (error) {

        console.error(error);

        storyOutput.textContent =
            "Something went wrong. Please try again.";

    }


    loading.classList.add("hidden");

    generateBtn.disabled = false;

}


copyBtn.addEventListener("click", copyStory);


function copyStory() {

    const story = storyOutput.innerText;

    if (!story.trim()) {

        return;

    }


    navigator.clipboard.writeText(story);

    alert("Story copied!");

}