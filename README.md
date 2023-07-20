# SonarDownloader

SonarDownloader is a Python application that allows you to download all the projects associated with a SonarQube API key. This tool utilizes the SonarQube API to retrieve project information and then proceeds to download the source code files.

## Requirements

Make sure you have Python installed on your system. SonarDownloader has been tested on Python 3.7 and above.

## Installation

### Clone this repository to your local system:
```shell
git clone https://github.com/your-username/sonar-downloader.git
cd sonar-downloader
```
### Install the necessary dependencies:
```shell
pip install -r requirements.txt
```

## Configuration

Before running SonarDownloader, you need to obtain a valid SonarQube API key. Follow the steps below:

Access your SonarQube server.
Log in with your credentials.
In the top-right corner, click on your profile picture and select "My Account".
In the left sidebar, click on "Security".
Click on the "Tokens" tab.
Enter a name for the token and set an expiration date (optional).
Click on "Generate".
Copy the generated token. This will be your SonarQube API key.
In the SonarDownloader directory, create a file named .env and add the API key as shown below:
SONAR_API_KEY=YOUR_API_KEY_HERE

Make sure to replace YOUR_API_KEY_HERE with the API key copied from SonarQube.

##Usage

After correctly configuring the API key, you can run SonarDownloader as follows:
```shell
python sonar_downloader.py
```

SonarDownloader will retrieve the list of projects associated with the provided API key and then proceed to download all projects into a directory called "projects". The source code files of each project will be stored in individual subdirectories within "projects".

## Contributing

If you encounter any issues or have suggestions for improving SonarDownloader, feel free to open an issue in this repository. Contributions are welcome too! Feel free to open a pull request with your enhancements.

## Disclaimer

This application is intended for personal use or for use on servers under your administration. Respect SonarQube's rights and usage policies when using this tool.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
