# Canvas Downloader
Webscraper that automates the download of all module attachments from your Canvas courses.

## Requirements
Python, selenium, tqdm, geckodriver, unix system.

The program might not work on Windows machines.  Symlinks are used to change the download directory without changing the Firefox download directory preference.

## Setup
Install requirements.
Get the geckodriver if you do not have one already from here: https://github.com/mozilla/geckodriver/releases

Edit `config.py` with your preferences, including the geckodriver location, your school's Canvas url, and the course IDs of the courses that you want to download.  The course ID is just the numbers after courses/ in the url.

Edit `mimetypes.txt` with the mime types of the files that you want to download.  One line for each mime type.  Included already are pdf, docx, and pptx.

## Usage

`python main.py`

Then enter your login credentials in the selenium webdriver.  After the main Canvas page has loaded, press enter in the terminal and the program will download files to `./downloads`.

## Example tree output
```
downloads
├── 123456
│   ├── lecture10.pdf
│   ├── lecture11.pdf
│   ├── lecture12.pdf
│   ├── lecture13.pdf
│   ├── lecture14.pdf
│   ├── lecture15.pdf
│   ├── lecture1.pdf
│   ├── lecture2.pdf
│   ├── lecture3.pdf
│   ├── lecture4.pdf
│   ├── lecture5.pdf
│   ├── lecture6.pdf
│   ├── lecture7.pdf
│   ├── lecture8.pdf
│   ├── lecture9.pdf
│   ├── practice_review.pdf
│   └── practice_review_solutions.pdf
├── 234567
│   ├── lecture1.pdf
│   ├── lecture2.pdf
│   ├── lecture3.pdf
│   └── lecture4.pdf
├── geckodriver.log
├── log.txt
└── symlink -> 234567
```

