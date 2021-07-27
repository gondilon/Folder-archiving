import csv
import json
import os
import pandas as pd


def read_projects():
   market_list = []
   active_projects = pd.read_csv("data/active_projects.csv", delimiter=",", encoding="windows-1252", index_col=0,
                                 header=0, names=
                                 ["Project", "Legacy_Project", "Name", "Project_Manager", "Market"])

   project_nums = active_projects.index.to_list()
   fixed_project_nums = []
   for num in project_nums:
      split_num = num.split(".")
      fixed_project_nums.append(split_num[1]+"."+split_num[2])
   legacy_nums = [num for num in active_projects["Legacy_Project"].to_list() if type(num)!=float]
   legacy_nums.extend(fixed_project_nums)
   return legacy_nums

def paths_to_check(start):
   paths_to_check = []
   for sub_dirs in os.listdir(start):
      if "Dallas" in sub_dirs:
         pass
      else:
         if os.path.isdir(os.path.join(start, sub_dirs)):
            #print(sub_dirs)
            if sub_dirs.startswith("Project") or sub_dirs.startswith("Medical") or sub_dirs.startswith("Cyber"):
               pass
            else:
               paths_to_check.append(os.path.join(start, sub_dirs))

   return paths_to_check

def split_folder_name(folder,seperator):
   find_project_num = folder.split(seperator)
   try:
      project_num = float(find_project_num[0])
      return find_project_num[0]
   except ValueError:
      split_num = find_project_num[0].split("-")
      if len(split_num) == 2 and split_num[0][0].isdigit():
            return find_project_num[0]
      else:
         return None



def find_project_nums(paths, com=False):
   '''finds all inactive projects at the given path.'''
   projects = {}
   seps = [' ', '_', '-']
   for path in paths:
      try:
         for sub_dir in os.listdir(path):
               if os.path.isdir(os.path.join(path, sub_dir)):
                  for sep in seps:
                     project_number = split_folder_name(sub_dir, sep)

                     if project_number:
                        if "Technology" in path and not "COM" in path:
                           project_number = split_folder_name(project_number, "-")
                        projects[project_number] = os.path.join(path, sub_dir)
                        #print(project_number)
                        break
                     else:
                        pass

               else:
                  pass
      except PermissionError:
         print(path)
   return projects

def process_inactive_projects(inactive_list):
   '''Takes in the list of inactive projects and their file paths and creates a dict organized by market'''
   project_by_folder = {}
   file_groupings = ["Dallas","Hamden","Houston","Indianapolis","Kansas City", "Miami", "Philadelphia","Northbrook", "St.Louis", "Technology"]
   for item in file_groupings:
      project_by_folder[item] = [(project, path) for project, path in inactive_list.items() if item in path]
   return project_by_folder

def file_write(active, scrape):
   with open ("active_projects.csv", "w") as active_project:
      write_line = csv.writer(active_project)
      for project in active:
         write_line.writerow(project)
      active_project.close()
   with open ("Inactive_list.csv", "w") as inactive_file:
      writer = csv.writer(inactive_file)
      for key, value in scrape.items():
         writer.writerow([key, value])
      inactive_file.close()

def get_key(val, projects):
   for key,value in projects.items():
      if val == value:
         return key

def find_active(project_scrape):
   active =[]
   seps = [' ', '-']
   active_nums = read_projects()
   active_names = {}
   projects = project_scrape
   active_projects = pd.read_csv("data/active_projects.csv", delimiter=",", encoding="windows-1252", index_col=0,
                                 header=0, names=
                                 ["Project", "Legacy_Project", "Name", "Project_Manager", "Market"])
   project_names = active_projects['Name'].tolist()
   errors = []
   try:
      for project in projects.keys():
         if project in active_nums:
            if project not in active:
               active.append(project)
         else:
            for name in project_names:
               if project in name and name not in active_names.keys():
                     active_names[name] = project
   except TypeError as e:
      errors.append(e)
   print("errors ", len(errors))

   for item in active:
      removed = projects.pop(item, "Not found")
      #print(removed)
   project_names = projects.keys()
   updated_projects = {}
   drop_errors = []
   for name in active_names.keys():
      '''for sep in seps:
         key = split_folder_name(name, sep)
         if key:
            break
      removed = projects.pop(key, "not found")
      print(removed)'''


      try:
         for project in project_names:
            if project not in name:
               updated_projects[project] = projects[project]
      except TypeError as e:
         drop_errors.append(e)
   print("drop errors: ", len(drop_errors))


   return updated_projects

def main():
   starting_path = 'j:'
   com_starting_path = "J:\Technology\COMgroup"
   Dallas_starting_path = "J:\Dallas"
   #project_numbers = read_projects()
   check_paths = paths_to_check(starting_path)
   Dallas_check_paths = paths_to_check(Dallas_starting_path)
   com_check_paths = paths_to_check(com_starting_path)
   check_paths.extend(Dallas_check_paths)
   check_paths.extend(com_check_paths)
   project_scrape = find_project_nums(check_paths)
   print(len(project_scrape))
   inactive = find_active(project_scrape)
   print(len(inactive))
   sorted_by_folder = process_inactive_projects(inactive)
   #print(sorted_by_folder)
   for key, value in sorted_by_folder.items():
      with open(f"output/{key}.csv", "w", newline='') as sorted_files:
         write = csv.writer(sorted_files)
         title = f"Projects from the{key} Folder. \n"
         sorted_files.write(title)
         write.writerows(value)
   sort_scrape = process_inactive_projects(project_scrape)

   with open("output/Full_project_scrape.csv", "w", newline='') as full_scrape:
      writer = csv.writer(full_scrape)
      for project, path in sort_scrape.items():
         title = f"Projects from the {project} Folder. \n"
         full_scrape.write(title)
         writer.writerows(path)

if __name__ == "__main__":
   main()

