# Developer Guidelines

## Requirements
1) Python 3.7 or above
2) Module Flask installed
3) Module SQLite3 installed
4) pyqrcode

        Any missing modules can be instaled via Pip with:

        pip install <module name>

## Running the Program for the first time
1) Install the database with the provided dbinstall script

        python dbinstall.py

2) Run flask using

        python main.py

3) Navigate to the given URL The default is:

        http://127.0.0.1:5000/

4) The default admin credentials are:

        Username: admin
        Password: admin

## Documentation

Documentation for using the system can be found in XXXX (TO BE COMPLETED). The user interface is by design easy to use and should be intuitive as to what you need to do to get a game up and running - any error messages (hopefully none) should be displayed out to tell you any errors you are causing when operating the system.

## Extending the program

To simply add new treasure hunts to the system, you can upload a new JSON config file to the system. An example file can be found in [../Technical-Documents/Configs/Computer_Science.json](../Technical-Documents/Configs/Computer_Science.json). The site will interpret this file provided it is in the right format and add the contents of it to the database - this game can then be ran from the GameKeeper section of the website.

The Treasure Hunt website is built in a way such that is can be easily extended for any scenario. The code follows an MVC framework which makes it easy to add new routes and thus new pages within the system. All files should contain a comment at the top detailing what the file does and each function contains a doc string to let you know what it does. The functions should be commented to a degree that means it is very easy to change and extend the system. A [./Coding Standards.md](./Coding Standards.md) is provided to give the standards that should be adhered to for the writing of new files.

Within the [../Product-Documents](../Product-Documents) directory, information including UI designs, flow diagrams for the transitions of the system and justifications of the languages used. Other information such as the FAQs and the Market Research may be useful for further reading. 

The website should be deployable to any Python environment which supports the requirements at the top of the page, the URLs are automatically configured by Flask when using the Routes directory. None of the folder or file names should be changed as this could lead to unspecified errors.