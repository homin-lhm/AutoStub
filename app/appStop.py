import requests
import yaml

with open(file='./config.yml', mode="r", encoding="utf-8") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


def app_stop():
    requests.post(url=f"http://127.0.0.1:{config['SERVER_PORT']}/shutdown", data={"password": "closePassword"})


if __name__ == '__main__':
    app_stop()
