# AudioAssembly

## A web application that allows users to upload audio/video files and receive a detailed report.

More description is available on the [DevPost](https://devpost.com/software/audio-assembly).

### How To Run

#### Setting Up The Environment

When you are in the command prompt, run the following three commands:

```
py -m venv env
py -m pip install --user virtualenv
.\env\Scripts\activate
```

> More description available here: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/.

#### Installing Dependancies

To install the dependencies, run the following command:

```
pip install -r requirements.txt
```

#### Setting Up Application

To set up the application, run the following three commands:

```
set FLASK_APP=AudioAssembly
set FLASK_ENV=development
set AAI_API_KEY=b64e2992b9364c3ab89ffeeca267438e
```

#### Running The Application

Finally, to run the application, run the following command:

```
flask run
```
