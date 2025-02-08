import streamlit as st

def cog_analysis():
    st.title("COG Analysis")
    st.write("""
    Center of Gravity (COG) analysis is a method used to identify and analyze the primary sources of strength and vulnerabilities in a system or organization. This framework helps in understanding the critical factors that can influence the success or failure of a strategy or operation.
    """)

    st.header("Steps for COG Analysis")
    st.markdown("""
    1. **Identify the Objective**: Define the primary goal or objective of the analysis.
    2. **Determine the Critical Capabilities**: Identify the key capabilities that are essential for achieving the objective.
    3. **Identify the Critical Requirements**: Determine the resources and conditions necessary for the critical capabilities to function.
    4. **Identify the Critical Vulnerabilities**: Analyze the weaknesses or vulnerabilities that can be exploited to disrupt the critical capabilities.
    5. **Develop a Plan**: Create a plan to protect the critical capabilities and address the vulnerabilities.
    """)

    st.header("COG Analysis Framework")
    st.markdown("""
    | Step | Description |
    |------|-------------|
    | Identify the Objective | Define the primary goal or objective of the analysis. |
    | Determine the Critical Capabilities | Identify the key capabilities that are essential for achieving the objective. |
    | Identify the Critical Requirements | Determine the resources and conditions necessary for the critical capabilities to function. |
    | Identify the Critical Vulnerabilities | Analyze the weaknesses or vulnerabilities that can be exploited to disrupt the critical capabilities. |
    | Develop a Plan | Create a plan to protect the critical capabilities and address the vulnerabilities. |
    """)

    st.header("Example COG Analysis")
    st.markdown("""
    **Objective**: Improve the cybersecurity posture of an organization.

    **Critical Capabilities**:
    - Network security
    - Endpoint protection
    - Incident response

    **Critical Requirements**:
    - Skilled cybersecurity personnel
    - Advanced security tools and technologies
    - Effective communication channels

    **Critical Vulnerabilities**:
    - Lack of employee training
    - Outdated software and hardware
    - Insufficient incident response procedures

    **Plan**:
    - Conduct regular employee training sessions on cybersecurity best practices.
    - Upgrade software and hardware to the latest versions.
    - Develop and implement comprehensive incident response procedures.
    """)

if __name__ == "__main__":
    cog_analysis()
