# nike-stock-monitor
Nike SNKRS monitor

## Run Locally

Clone the project

```bash
  git clone https://github.com/niewiemczego/nike-stock-monitor
```

Go to the project directory

```bash
  cd nike-stock-monitor
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Open `example_runner.py` and add/edit/remove countries and webhook urls from monitors dict. 
Also if you want to change webhook footer/name etc, you can do it in webhook.py file.

## Supported Countires List
In countries.py file you can check if your country is available to be runned. If your country is not located in the file then most likely it uses different nike API which will be added soon...

## Image
<img width="527" alt="Screenshot 2022-09-06 at 22 39 48" src="https://user-images.githubusercontent.com/50675404/188733796-789dcc86-0b7c-4950-a6c0-449c6282b560.png">

## License
[MIT](https://choosealicense.com/licenses/mit/)
