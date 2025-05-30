import streamlit as st
import json
from utilities.gpt import chat_gpt
from utilities.helpers import create_docx_document

def generate_executive_summary(context):
    """
    Generate a concise executive summary based on the provided Action or Behavior Analysis data.
    The summary is tailored to high-level decision makers.
    """
    with st.spinner("Generating executive summary..."):
        prompt = (
            "Based on the following Action or Behavior Analysis data, generate a concise executive summary that synthesizes the key insights, findings, and potential next steps. "
            "The executive summary should be clear, high-level, and suitable for presentation to senior decision makers. "
            "Return only the summary as plain text.\n\n"
            f"Data:\n{context}"
        )
        system_msg = {"role": "system", "content": "You are an expert analyst in behavior analysis."}
        user_msg = {"role": "user", "content": prompt}
        summary = chat_gpt([system_msg, user_msg], model="gpt-4o-mini")
        return summary.strip()

def generate_recommendations(context):
    """
    Generate a numbered list of actionable recommendations based on the provided Action or Behavior Analysis data.
    """
    with st.spinner("Generating recommendations..."):
        prompt = (
            "Based on the following Action or Behavior Analysis data, please provide a list of actionable recommendations that address any identified gaps, challenges, or opportunities for intervention. "
            "Each recommendation should be clear, specific, and prioritized if applicable. "
            "Return the answer as a numbered list in plain text.\n\n"
            f"Data:\n{context}"
        )
        system_msg = {"role": "system", "content": "You are an expert strategic analyst focused on delivering actionable recommendations."}
        user_msg = {"role": "user", "content": prompt}
        recommendations = chat_gpt([system_msg, user_msg], model="gpt-4o-mini")
        return recommendations.strip()

