# Folder-archiving
Script to scrape folders for archiving.
script takes in a list of paths in a csv file, looks for project numbers in the foler names, compares them to a csv of active projects, then outputs s list of projects sorted by subfolder.
The search path CSV is a list of parent folders, which the script uses to search all the subfolders within that parent for projects. 
