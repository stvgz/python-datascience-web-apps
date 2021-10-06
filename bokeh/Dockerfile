FROM python:3.7.6-slim

LABEL Auther="stvgz"

COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

EXPOSE 7860

CMD ["bokeh", "serve", "example_bokeh.py" ]


# docker build -t bokeh . && docker run -d bokeh 