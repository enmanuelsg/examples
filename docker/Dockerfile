FROM python:3.6

RUN pip install pyjokes
RUN echo "import pyjokes" > test.py
RUN echo "print(pyjokes.get_joke())" >> test.py

CMD ["python", "test.py"]