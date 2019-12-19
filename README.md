# Logo Removal Project
Input an image with an FPT Logo on it, remove the logo and return new image with natural background replacing the logo

# TODO list:
* ~Test drawing function (util.py)~ DONE
* ~Design confidence score~ DONE
* ~Write logo auto detect function (util.py)~ DONE
* Return function of server.py
  * For now it just yield images over time. Should upgrade this function to yield iteration, match rate... to apply for progress bar
  * Check memory leak
* Dev front end
  * ~Just simple front end~ DONE
  * Re-design web page
  * Add descriptions for method explanation
  * Design user-oriented process flow