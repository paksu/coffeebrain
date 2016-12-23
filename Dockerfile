FROM python:2.7.12

RUN pip install numpy==1.11.3 scipy==0.18.1 scikit-learn==0.18.1 scikit-learn==0.18.1 requests==2.12.4 Flask==0.12 Pillow==3.4.2

ADD . /

EXPOSE 5000

CMD ["python","web.py"]
