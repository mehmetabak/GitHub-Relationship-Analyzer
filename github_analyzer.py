import requests
import re
import json
import csv
from getpass import getpass
from colorama import init, Fore, Style

# Initialize colorama for colored terminal output
init(autoreset=True)

class GitHubAnalyzer:
    """
    A class to analyze GitHub user relationships, such as finding non-followers,
    fans, and handling unfollow actions.
    """
    API_URL = "https://api.github.com"

    def __init__(self, username):
        """
        Initializes the analyzer with a GitHub username.
        
        Args:
            username (str): The GitHub username to analyze.
        """
        if not self.validate_username(username):
            raise ValueError(f"Invalid GitHub username format: {username}")
            
        self.username = username
        self.session = requests.Session()
        self.session.headers.update({'Accept': 'application/vnd.github.v3+json'})
        
        # Caching results to avoid redundant API calls
        self._followers = None
        self._following = None

    @staticmethod
    def validate_username(username):
        """
        Validates the GitHub username format.
        GitHub usernames can only contain alphanumeric characters and hyphens,
        and cannot start or end with a hyphen. Length 1-39.
        """
        return re.match(r'^[a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,38}$', username)

    def _get_paginated_data(self, endpoint):
        """
        Fetches all pages for a given API endpoint.
        
        Args:
            endpoint (str): The API endpoint (e.g., f"/users/{self.username}/followers").
            
        Returns:
            list: A list of all items from all pages.
        """
        results = []
        page = 1
        while True:
            url = f"{self.API_URL}{endpoint}"
            params = {'per_page': 100, 'page': page}
            try:
                response = self.session.get(url, params=params)
                response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
                data = response.json()
                if not data:
                    break
                results.extend(data)
                page += 1
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    print(f"{Fore.RED}Error: User '{self.username}' not found on GitHub.")
                else:
                    print(f"{Fore.RED}An HTTP error occurred: {e}")
                return None # Indicate failure
        return results

    def get_followers(self):
        """
        Gets a list of all followers for the user.
        Results are cached.
        """
        if self._followers is None:
            print(f"{Fore.CYAN}Fetching followers for {self.username}...")
            data = self._get_paginated_data(f"/users/{self.username}/followers")
            if data is not None:
                self._followers = [user['login'] for user in data]
            else:
                self._followers = [] # Failed fetch
        return self._followers

    def get_following(self):
        """
        Gets a list of all users the user is following.
        Results are cached.
        """
        if self._following is None:
            print(f"{Fore.CYAN}Fetching users {self.username} is following...")
            data = self._get_paginated_data(f"/users/{self.username}/following")
            if data is not None:
                self._following = [user['login'] for user in data]
            else:
                self._following = [] # Failed fetch
        return self._following

    def find_non_followers(self):
        """
        Finds users that the main user follows but who do not follow back.
        
        Returns:
            list: A list of usernames who do not follow back.
        """
        following = self.get_following()
        followers = self.get_followers()
        # Ensure lists were fetched successfully
        if following is None or followers is None:
            return []
        return [user for user in following if user not in followers]

    def find_fans(self):
        """
        Finds users who follow the main user but are not followed back.
        
        Returns:
            list: A list of "fan" usernames.
        """
        following = self.get_following()
        followers = self.get_followers()
        # Ensure lists were fetched successfully
        if following is None or followers is None:
            return []
        return [user for user in followers if user not in following]

    @staticmethod
    def save_to_file(data, filename, file_format='txt'):
        """
        Saves a list of data to a file.
        
        Args:
            data (list): The list of strings to save.
            filename (str): The base name for the file.
            file_format (str): 'txt', 'csv', or 'json'.
        """
        full_filename = f"{filename}.{file_format}"
        try:
            if file_format == 'txt':
                with open(full_filename, 'w') as f:
                    for item in data:
                        f.write(f"{item}\n")
            elif file_format == 'csv':
                with open(full_filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['username'])  # Header
                    for item in data:
                        writer.writerow([item])
            elif file_format == 'json':
                with open(full_filename, 'w') as f:
                    json.dump(data, f, indent=4)
            else:
                print(f"{Fore.RED}Unsupported file format: {file_format}")
                return
                
            print(f"{Fore.GREEN}Successfully saved list to {full_filename}")
        except IOError as e:
            print(f"{Fore.RED}Error saving file: {e}")


def display_results(user_list, title):
    """
    Prints a formatted list of users.
    """
    if not user_list:
        print(f"{Fore.GREEN}All good! No users found in this category.")
        return

    print(Style.BRIGHT + Fore.YELLOW + f"\n--- {title} ({len(user_list)}) ---")
    for user in user_list:
        print(f"  - {user}")
    print(Style.BRIGHT + Fore.YELLOW + "------------------------\n")

def main():
    """
    Main function to run the interactive command-line interface.
    """
    print(Style.BRIGHT + Fore.MAGENTA + "Welcome to the GitHub Relationship Analyzer!")
    
    while True:
        username = input(Style.BRIGHT + "Enter your GitHub username: ")
        if GitHubAnalyzer.validate_username(username):
            break
        print(f"{Fore.RED}Invalid GitHub username. Please try again.")

    try:
        analyzer = GitHubAnalyzer(username)
    except ValueError as e:
        print(f"{Fore.RED}Error: {e}")
        return

    while True:
        print("\nWhat would you like to do?")
        print("  1. Find users you follow who DON'T follow you back")
        print("  2. Find users who follow you that you DON'T follow back (Fans)")
        print("  3. Exit")
        
        choice = input(Style.BRIGHT + "Enter your choice (1-3): ")

        if choice == '1':
            non_followers = analyzer.find_non_followers()
            display_results(non_followers, "Users Who Don't Follow You Back")
            if non_followers:
                if input("Save this list to a file? (y/n): ").lower() == 'y':
                    fmt = input("Enter format (txt, csv, json): ").lower()
                    analyzer.save_to_file(non_followers, f"{username}_non_followers", fmt)
        
        elif choice == '2':
            fans = analyzer.find_fans()
            display_results(fans, "Your 'Fans' (You Don't Follow Them Back)")
            if fans:
                if input("Save this list to a file? (y/n): ").lower() == 'y':
                    fmt = input("Enter format (txt, csv, json): ").lower()
                    analyzer.save_to_file(fans, f"{username}_fans", fmt)
                    
        elif choice == '3':
            print(f"{Fore.CYAN}Goodbye!")
            break
            
        else:
            print(f"{Fore.RED}Invalid choice. Please enter a number between 1 and 3.")


if __name__ == "__main__":
    # To run the script, you might need to install colorama:
    # pip install requests colorama
    main()
