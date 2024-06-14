import requests
from bs4 import BeautifulSoup
import os
import shutil
import random

# Function to create a folder
def create_folder(path):
    try:
        # Create the directory
        os.makedirs(path, exist_ok=True)
        print(f"Directory '{path}' created successfully")
    except OSError as error:
        print(f"Error creating directory '{path}': {error}")

# Function to extract all links from a webpage
def get_all_links(url):
    # Send a request to the webpage
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return []

    # Parse the webpage content
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all <a> tags
    a_tags = soup.find_all('img')
    # Extract the href attribute from each <a> tag
    links = [a.get('src') for a in a_tags if a.get('src')]

    return links

def read_file_to_array(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # Remove newline characters from each line and add to the array
            lines = [line.strip() for line in lines]
            lines = [line.lower() for line in lines]
            return lines
    except Exception as e:
        print(f"Error reading file: {e}")
        return []
    
def download_image(url, file_path):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            # Open a file in binary write mode and write the image content
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Image downloaded successfully to {file_path}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading image: {e}")


def list_empty_directories(root_dir):
    empty_dirs = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Check if the directory is empty
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)
    
    return empty_dirs


def delete_empty_directory(dir_path):
    try:
        os.rmdir(dir_path)
        print(f"Directory '{dir_path}' deleted successfully")
    except OSError as e:
        print(f"Error: {e.strerror} - {e.filename}")

def list_directories(root_dir):
    directories = []
    
    # Loop through the directory tree
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Add each directory path to the list
        for dirname in dirnames:
            directories.append(os.path.join(dirpath, dirname))
            
    return directories

def write_directories_to_file(directories, file_path):
    try:
        with open(file_path, 'w') as file:
            for directory in directories:
                file.write(directory + '\n')
        print(f"Directories written to {file_path} successfully")
    except Exception as e:
        print(f"Error writing to file: {e}")

def split_data(source_dir, train_dir, test_dir, split_ratio=0.8):
    # Create train and test directories if they don't exist
    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    
    # Iterate over each class in the source directory
    for class_name in os.listdir(source_dir):
        class_path = os.path.join(source_dir, class_name)
        if os.path.isdir(class_path):
            images = os.listdir(class_path)
            random.shuffle(images)
            
            # Calculate the split index
            split_index = int(len(images) * split_ratio)
            
            # Create class directories in train and test directories
            train_class_dir = os.path.join(train_dir, class_name)
            test_class_dir = os.path.join(test_dir, class_name)
            os.makedirs(train_class_dir, exist_ok=True)
            os.makedirs(test_class_dir, exist_ok=True)
            
            # Split the images into train and test sets
            train_images = images[:split_index]
            test_images = images[split_index:]
            
            # Move the images to the corresponding directories
            for image in train_images:
                shutil.move(os.path.join(class_path, image), os.path.join(train_class_dir, image))
            for image in test_images:
                shutil.move(os.path.join(class_path, image), os.path.join(test_class_dir, image))
    
    print(f"Data split into {train_dir} and {test_dir} successfully.")


def main():
    source_directory = 'data'
    train_directory = 'train'
    test_directory = 'test'
    split_ratio = 0.8

    split_data(source_directory, train_directory, test_directory, split_ratio)
    return
    # root_directory = '.'
    # directories = list_directories(root_directory)
    # directories = [direc.replace(".\\", "").replace("-images", "") for direc in directories]
    # print(directories[0])
    
    # file_path = 'classes.txt'
    # write_directories_to_file(directories, file_path)
    # return
    # Example usage
    # root_directory = '.'
    # empty_directories = list_empty_directories(root_directory)

    # print("Empty directories:")
    # for empty_dir in empty_directories:
    #     print(empty_dir)
    #     # delete_empty_directory(empty_dir)
    # return

    base_url = "https://dermnetnz.org"
    
    dlist = read_file_to_array("skin-diseaase.txt")
    for d in dlist:
        create_folder(d)
        l1 = get_all_links(base_url + "/images/" + d)
        l2 = get_all_links(base_url + "/topics/" + d)
        ml = l1 + l2
        for index, i in enumerate(ml):
            download_image(base_url+i, d + f"/{index}.jpg")
    print("done")

# Example usage
url = 'https://dermnetnz.org/images/acne-affecting-the-back-images'
main()
