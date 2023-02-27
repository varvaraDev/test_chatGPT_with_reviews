### Test task by Welltory 

[description](https://docs.google.com/spreadsheets/d/1RpHXQgM1_1zIrLdbjM7HxpgfLNvDBWrqTZSeHd7CikA/edit#gid=2057762519)


### How to test by local

1. Clone this repo
2. Create virtualenv (python3.10)
   3. conda create -n welltory python=3.10 | conda activate welltory
   4. python -m venv welltory | source welltory/bin/activate
   5. Or pyenv, or what you use :) 
6. Run ``pip install -r requirements.txt``
7. Create .env file and put `OPENAI_API_KEY=<your_key>` from this [link](https://platform.openai.com/docs/quickstart/add-your-api-key)
7. Run python scripts
   8. ``python analyze_review_v1.py`` - this uis base realization by requirements of task
   9. ``python tests_and_improvments/analyze_review_v2.py`` - first iteration with pandas
   10. ``python tests_and_improvments/analyze_review_v3.py`` - refactoring pandas solution by me and chat GPT