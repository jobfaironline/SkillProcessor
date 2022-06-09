FROM public.ecr.aws/lambda/python:3.8

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}

# Copy Skill database from project folder
COPY skill_db_relax_20.json .
COPY token_dist.json .

# Install the function's dependencies using file requirements.txt
# from your project folder.
COPY requirements.txt  .


RUN python3 -m pip install --upgrade pip

RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

RUN python3 -m spacy download en_core_web_sm

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]