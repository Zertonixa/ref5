FROM python:3.9

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

# RUN chmod +x ./docker_scripts/alembic.sh

# CMD ./docker_scripts/alembic.sh && uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

CMD alembic upgrade head && uvicorn src.main:app --reload