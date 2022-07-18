                 $$$$$$\    $$\                     $$\    $$\ 
                $$  __$$\   $$ |                    $$ |   $$ |
     $$$$$$\    $$ /  \__|  $$$$$$$\     $$$$$$\    $$ |   $$ |
    $$  __$$\   \$$$$$$\    $$  __$$\   $$  __$$\   $$ |   $$ |
    $$ |  \__|   \____$$\   $$ |  $$ |  $$$$$$$$ |  $$ |   $$ |
    $$ |        $$\   $$ |  $$ |  $$ |  $$   ____|  $$ |   $$ |
    $$ |        \$$$$$$  |  $$ |  $$ |  \$$$$$$$\   $$ |   $$ |
    \__|         \______/   \__|  \__|   \_______|  \__|   \__|
    

## Remotely access other computer's terminal via TCP connection

Installation:
  
  Clone this repository into a folder.
  Good practice is to add the folder to your PATH:
    
      $ export PATH="$PATH:/path/to/repo/bin/darwin"  # depending on 
      $ export PATH="$PATH:/path/to/repo/bin/linux"   # your own system 
      
Usage:
  
  Just cd into /path/to/repo/bin/yourOS and type
  
      $ ./rshell

  In some systems, you may need to get permission to execute

      $ sudo chmod +x rshell
      
  The CLI itself provides a full guide for rShell usage

      \..{|[<->_<'>]|}../
