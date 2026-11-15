# User Health State Layer

This folder houses your personal health data. It is pre-configured with zero-leak privacy controls:

- user_profile.template.yaml: The canonical blank questionnaire.
- user_profile.yaml: Your active health profile (pre-configured in .gitignore).
- lab_reports/: Drop-zone for raw PDF lab tests and photos (pre-configured in .gitignore).
- protocols/: Where your AI agent generates your personalized regimens (pre-configured in .gitignore).

### How to Initialize:
1. Copy the template to your active profile:
   cp profile/user_profile.template.yaml profile/user_profile.yaml

2. Enter your numbers directly in profile/user_profile.yaml, or drop your lab reports into profile/lab_reports/ and have your AI agent populate it automatically.
