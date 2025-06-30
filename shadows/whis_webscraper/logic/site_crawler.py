def scrape_sources():
    # Fake list for now — parse real markdown or JSON feeds later
    return [
        {
            "title": "Top K8s Best Practices",
            "link": "https://kubernetes.io/docs/concepts/",
            "type": "kubernetes",
        },
        {
            "title": "OpenDevin Orchestrator Tips",
            "link": "https://github.com/OpenDevin/OpenDevin",
            "type": "github",
        },
        {
            "title": "FastAPI Best Practices",
            "link": "https://fastapi.tiangolo.com/tutorial/",
            "type": "blog",
        },
        {
            "title": "Microservices Architecture Patterns",
            "link": "https://microservices.io/patterns/",
            "type": "blog",
        },
        {
            "title": "AI Agent Development Guide",
            "link": "https://github.com/langchain-ai/langchain",
            "type": "github",
        },
    ]


def scrape_github_repos():
    # TODO: Implement GitHub API integration
    return [
        {
            "repo": "OpenDevin/OpenDevin",
            "stars": 15000,
            "description": "AI agent development",
        },
        {
            "repo": "langchain-ai/langchain",
            "stars": 65000,
            "description": "LLM framework",
        },
    ]


def scrape_blog_posts():
    # TODO: Implement RSS/feed parsing
    return [
        {
            "title": "Kubernetes Security Best Practices",
            "url": "https://blog.example.com/k8s-security",
        },
        {
            "title": "Microservices Monitoring",
            "url": "https://blog.example.com/microservices-monitoring",
        },
    ]