def behavior_analysis_page():
    # Initialize session state keys to avoid KeyErrors.
    if "behavior_questions" not in st.session_state:
        st.session_state["behavior_questions"] = []
    
    st.markdown(
        """
        This template builds upon the latest doctrine **TM 3-53.11 Influence Process Activity: Target Audience Analysis**.
        
        Provide an in-depth analysis of a specific behavior, map out its timeline, and identify gaps, requirements, and implications using the COM‑B framework.
        """
    )

    # Sidebar help
    st.sidebar.title("Quick Help")
    st.sidebar.info(
        "Complete each section by entering data or clicking the 'Recommend' buttons for GPT suggestions. "
        "The form is organized into sections to help you capture basic details, analyze COM‑B determinants, "
        "build a timeline, and consider stakeholders and implications."
    )

    with st.expander("Template Instructions", expanded=False):
        st.markdown(
            """
            **Purpose:**  
            Provide a detailed analysis of a behavior – focusing on its requirements (capability, opportunity, motivation) and implications – and map out a timeline to identify gaps and opportunities for intervention.
            
            **How To Use:**  
            1. Replace placeholders with your specific information.
            2. Enter data in each section. Use the recommendation buttons to auto-populate fields with expert COM‑B–informed suggestions.
            3. Generate analytical questions, draft answers, and produce a comprehensive report.
            """
        )

    # Define field metadata (label, GPT prompt, input type)
    field_info = {
        # Basic Info
        "objective_effect": {
            "label": "Planner's Objective or Effect",
            "prompt": "Describe your objective as a planner. What effect or outcome are you trying to achieve? The target behavior you'll analyze should be an action that others would take that would help achieve this objective.",
            "type": "text",
            "no_ai_recommend": True  # Flag to prevent AI recommendations for this field
        },
        "action_behavior": {
            "label": "Target Action or Behavior (Critical Capability)",
            "prompt": "Describe the specific action or behavior (critical capability) you want others to take that would help achieve your objective. This behavior represents a critical capability that supports your objective. Provide context and clear examples in a concise summary.",
            "type": "text"
        },
        "location": {
            "label": "Location where the behavior occurs",
            "prompt": "Specify the location (city, region, or country) where the behavior is observed.",
            "type": "text"
        },
        # Critical Requirements Section
        "physical_capability": {
            "label": "Physical Capability Requirements",
            "prompt": "List the critical physical requirements (skills, strength, endurance) needed to perform this behavior/capability. These are potential vulnerability points. Format as numbered list: '#. [requirement]'.",
            "type": "textarea"
        },
        "psychological_capability": {
            "label": "Psychological Capability Requirements",
            "prompt": "List the critical psychological requirements (knowledge, skills, mental capacity) needed for this behavior/capability. These are potential vulnerability points. Format as numbered list: '#. [requirement]'.",
            "type": "textarea"
        },
        "physical_opportunity": {
            "label": "Physical Opportunity Requirements",
            "prompt": "List the critical physical environmental requirements (resources, time, location) needed for this behavior/capability. These are potential vulnerability points. Format as numbered list: '#. [requirement]'.",
            "type": "textarea"
        },
        "social_opportunity": {
            "label": "Social Opportunity Requirements",
            "prompt": "List the critical social and cultural requirements needed for this behavior/capability. These are potential vulnerability points. Format as numbered list: '#. [requirement]'.",
            "type": "textarea"
        },
        "reflective_motivation": {
            "label": "Reflective Motivation Requirements",
            "prompt": "List the critical conscious motivation requirements (goals, plans) needed for this behavior/capability. These are potential vulnerability points. Format as numbered list: '#. [requirement]'.",
            "type": "textarea"
        },
        "automatic_motivation": {
            "label": "Automatic Motivation Requirements",
            "prompt": "List the critical habitual/emotional requirements needed for this behavior/capability. These are potential vulnerability points. Format as numbered list: '#. [requirement]'.",
            "type": "textarea"
        },
        # Vulnerabilities Analysis
        "vulnerabilities": {
            "label": "Critical Vulnerabilities",
            "prompt": "Based on the requirements above, list the critical vulnerabilities that could be targeted to affect this behavior/capability. Prioritize vulnerabilities that affect multiple requirements or have cascading effects. Format as numbered list.",
            "type": "textarea"
        },
        # Supporting Analysis
        "behavior_breakdown": {
            "label": "Behavior/Capability Process Breakdown",
            "prompt": "Break down the chronological steps needed to execute this behavior/capability. This helps identify additional requirements and vulnerabilities. Include eligibility and prerequisites as a numbered list.",
            "type": "textarea"
        },
        "instances": {
            "label": "Historical Examples",
            "prompt": "Provide historical examples showing how this behavior/capability was executed or disrupted, focusing on requirements and vulnerabilities exploited.",
            "type": "textarea"
        },
        "obstacles": {
            "label": "Known Obstacles and Disruptions",
            "prompt": "List known obstacles or successful disruptions to this behavior/capability, highlighting which requirements or vulnerabilities were exploited.",
            "type": "textarea"
        },
        "associated_symbols": {
            "label": "Associated Symbols and Signals",
            "prompt": "Provide a numbered list of the symbolic objects—such as banners, placards, icons, or other visual cues—that not only represent the behavior but also carry deeper material and semiotic significance. Consider how these objects function as targets, components, or stimuli in contentious politics, reflecting both their tangible and symbolic roles. Provide a numbered list where each entry includes the symbol's name and a brief description of its symbolic relevance.",
            "type": "textarea"
        },
        # Implications & Outcomes
        "consequences": {
            "label": "Consequences and Outcomes",
            "prompt": "Discuss the outcomes (both positive and negative) of the behavior as a numbered list.",
            "type": "textarea"
        },
        "environmental_factors": {
            "label": "Environmental and Contextual Factors",
            "prompt": "Identify additional environmental or situational factors that influence the behavior, as a numbered list.",
            "type": "textarea"
        },
        "impact_strategies": {
            "label": "Strategies That Impacted the Behavior",
            "prompt": "List strategies or interventions that have increased or decreased the behavior, as a numbered list.",
            "type": "textarea"
        },
        # Stakeholders
        "primary_ta": {
            "label": "Potential Primary Target Audiences",
            "prompt": "Identify the primary target audiences most affected by this behavior.",
            "type": "textarea"
        },
        "secondary_ta": {
            "label": "Potential Secondary Target Audiences",
            "prompt": "Identify secondary audiences that may be influenced or engaged by the behavior.",
            "type": "textarea"
        },
        "engaging_actors": {
            "label": "Engaging Actors",
            "prompt": "List the individuals or groups actively engaging in the behavior.",
            "type": "textarea"
        },
        "beneficiaries": {
            "label": "Beneficiaries",
            "prompt": "Describe who benefits from the behavior, directly or indirectly.",
            "type": "textarea"
        },
        "harmed_parties": {
            "label": "Harmed Parties",
            "prompt": "List the parties that are negatively impacted by the behavior.",
            "type": "textarea"
        },
        "influencers": {
            "label": "Influencers and Stakeholders",
            "prompt": "Identify key influencers or stakeholders related to the behavior.",
            "type": "textarea"
        },
        "enablers": {
            "label": "Enablers and Supporters",
            "prompt": "Discuss the enablers that facilitate the behavior.",
            "type": "textarea"
        },
        "opposers": {
            "label": "Opposers and Detractors",
            "prompt": "Identify those who oppose or detract from the behavior.",
            "type": "textarea"
        },
        # Additional Considerations
        "additional_notes": {
            "label": "Additional Notes",
            "prompt": "Provide any extra observations or context.",
            "type": "textarea"
        },
        "cultural_considerations": {
            "label": "Cultural Considerations",
            "prompt": "Discuss cultural factors that influence the behavior.",
            "type": "textarea"
        },
        "legal_ethics": {
            "label": "Legal and Ethical Implications",
            "prompt": "Outline the legal and ethical implications relevant to the behavior.",
            "type": "textarea"
        }
    }

    # Reorganize sections to match COG analysis flow
    sections = {
        "Basic Info": ["objective_effect", "action_behavior", "location"],
        "Critical Requirements Analysis": ["physical_capability", "psychological_capability", "physical_opportunity", "social_opportunity", "reflective_motivation", "automatic_motivation"],
        "Vulnerabilities Analysis": ["vulnerabilities", "behavior_breakdown", "instances", "obstacles"],
        "Supporting Details": ["associated_symbols", "consequences", "environmental_factors", "impact_strategies"],
        "Stakeholders": ["primary_ta", "secondary_ta", "engaging_actors", "beneficiaries", "harmed_parties", "influencers", "enablers", "opposers"],
        "Additional Considerations": ["additional_notes", "cultural_considerations", "legal_ethics"]
    }

    analysis_details = {}

    # Render each section in an expander for a cleaner, form-like UI.
    for section, keys in sections.items():
        with st.expander(section, expanded=True):
            for key in keys:
                info = field_info[key]
                # Show the GPT recommendation button only if not explicitly disabled
                if not info.get("no_ai_recommend", False):
                    if st.button(f"Recommend for '{info['label']}'", key=f"btn_{key}"):
                        # Ensure mandatory "action_behavior" is provided for context.
                        if not st.session_state.get("action_behavior", "").strip():
                            st.warning("Please provide the Action or Behavior detail before generating recommendations.")
                        else:
                            with st.spinner(f"Generating recommendation for {info['label']}..."):
                                # Build a context string using key fields
                                context_parts = []
                                if st.session_state.get("action_behavior", "").strip():
                                    context_parts.append(f"{field_info['action_behavior']['label']}: {st.session_state.get('action_behavior')}")
                                if st.session_state.get("location", "").strip():
                                    context_parts.append(f"{field_info['location']['label']}: {st.session_state.get('location')}")
                                # Optionally add any other non-empty field (except the current one)
                                for cf, val in st.session_state.items():
                                    if cf in field_info and cf not in ["action_behavior", "location", key]:
                                        if isinstance(val, str) and val.strip():
                                            context_parts.append(f"{field_info[cf]['label']}: {val}")
                                context_str = "\n".join(context_parts) if context_parts else "No additional context provided."
                                full_prompt = (
                                    f"Using the context below:\n{context_str}\n\n"
                                    f"Now, please provide a suggestion for the '{info['label']}' field. {info['prompt']}"
                                )
                                system_msg = {"role": "system", "content": "You are an expert analyst in behavior analysis using the COM‑B framework."}
                                user_msg = {"role": "user", "content": full_prompt}
                                suggestion = chat_gpt([system_msg, user_msg], model="gpt-4o-mini")
                                st.session_state[key] = suggestion.strip()
                                st.success(f"'{info['label']}' auto-populated.")
                                st.rerun
                # Render the input widget.
                if info["type"] == "text":
                    analysis_details[key] = st.text_input(
                        info["label"],
                        key=key,
                        value=st.session_state.get(key, ""),
                        help=info["prompt"]
                    )
                else:
                    analysis_details[key] = st.text_area(
                        info["label"],
                        key=key,
                        height=100,
                        value=st.session_state.get(key, ""),
                        help=info["prompt"]
                    )

    st.markdown("---")
    st.header("Step 1: Generate Analytical Questions")
    """
    The purpose of this step is to generate a list of analytical questions that help refine the understanding of the behavior, identify potential gaps (including in capability, opportunity, and motivation), and explore challenges.
    The questions should be specific to the behavior and the context in which it occurs.
    The questions should be in the format of INTEL RFIs (Request for Information) that are specific to the behavior, location, and the context in which it occurs.
    """
    if st.button("Generate Analysis Questions"):
        if not analysis_details["action_behavior"] or not analysis_details["location"]:
            st.warning("Please provide at least the Action/Behavior and Location details before generating questions.")
        else:
            context = "\n".join(
                f"{field_info[key]['label']}: {analysis_details.get(key, '').strip()}"
                for key in field_info if analysis_details.get(key, "").strip()
            )
            prompt = (
                "Based on the Action or Behavior Analysis data provided below, please formulate exactly five analytical questions that deepen our understanding of the behavior, identify potential gaps (including those related to capability, opportunity, and motivation), and explore challenges and possible interventions.\n\n"
                "Requirements:\n"
                "1. Each question must begin with an interrogative word (e.g., 'what', 'how', 'why', etc.).\n"
                "2. The questions should be clear, concise, and directly related to the data.\n"
                "3. Do not include any additional commentary, explanations, or formatting.\n"
                "4. Return your answer strictly as a JSON array of strings (e.g., [\"Question 1\", \"Question 2\", ...]).\n\n"
                f"Data:\n{context}"
            )
            system_msg = {"role": "system", "content": "You are a strategic analyst specializing in behavior analysis using COM‑B."}
            user_msg = {"role": "user", "content": prompt}
            response = chat_gpt([system_msg, user_msg], model="gpt-4o-mini")
            
            # Clean and validate the response.
            cleaned_response = response.strip()
            if not cleaned_response:
                st.error("Received empty response from GPT.")
            else:
                # Optionally remove markdown formatting if present.
                if cleaned_response.startswith("```") and cleaned_response.endswith("```"):
                    cleaned_response = cleaned_response.strip("```").strip()

                # Remove an optional 'json' prefix if present.
                if cleaned_response.lower().startswith("json"):
                    cleaned_response = cleaned_response[len("json"):].strip()

                try:
                    questions = json.loads(cleaned_response)
                    st.session_state["behavior_questions"] = questions
                    st.success("Analytical questions generated successfully!")
                except Exception as e:
                    st.error(f"Error parsing questions from AI response: {e}")
                    st.write("Raw GPT Response:", cleaned_response)  # Debug the raw response.

    questions_list = st.session_state.get("behavior_questions", [])
    if questions_list:
        st.header("Analysis Questions and Answers")
        for idx, question in enumerate(questions_list, start=1):
            st.subheader(f"Question {idx}:")
            st.write(question)
            answer_key = f"behavior_answer_{idx}"
            st.text_area(
                f"Your answer for Question {idx}:",
                key=answer_key,
                height=100,
                value=st.session_state.get(answer_key, "")
            )
            if st.button(f"Suggest Answer for Question {idx}", key=f"suggest_btn_{idx}"):
                with st.spinner(f"Generating answer suggestion for Question {idx}..."):
                    suggestion_prompt = (
                        "Based on the following Action or Behavior Analysis data and the question provided, generate a draft answer that is clear and actionable. "
                        "Return only the answer with no additional commentary.\n\n"
                        "Data:\n" +
                        "\n".join(
                            f"{field_info[key]['label']}: {analysis_details.get(key, '').strip()}"
                            for key in field_info if analysis_details.get(key, "").strip()
                        ) +
                        f"\n\nQuestion: {question}"
                    )
                    system_msg = {"role": "system", "content": "You are an expert analyst in behavior analysis."}
                    user_msg = {"role": "user", "content": suggestion_prompt}
                    suggestion = chat_gpt([system_msg, user_msg], model="gpt-4o-mini")
                    st.session_state[f"behavior_answer_{idx}"] = suggestion.strip()
                    st.success(f"Answer for Question {idx} auto-populated.")
                    st.rerun

    st.markdown("---")
    st.header("Step 2: Generate Comprehensive Analysis Report")
    if st.button("Generate Analysis Report"):
        report_context = "Action or Behavior Analysis Data:\n"
        for key in field_info:
            value = analysis_details.get(key, "").strip()
            if value:
                report_context += f"{field_info[key]['label']}: {value}\n"
        if questions_list:
            report_context += "\nAnalysis Q&A:\n"
            for idx, question in enumerate(questions_list, start=1):
                answer = st.session_state.get(f"behavior_answer_{idx}", "")
                report_context += f"Q{idx}: {question}\nA{idx}: {answer}\n"
        
        report_prompt = (
            "Based on the following Action or Behavior Analysis data and the corresponding Q&A, generate a comprehensive report that summarizes "
            "the key insights, highlights potential gaps (including in capability, opportunity, and motivation), and provides recommendations for further action. "
            "Return the report as plain text.\n\n"
            f"{report_context}"
        )
        system_msg = {"role": "system", "content": "You are a strategic behavior analyst."}
        user_msg = {"role": "user", "content": report_prompt}
        report = chat_gpt([system_msg, user_msg], model="gpt-4o-mini")
        st.subheader("Analysis Report")
        st.text_area("Generated Report", value=report, height=300)
        st.download_button("Download Report as Text", report, file_name="behavior_analysis_report.txt", mime="text/plain")
        st.session_state["report_context"] = report_context  # Save for export

    st.markdown("---")
    st.subheader("Export Analysis")
    title_doc = st.text_input("Enter export file name for behavior analysis", "behavior_analysis")
    if st.button("Export Behavior Analysis as DOCX Document"):
        if "report_context" not in st.session_state or "behavior_questions" not in st.session_state:
            st.error("Please generate the analysis report before exporting.")
        else:
            # Extract the behavior summary and format it for the file name and title
            behavior_summary = analysis_details.get("action_behavior", "").strip()
            behavior_summary_filename = behavior_summary.replace(" ", "_") # Replace spaces with underscores
            behavior_summary_title = behavior_summary  # Keep spaces for the document title

            # Ensure report_context exists
            report_context = st.session_state["report_context"]
            
            # Generate executive summary and recommendations to include as the first pages.
            executive_summary = generate_executive_summary(report_context)
            recommendations_list = generate_recommendations(report_context)

            # Organize sections with the executive summary and recommendations as the first pages.
            sections = {
                "Executive Summary": executive_summary,
                "Recommendations": recommendations_list,
                f"Action or Behavior Analysis Data - {behavior_summary_title}": report_context,
                "Analysis Questions and Answers": "\n".join(
                    f"Q{idx}: {question}\nA{idx}: {st.session_state.get(f'behavior_answer_{idx}', '')}"
                    for idx, question in enumerate(st.session_state["behavior_questions"], start=1)
                ),
                "Analysis Report": report_context
            }
            docx_file = create_docx_document(f"{title_doc}-{behavior_summary_filename}", sections)
            st.download_button(
                label="Download DOCX",
                data=docx_file,
                file_name=f"{title_doc}-{behavior_summary_filename}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

if __name__ == "__main__":
    behavior_analysis_page()