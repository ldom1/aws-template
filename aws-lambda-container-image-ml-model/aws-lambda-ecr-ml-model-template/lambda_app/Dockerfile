FROM public.ecr.aws/lambda/python:3.8

COPY app.py requirements.txt svm_best_model.pkl ./

RUN python3.8 -m pip install -r requirements.txt -t .

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]
