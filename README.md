# h501-finalproject


## To setup the project to run locally. First clone and then: 
### With conda, activiate the packages listed in env_app.yml
conda env create -f env_app.yml
conda activate H501-finalproject



### To test this application run this command: 
CD to project
python -m streamlit run frontend/streamlit_app.py


### Commands if your env file already exists
conda env create -f env_app.yml
conda activate H501-finalproject

### command to update the requirements file which is NEEDED for streamlit hosting
pip freeze > requirements.txt


## PROD Environment URL: https://h501-finalproject.streamlit.app/
## TOON Environment URL: https://h501-finalproject-xstblhshf5njjr4pzqzcfm.streamlit.app/