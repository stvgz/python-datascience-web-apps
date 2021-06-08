FROM python:3.7.6-slim

LABEL Auther="stvgz"

COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

EXPOSE 7860

CMD [ 'python', 'example_gradio_simple.py' ]