from flask import Flask, render_template, request, jsonify

# # Import the graph from your existing app.py
# from app import graph


# app = Flask(__name__)


# # =============================================================
# # HOME PAGE
# # =============================================================

# @app.route("/")
# def home():
#     return render_template("index.html")


# # =============================================================
# # ANALYZE CANDIDATE
# # =============================================================

# @app.route("/analyze", methods=["POST"])
# def analyze():

#     try:

#         data = request.get_json()

#         candidate_name = data.get(
#             "candidate_name",
#             ""
#         ).strip()

#         position = data.get(
#             "position",
#             ""
#         ).strip()

#         resume = data.get(
#             "resume",
#             ""
#         ).strip()

#         job_description = data.get(
#             "job_description",
#             ""
#         ).strip()


#         # -----------------------------------------------------
#         # Validation
#         # -----------------------------------------------------

#         if not candidate_name:

#             return jsonify({
#                 "success": False,
#                 "error": "Please enter the candidate name."
#             }), 400


#         if not position:

#             return jsonify({
#                 "success": False,
#                 "error": "Please enter the position."
#             }), 400


#         if not resume:

#             return jsonify({
#                 "success": False,
#                 "error": "Please enter the candidate resume."
#             }), 400


#         if not job_description:

#             return jsonify({
#                 "success": False,
#                 "error": "Please enter the job description."
#             }), 400


#         # -----------------------------------------------------
#         # Run YOUR existing LangGraph
#         # -----------------------------------------------------

#         result = graph.invoke({

#             "resume": resume,

#             "job_description": job_description,

#             "resume_skills": [],

#             "job_skills": [],

#             "matching_skills": [],

#             "missing_skills": [],

#             "match_score": 0,

#             "retrieved_knowledge": "",

#             "interview_questions": [],

#             "final_answer": ""

#         })


#         # -----------------------------------------------------
#         # Send result to frontend
#         # -----------------------------------------------------

#         return jsonify({

#             "success": True,

#             "candidate_name": candidate_name,

#             "position": position,

#             "resume_skills":
#                 result["resume_skills"],

#             "job_skills":
#                 result["job_skills"],

#             "matching_skills":
#                 result["matching_skills"],

#             "missing_skills":
#                 result["missing_skills"],

#             "match_score":
#                 result["match_score"],

#             "retrieved_knowledge":
#                 result["retrieved_knowledge"],

#             "interview_questions":
#                 result["interview_questions"],

#             "final_answer":
#                 result["final_answer"]

#         })


#     except Exception as e:

#         print("ERROR:", e)

#         return jsonify({

#             "success": False,

#             "error": str(e)

#         }), 500


# # =============================================================
# # RUN SERVER
# # =============================================================

# if __name__ == "__main__":

#     app.run(
#         host="127.0.0.1",
#         port=5000,
#         debug=True
#     )
import os
from flask import Flask, render_template, request, jsonify
from app import graph

app = Flask(__name__)


# =============================================================
# HOME PAGE
# =============================================================

@app.route("/")
def home():
    return render_template("index.html")


# =============================================================
# HEALTH CHECK
# =============================================================

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "success": True,
        "message": "AI HR Recruitment Assistant server is running.",
        "model_provider": "Groq cloud",
        "model_configured": bool(os.getenv("GROQ_API_KEY"))
    })


# =============================================================
# ANALYZE CANDIDATE
# =============================================================

@app.route("/analyze", methods=["POST"])
def analyze():

    try:
        # ---------------------------------------------------------
        # Read JSON
        # ---------------------------------------------------------

        data = request.get_json(silent=True)

        if data is None:
            return jsonify({
                "success": False,
                "error": "Invalid request. JSON data was not received."
            }), 400

        # ---------------------------------------------------------
        # Get input values
        # ---------------------------------------------------------

        candidate_name = str(
            data.get("candidate_name", "")
        ).strip()

        position = str(
            data.get("position", "")
        ).strip()

        resume = str(
            data.get("resume", "")
        ).strip()

        job_description = str(
            data.get("job_description", "")
        ).strip()

        # ---------------------------------------------------------
        # Validation
        # ---------------------------------------------------------

        if not candidate_name:
            return jsonify({
                "success": False,
                "error": "Please enter the candidate name."
            }), 400

        if not position:
            return jsonify({
                "success": False,
                "error": "Please enter the position."
            }), 400

        if not resume:
            return jsonify({
                "success": False,
                "error": "Please enter the candidate resume."
            }), 400

        if not job_description:
            return jsonify({
                "success": False,
                "error": "Please enter the job description."
            }), 400

        # ---------------------------------------------------------
        # Initial LangGraph State
        # ---------------------------------------------------------

        initial_state = {
            "resume": resume,
            "job_description": job_description,

            "resume_skills": [],
            "job_skills": [],

            "matching_skills": [],
            "missing_skills": [],

            "match_score": 0.0,

            "retrieved_knowledge": "",

            "interview_questions": [],

            "final_answer": ""
        }

        # ---------------------------------------------------------
        # Run LangGraph
        # ---------------------------------------------------------

        print("\n" + "=" * 60)
        print("STARTING CANDIDATE ANALYSIS")
        print("=" * 60)

        print(f"Candidate : {candidate_name}")
        print(f"Position  : {position}")

        print("\nRunning LangGraph...")

        result = graph.invoke(initial_state)

        print("\nLangGraph completed successfully.")

        # ---------------------------------------------------------
        # Safely get results
        # ---------------------------------------------------------

        resume_skills = result.get(
            "resume_skills",
            []
        )

        job_skills = result.get(
            "job_skills",
            []
        )

        matching_skills = result.get(
            "matching_skills",
            []
        )

        missing_skills = result.get(
            "missing_skills",
            []
        )

        match_score = result.get(
            "match_score",
            0.0
        )

        retrieved_knowledge = result.get(
            "retrieved_knowledge",
            ""
        )

        interview_questions = result.get(
            "interview_questions",
            []
        )

        final_answer = result.get(
            "final_answer",
            ""
        )

        # ---------------------------------------------------------
        # Send response
        # ---------------------------------------------------------

        return jsonify({

            "success": True,

            "candidate_name": candidate_name,

            "position": position,

            "resume_skills": resume_skills,

            "job_skills": job_skills,

            "matching_skills": matching_skills,

            "missing_skills": missing_skills,

            "match_score": match_score,

            "retrieved_knowledge": retrieved_knowledge,

            "interview_questions": interview_questions,

            "final_answer": final_answer

        })


    # =============================================================
    # ERROR HANDLING
    # =============================================================

    except Exception as e:

        print("\n" + "=" * 60)
        print("ERROR DURING ANALYSIS")
        print("=" * 60)

        print(str(e))

        error_message = str(e)
        status_code = 503 if "GROQ_API_KEY is missing" in error_message else 500

        return jsonify({
            "success": False,
            "error": error_message
        }), status_code


# =============================================================
# RUN SERVER
# =============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 60)
    print("       AI HR RECRUITMENT ASSISTANT")
    print("=" * 60)
    print("\nServer starting...")
    print("Open: http://127.0.0.1:5000/")
    print("Health: http://127.0.0.1:5000/health")
    print("\n")

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true",
        threaded=True
    )