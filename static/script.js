// =============================================================
// AI HR RECRUITMENT ASSISTANT
// Frontend JavaScript
// =============================================================


// =============================================================
// ANALYZE CANDIDATE
// =============================================================

async function analyzeCandidate() {

    const candidateName =
        document.getElementById(
            "candidateName"
        ).value.trim();


    const position =
        document.getElementById(
            "position"
        ).value.trim();


    const resume =
        document.getElementById(
            "resume"
        ).value.trim();


    const jobDescription =
        document.getElementById(
            "jobDescription"
        ).value.trim();


    // ---------------------------------------------------------
    // Validation
    // ---------------------------------------------------------

    if (!candidateName) {

        showError(
            "Please enter the candidate name."
        );

        return;
    }


    if (!position) {

        showError(
            "Please enter the position."
        );

        return;
    }


    if (!resume) {

        showError(
            "Please enter the candidate resume."
        );

        return;
    }


    if (!jobDescription) {

        showError(
            "Please enter the job description."
        );

        return;
    }


    hideError();


    // ---------------------------------------------------------
    // UI Loading
    // ---------------------------------------------------------

    const button =
        document.getElementById(
            "analyzeButton"
        );


    const buttonText =
        document.getElementById(
            "buttonText"
        );


    const buttonIcon =
        document.getElementById(
            "buttonIcon"
        );


    button.disabled = true;

    buttonText.textContent =
        "Analyzing...";

    buttonIcon.textContent =
        "⏳";


    document
        .getElementById("loading")
        .classList.remove("hidden");


    document
        .getElementById("results")
        .classList.add("hidden");


    // ---------------------------------------------------------
    // Loading messages
    // ---------------------------------------------------------

    const loadingText =
        document.getElementById(
            "loadingText"
        );


    loadingText.textContent =
        "Analyzing candidate resume...";


    const messages = [

        "Analyzing candidate resume...",

        "Analyzing job requirements...",

        "Matching candidate skills...",

        "Retrieving HR knowledge using RAG...",

        "Generating interview questions...",

        "Groq cloud AI agent is preparing analysis..."

    ];


    let messageIndex = 0;


    const messageTimer =
        setInterval(() => {

            if (
                messageIndex <
                messages.length - 1
            ) {

                messageIndex++;

                loadingText.textContent =
                    messages[messageIndex];

            }

        }, 1800);


    // ---------------------------------------------------------
    // Send request to Flask
    // ---------------------------------------------------------

    try {

        const response =
            await fetch(
                "/analyze",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        candidate_name:
                            candidateName,

                        position:
                            position,

                        resume:
                            resume,

                        job_description:
                            jobDescription

                    })

                }
            );


        const data =
            await response.json();


        clearInterval(
            messageTimer
        );


        // -----------------------------------------------------
        // Handle error
        // -----------------------------------------------------

        if (!response.ok ||
            !data.success) {

            throw new Error(
                data.error ||
                "Analysis failed."
            );

        }


        // -----------------------------------------------------
        // Display results
        // -----------------------------------------------------

        displayResults(data);


    }
    catch (error) {

        clearInterval(
            messageTimer
        );


        showError(
            error.message
        );

    }
    finally {

        document
            .getElementById("loading")
            .classList.add("hidden");


        button.disabled = false;

        buttonText.textContent =
            "Analyze Candidate";

        buttonIcon.textContent =
            "✨";

    }

}


// =============================================================
// DISPLAY RESULTS
// =============================================================

function displayResults(data) {

    // ---------------------------------------------------------
    // Candidate
    // ---------------------------------------------------------

    document.getElementById(
        "resultCandidate"
    ).textContent =
        data.candidate_name;


    document.getElementById(
        "resultPosition"
    ).textContent =
        data.position;


    // ---------------------------------------------------------
    // Score
    // ---------------------------------------------------------

    const score =
        Number(
            data.match_score
        );


    document.getElementById(
        "matchScore"
    ).textContent =
        score.toFixed(1) + "%";


    document.getElementById(
        "scoreProgress"
    ).style.width =
        Math.min(score, 100) + "%";


    // ---------------------------------------------------------
    // Counts
    // ---------------------------------------------------------

    document.getElementById(
        "resumeSkillCount"
    ).textContent =
        data.resume_skills.length;


    document.getElementById(
        "matchingCount"
    ).textContent =
        data.matching_skills.length;


    document.getElementById(
        "missingCount"
    ).textContent =
        data.missing_skills.length;


    // ---------------------------------------------------------
    // Matching Skills
    // ---------------------------------------------------------

    renderSkills(
        "matchingSkills",
        data.matching_skills,
        "matching"
    );


    // ---------------------------------------------------------
    // Missing Skills
    // ---------------------------------------------------------

    renderSkills(
        "missingSkills",
        data.missing_skills,
        "missing"
    );


    // ---------------------------------------------------------
    // Resume Skills
    // ---------------------------------------------------------

    renderSkills(
        "resumeSkills",
        data.resume_skills,
        "matching"
    );


    // ---------------------------------------------------------
    // Job Skills
    // ---------------------------------------------------------

    renderSkills(
        "jobSkills",
        data.job_skills,
        "missing"
    );


    // ---------------------------------------------------------
    // AI Analysis
    // ---------------------------------------------------------

    document.getElementById(
        "finalAnswer"
    ).textContent =
        data.final_answer;


    // ---------------------------------------------------------
    // Interview Questions
    // ---------------------------------------------------------

    renderQuestions(
        data.interview_questions
    );


    // ---------------------------------------------------------
    // RAG
    // ---------------------------------------------------------

    document.getElementById(
        "ragKnowledge"
    ).textContent =
        data.retrieved_knowledge;


    // ---------------------------------------------------------
    // Show results
    // ---------------------------------------------------------

    document
        .getElementById("results")
        .classList.remove("hidden");


    // Scroll to results

    document
        .getElementById("results")
        .scrollIntoView({
            behavior: "smooth"
        });

}


