# GitHub Relationship Analyzer

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mehmetabak/GitHub-Relationship-Analyzer/blob/main/github_analyzer.ipynb)

A powerful and user-friendly Python script to analyze your GitHub social connections. Find out who isn't following you back, discover your "fans," and manage your network more effectively.

## ✨ Features

-   **Find Non-Followers**: Get a list of users you follow who don't follow you back.
-   **Discover Your Fans**: Get a list of users who follow you, but you don't follow back.
-   **Interactive CLI**: A simple and clean command-line menu to navigate the tool's features.
-   **Handles Large Accounts**: Correctly fetches all followers/following, even for users with thousands of connections, thanks to full pagination support.
-   **Export Results**: Save the generated user lists to a file in `txt`, `csv`, or `json` format.
-   **User-Friendly Output**: Clean, colorful, and easy-to-read output in your terminal.
-   **No API Key Required**: Works with the public GitHub API without needing a personal access token for its core features.
-   **Input Validation**: Ensures you enter a valid GitHub username format before making API calls.

## 📸 Screenshot



## 🚀 Getting Started

### Prerequisites

-   Python 3.6+
-   `pip` package manager

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/mehmetabak/GitHub-Relationship-Analyzer.git
    cd YOUR_REPOSITORY
    ```

2.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```
    *(Note: The `requirements.txt` file should contain `requests` and `colorama`)*

### Usage

Run the script from your terminal:

```sh
python github_analyzer.py
```

The script will then prompt you to enter a GitHub username and will present you with an interactive menu of options.

## 📝 How It Works

The script uses the official GitHub REST API to fetch public follower and following data for a specified user.

1.  **Pagination**: It makes paginated requests to endpoints like `/users/{username}/followers`, ensuring all data is retrieved, not just the first page (a common limitation in simpler scripts).
2.  **Set Operations**: It converts the lists of followers and following into sets to efficiently find the differences between them:
    -   **Non-Followers**: `following` - `followers`
    -   **Fans**: `followers` - `following`
3.  **Caching**: To avoid making redundant API calls within a single session, the follower and following lists are cached in memory after the first fetch.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/mehmetabak/GitHub-Relationship-Analyzer/issues).

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
