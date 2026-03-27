import requests
import sys

url = 'https://api.github.com'

def fetch_github_api(url):
    try:
        response = requests.get(url, headers={'Accept': 'application/vnd.github+json'}, timeout=10)
        if response.status_code == 404:
            print("Error: Resource not found")
            return
        elif response.status_code == 403:
            print("Rate limit exceeded. GitHub allows 60 requests/hour for unauthenticated users.")
            print("Wait a while and try again, or use a token for higher limits.")
            sys.exit(1)
        elif not response.ok:
            print(f"HTTP error {response.status_code}: {response.reason}")
            sys.exit(1)

        return response.json()

    except requests.exceptions.Timeout:
        print("Request timed out. GitHub took too long to respond. Try again later.")
        sys.exit(1)


def getUserName(userName):
    return fetch_github_api(f"{url}/users/{userName}")

def get_repos(userName):
    return fetch_github_api(f"{url}/users/{userName}/repos?per_page=100&sort=pushed")

def top_repos(repos, n=5):
    sorted_repos = sorted(repos, key=lambda r: r.get("stargazers_count", 0), reverse=True)
    return sorted_repos[:n]

def get_username():
    if len(sys.argv) >= 2:
        return sys.argv[1].strip()
    username = input("Enter GitHub username: ").strip()
    if not username:
        print("Username cannot be empty.")
        sys.exit(1)
    return username

def print_profile(user, repos):
    name      = user.get("name") or user.get("login")
    username  = user.get("login")
    bio       = user.get("bio") or "No bio provided."
    pub_repos = user.get("public_repos", 0)
    followers = user.get("followers", 0)
 
    print("\n" + "═" * 50)
    print(f"  {name}  (@{username})")
    print("═" * 50)
    print(f" Bio          : {bio}")
    print(f" Public Repos : {pub_repos}")
    print(f" Followers    : {followers}")
 
    top = top_repos(repos)
    if not top:
        print("\n No public repositories found.")
        print("═" * 50 + "\n")
        return
 
    print("\n Top 5 Repos by Stars:")
    print("  " + "─" * 46)
    for i, repo in enumerate(top, 1):
        name     = repo.get("name", "unknown")
        stars    = repo.get("stargazers_count", 0)
        language = repo.get("language") or "N/A"
        print(f"  {i}. {name}")
        print(f" {stars} stars  |  {language}")
    print("═" * 50 + "\n")


def main():
    username  = get_username()
    print(f"\n Fetching GitHub profile for: {username} ...")
 
    user  = getUserName(username)
    repos = get_repos(username)
 
    print_profile(user, repos)
 
 
if __name__ == "__main__":
    main()