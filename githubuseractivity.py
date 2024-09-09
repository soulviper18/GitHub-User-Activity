import sys
import urllib.request
import json

def fetch_github_activity(username):
    """Fetches recent GitHub activity for a given username."""
    url = f"https://api.github.com/users/{username}/events"
    
    try:
        # Make a GET request to fetch the user's events
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                display_activity(data)
            else:
                print(f"Failed to fetch data. Status Code: {response.status}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: GitHub user '{username}' not found.")
        else:
            print(f"Error: Unable to fetch data. HTTP Error Code: {e.code}")
    except urllib.error.URLError as e:
        print(f"Error: Unable to connect to GitHub API. Reason: {e.reason}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def display_activity(events):
    """Displays the fetched activity in a user-friendly format."""
    if not events:
        print("No recent activity found.")
        return

    for event in events[:10]:  # Display only the latest 10 events
        event_type = event.get("type")
        repo_name = event.get("repo", {}).get("name")
        if event_type == "PushEvent":
            commits_count = len(event.get("payload", {}).get("commits", []))
            print(f"Pushed {commits_count} commit(s) to {repo_name}")
        elif event_type == "IssuesEvent":
            action = event.get("payload", {}).get("action")
            print(f"{action.capitalize()} an issue in {repo_name}")
        elif event_type == "WatchEvent":
            print(f"Starred {repo_name}")
        elif event_type == "ForkEvent":
            print(f"Forked {repo_name}")
        else:
            print(f"{event_type} in {repo_name}")

def main():
    """Main function to accept command line arguments and fetch GitHub activity."""
    if len(sys.argv) != 2:
        print("Usage: github_activity <username>")
        sys.exit(1)

    username = sys.argv[1]
    fetch_github_activity(username)

if __name__ == "__main__":
    main()
