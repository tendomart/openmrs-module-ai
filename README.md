# openmrs-module-ai
Carries out AI Related Functions for OpenMRS
## Install All necessary softwares and dependency packages (Ubuntu Linux 24.04LTS lower versions should work well)
- Install python3, anaconda or pip
  -  Install the following project dependencies st, Ollama, AgentType, initialize_agent, Tool
- Install OpenJDK 11 & higher,  and Maven
- Install OpeNMRS SDK
- Install MySQL 8.X+
- Setup OpenMRS 3.0 Using SDK
- Install Ollama
- Pull qwen2.5-coder:1.5b model

  ## Setup
  - clone repo "git clone https://github.com/tendomart/openmrs-module-ai.git"
  - Setup virtual python environment follow  https://medium.com/@AgnesMbiti/creating-a-python-virtual-environment-on-ubuntu-22-04-5efc173ce655
  - install all project dependencies i.e st, Ollama, AgentType, initialize_agent, Tool
  - Pull LLM for powering agent using "ollama pull qwen2.5-coder:1.5b" or "ollama run qwen2.5-coder:1.5b". bigger models should work if you have necessary computing power
  - cd into project "cd /openmrs-module-ai/text2sql"
  - Make sure you edit the database connection properties in OpenmrsTextToSqlStreamlitUI.py to match your local or remote database
  - Run project using the command "streamlit run OpenmrsTextToSqlStreamlit.py"
  - The project should start at default port  http://localhost:8501 or  http://your-domain:8501
  - You will be provided with a simple UI to interact with the OpenMRS database using simple English.
 
    Congratulations ! you can now Query OpenMRS using AI

 
