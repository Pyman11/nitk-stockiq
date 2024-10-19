# NITK (StockIQ)

## Team Members (NITK)
1. Aadharsh Venkat (Ph: 9741529341)
2. Pradyun Diwakar (Ph: 9980041415)
3. Anirudh Nayak (Ph: 7338219470)

## Theme
4. Improving Banking, Integrated Apps

## Problem Statement
4.2 Real time equity analysis

## Overview
A fully functional, easy-to-use desktop application to help users track and analyze the stocks that they are interested in. The application provides insights on the current nature of the stock, recent relevant news about it, and factors affecting the stock price and a deep analysis into it, helping users in their investment decision processes.

The application provides a user-friendly homepage which allows the user to view simple data pertaining to the stock at a glance about the stocks they are interested in and general news about other stocks and the stock market in general, which may help users in choosing new stocks to invest in. Generative AI has been used to analyze in depth factors and provide insights on a particular stock.

A full video walkthrough is included in the link provided in VIDEO_WALKTHROUGH.txt.
Some additional feature explanations and financial terms used are explained in ANALYTICS.txt.

## Running the code (Necessary Dependencies and languages required)
(Steps necessary for execution)

Locate the TORUN.zip file.
All the files in the ZIP need to be downloaded and extracted into one folder. The entire solution is written in 100% python3. Hence, python3 will be required to run this code. The dependencies required must be installed using the pip module one by one in the command line:
```
pip install yfinance
pip install requests
pip install beautifulsoup4
pip install pandas
pip install matplotlib
pip install wxPython
pip install google-generativeai
```
The files on the repo must be extracted and saved in a folder.
For running the program, main.py must be run.
A window will appear after a few seconds, allowing the user to access the features of the software.

## References

1. The generative AI model used was Gemini through the python API. (https://ai.google.dev/gemini-api/docs/text-generation?lang=python)
2. WxPython was used to create the GUI framework. (https://docs.wxpython.org)
3. Matplotlib was used for plotting graphs (https://matplotlib.org/stable/index.html)
4. Yfinance was used to gather stock related data (https://pypi.org/project/yfinance)