// =============================================================
// RENDER SKILLS
// =============================================================

function renderSkills(
    elementId,
    skills,
    type
) {

    const container =
        document.getElementById(
            elementId
        );


    container.innerHTML = "";


    if (
        !skills ||
        skills.length === 0
    ) {

        const empty =
            document.createElement(
                "span"
            );


        empty.className =
            "empty-message";


        empty.textContent =
            "No skills detected.";


        container.appendChild(
            empty
        );


        return;

    }


    skills.forEach(
        function(skill) {

            const pill =
                document.createElement(
                    "span"
                );


            pill.className =
                type === "missing"
                    ? "missing-pill"
                    : "skill-pill";


            pill.textContent =
                skill;


            container.appendChild(
                pill
            );

        }
    );

}


// =============================================================
// RENDER QUESTIONS
// =============================================================

function renderQuestions(
    questions
) {

    const container =
        document.getElementById(
            "interviewQuestions"
        );


    container.innerHTML = "";


    if (
        !questions ||
        questions.length === 0
    ) {

        container.textContent =
            "No interview questions generated.";

        return;

    }


    questions.forEach(
        function(question, index) {

            const questionDiv =
                document.createElement(
                    "div"
                );


            questionDiv.className =
                "question";


            const number =
                document.createElement(
                    "span"
                );


            number.className =
                "question-number";


            number.textContent =
                "Q" + (index + 1);


            const text =
                document.createElement(
                    "span"
                );


            text.textContent =
                question;


            questionDiv.appendChild(
                number
            );


            questionDiv.appendChild(
                text
            );


            container.appendChild(
                questionDiv
            );

        }
    );

}


// =============================================================
// TABS
// =============================================================

function showTab(
    tabId,
    button
) {

    const contents =
        document.querySelectorAll(
            ".tab-content"
        );


    contents.forEach(
        function(content) {

            content.classList.remove(
                "active"
            );

        }
    );


    const buttons =
        document.querySelectorAll(
            ".tab-button"
        );


    buttons.forEach(
        function(btn) {

            btn.classList.remove(
                "active"
            );

        }
    );


    document
        .getElementById(tabId)
        .classList.add("active");


    button.classList.add(
        "active"
    );

}


// =============================================================
// ERROR
// =============================================================

function showError(
    message
) {

    const box =
        document.getElementById(
            "errorBox"
        );


    box.textContent =
        "⚠️ " + message;


    box.classList.remove(
        "hidden"
    );


    box.scrollIntoView({
        behavior: "smooth"
    });

}


function hideError() {

    document
        .getElementById("errorBox")
        .classList.add("hidden");

}


// =============================================================
// NEW ANALYSIS
// =============================================================

function newAnalysis() {

    document.getElementById(
        "candidateName"
    ).value = "";


    document.getElementById(
        "position"
    ).value = "";


    document.getElementById(
        "resume"
    ).value = "";


    document.getElementById(
        "jobDescription"
    ).value = "";


    document
        .getElementById("results")
        .classList.add("hidden");


    hideError();


    window.scrollTo({

        top: 0,

        behavior: "smooth"

    });

}

// SIDEBAR NAVIGATION

function navigateSection(sectionId, clickedButton) {

    // Update active sidebar button
    document.querySelectorAll(".sidebar-item").forEach(item => {
        item.classList.remove("active");
    });

    clickedButton.classList.add("active");

    // Check whether candidate analysis is completed
    const results = document.getElementById("results");

    if (
        sectionId !== "screening" &&
        results.classList.contains("hidden")
    ) {
        alert("Please analyze a candidate first!");
        return;
    }

    // Candidate Screening
    if (sectionId === "screening") {
        document.getElementById("screening").scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
        return;
    }

    // Skill Matching
    if (sectionId === "skillMatching") {
        document.getElementById("skillMatching").scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
        return;
    }

    // Interview Questions
    if (sectionId === "interviewQuestions") {

        const questionButton = document.querySelector(
            '.tab-button[onclick*="questions"]'
        );

        showTab("questions", questionButton);

        document.getElementById("questions").scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    }
}
