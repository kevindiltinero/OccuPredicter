import os
import time

if __name__ == "__main__":

    welcome = """
  _      __    __                    
 | | /| / /__ / /______  __ _  ___   
 | |/ |/ / -_) / __/ _ \/  ' \/ -_)  
 |__/|__/\__/_/\__/\___/_/_/_/\__/   
                __                   
               / /____               
              / __/ _ \              
   __ __      \__/\___/              
  / // /__ _______ _  ___  ___  __ __
 / _  / _ `/ __/  ' \/ _ \/ _ \/ // /
/_//_/\_,_/_/ /_/_/_/\___/_//_/\_, / 
                              /___/  
    """
    print welcome

    data = """
    

  ____        _          _____      _                  _   _             
 |  _ \  __ _| |_ __ _  | ____|_  _| |_ _ __ __ _  ___| |_(_) ___  _ __  
 | | | |/ _` | __/ _` | |  _| \ \/ / __| '__/ _` |/ __| __| |/ _ \| '_ \ 
 | |_| | (_| | || (_| | | |___ >  <| |_| | | (_| | (__| |_| | (_) | | | |
 |____/ \__,_|\__\__,_| |_____/_/\_|___|_|  \__,_|\___|\__|_|\___/|_| |_|
    """
    print data
    # Attempt to run all of the data extraction files
    try:
        execfile("./parser/ground_parser.py")
        execfile("./parser/timetable_parser.py")
        execfile("./parser/wifi_parser.py")

    # If an IOError is thrown, print the message and remove any files that were created during the process
    # Exit the program
    except IOError as e:
        print "ERROR: "+ e.message
        generated_files = os.listdir("./data/Cleaned_Data")
        for filename in generated_files:
            os.remove("./data/Cleaned_Data/"+filename)
        sys.exit(0)

    # Run the other parsers
    execfile("./parser/room_parser.py")
    execfile("./parser/modules.py")


    database = """


  ____        _        _                      ____       _               
 |  _ \  __ _| |_ __ _| |__   __ _ ___  ___  / ___|  ___| |_ _   _ _ __  
 | | | |/ _` | __/ _` | '_ \ / _` / __|/ _ \ \___ \ / _ \ __| | | | '_ \ 
 | |_| | (_| | || (_| | |_) | (_| \__ \  __/  ___) |  __/ |_| |_| | |_) |
 |____/ \__,_|\__\__,_|_.__/ \__,_|___/\___| |____/ \___|\__|\__,_| .__/ 
                                                                  |_|    
    """
    print database
    # Attempt to create the database
    try:
        execfile("./parser/db_create.py")

    # If the user does not want to overwrite an existing database of the same name, exit the program
    except IOError as e:
        print "ERROR: "+e.message+" Program exiting."
        generated_files = os.listdir("./data/Cleaned_Data")
        for filename in generated_files:
            os.remove("./data/Cleaned_Data/"+filename)
        sys.exit(0)

    execfile("./parser/db_insert.py")
    print "Setup complete!"


    model = """



  __  __           _      _    ____                           _   _             
 |  \/  | ___   __| | ___| |  / ___| ___ _ __   ___ _ __ __ _| |_(_) ___  _ __  
 | |\/| |/ _ \ / _` |/ _ \ | | |  _ / _ \ '_ \ / _ \ '__/ _` | __| |/ _ \| '_ \ 
 | |  | | (_) | (_| |  __/ | | |_| |  __/ | | |  __/ | | (_| | |_| | (_) | | | |
 |_|  |_|\___/ \__,_|\___|_|  \____|\___|_| |_|\___|_|  \__,_|\__|_|\___/|_| |_|
                                                                                
    """
    print model
    execfile("./Model/train.py")
