                                      Automated Snow Melting System
                                      
This repository contains the source files that are designed to perform IoT functionality for a raspberry pi controlled heat system. The goal
is to allow the users to remotely access their raspberry pi and start melting snow. The program files perform the following functions:
  1) Darksky.py
     This file contains the api that is requested for the current weather conditions. It returns a json data type. The data is appended 
     to a list and then returned to the main program. If for any reason the weather api doesn't respond or if the received coordinates are
     invalid, it returns back to the user page.
  2) App.py
     This is the main program file that combines the Flask backend and along with the integration of darksky file. Also, it stores all the data
     that is generated using a class that creates a table in a postgresql database. The backend is designed in a way that provides a 
     seamless experience to the user. 
  3) Templates folder
     The templates provide the front end code of the website. It contains css snippets from bootstrap and W3Schools. 
