"""
Whis WebScraper - Intelligence Harvester for Whis Training
Scrapes external sources and agent logs, sends to whis_sanitize for processing
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import logging
import asyncio
from datetime import datetime

# Import Whis WebScraper modules
from scrape_sources import WhisWebScraper
from send_to_sanitize import WhisSanitizeSender
from scrape_agent_logs import AgentLogScraper

app = FastAPI(
    title="Whis WebScraper - Intelligence Harvester",
    description="Scrapes external sources and agent logs for Whis training data",
    version="2.0.0"
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize scraper components
web_scraper = WhisWebScraper()
sanitize_sender = WhisSanitizeSender()
log_scraper = AgentLogScraper()


class ScrapeRequest(BaseModel):
    sources: List[str] = ["blogs", "github", "kubernetes_docs", "terraform_guides", "agent_logs"]
    hours_back: int = 24
    send_to_sanitize: bool = True
    auto_process: bool = True


class ScrapeResponse(BaseModel):
    task_id: str
    status: str
    sources_scraped: List[str]
    total_items: int
    sanitize_results: Optional[Dict[str, Any]] = None
    timestamp: str


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "whis_webscraper",
        "role": "Intelligence Harvester for Whis Training",
        "capabilities": [
            "Web Blog Scraping",
            "GitHub Trending Analysis", 
            "Kubernetes Docs Harvesting",
            "Terraform Guides Collection",
            "Agent Log Intelligence",
            "Whis Sanitize Integration",
            "Auto Training Queue"
        ],
        "version": "2.0.0"
    }


@app.post("/scrape/intelligence", response_model=ScrapeResponse)
async def scrape_intelligence(request: ScrapeRequest, background_tasks: BackgroundTasks):
    """
    Scrape intelligence from multiple sources and optionally send to sanitize
    """
    task_id = f"scrape_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    logger.info(f"Starting intelligence scraping task {task_id}")
    
    try:
        all_scraped_data = {}
        sources_scraped = []
        total_items = 0
        
        # Scrape web sources
        if "blogs" in request.sources:
            logger.info("Scraping development blogs")
            all_scraped_data.update(web_scraper.scrape_dev_blogs(request.hours_back))
            sources_scraped.append("blogs")
            
        if "github" in request.sources:
            logger.info("Scraping GitHub trending")
            all_scraped_data["github_trending"] = web_scraper.scrape_github_trending()
            sources_scraped.append("github")
            
        if "kubernetes_docs" in request.sources:
            logger.info("Scraping Kubernetes documentation")
            all_scraped_data["kubernetes_docs"] = web_scraper.scrape_kubernetes_docs()
            sources_scraped.append("kubernetes_docs")
            
        if "terraform_guides" in request.sources:
            logger.info("Scraping Terraform guides")
            all_scraped_data["terraform_guides"] = web_scraper.scrape_terraform_guides()
            sources_scraped.append("terraform_guides")
            
        # Scrape agent logs
        if "agent_logs" in request.sources:
            logger.info("Scraping agent logs")
            all_scraped_data["agent_logs"] = log_scraper.scrape_agent_logs(request.hours_back)
            sources_scraped.append("agent_logs")
            
        # Calculate total items
        total_items = sum(len(items) for items in all_scraped_data.values())
        
        # Send to sanitize if requested
        sanitize_results = None
        if request.send_to_sanitize and total_items > 0:
            logger.info(f"Sending {total_items} items to whis_sanitize")
            sanitize_results = sanitize_sender.send_batch_to_sanitize(all_scraped_data)
            
        response = ScrapeResponse(
            task_id=task_id,
            status="completed",
            sources_scraped=sources_scraped,
            total_items=total_items,
            sanitize_results=sanitize_results,
            timestamp=datetime.now().isoformat()
        )
        
        logger.info(f"Intelligence scraping completed: {total_items} items from {len(sources_scraped)} sources")
        return response
        
    except Exception as e:
        logger.error(f"Intelligence scraping failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")


@app.post("/scrape/web_sources")
async def scrape_web_sources(hours_back: int = 24, send_to_sanitize: bool = True):
    """
    Scrape web sources (blogs, GitHub, docs) only
    """
    try:
        logger.info(f"Scraping web sources for last {hours_back} hours")
        
        # Scrape all web sources
        web_data = web_scraper.scrape_all_sources(hours_back)
        
        # Send to sanitize if requested
        sanitize_results = None
        if send_to_sanitize:
            sanitize_results = sanitize_sender.send_batch_to_sanitize(web_data)
            
        return {
            "status": "success",
            "web_sources_scraped": list(web_data.keys()),
            "total_items": sum(len(items) for items in web_data.values()),
            "sanitize_results": sanitize_results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Web scraping failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Web scraping failed: {str(e)}")


@app.post("/scrape/agent_logs")
async def scrape_agent_logs(hours_back: int = 24, send_to_sanitize: bool = True):
    """
    Scrape agent logs for intelligence patterns
    """
    try:
        logger.info(f"Scraping agent logs for last {hours_back} hours")
        
        # Scrape agent logs
        log_entries = log_scraper.scrape_agent_logs(hours_back)
        
        # Extract patterns
        patterns = log_scraper.extract_intelligence_patterns(log_entries)
        
        # Generate report
        report = log_scraper.generate_intelligence_report(hours_back)
        
        # Send to sanitize if requested
        sanitize_results = None
        if send_to_sanitize and log_entries:
            # Format log data for sanitize
            log_data = {
                'agent_logs': log_entries,
                'intelligence_patterns': patterns
            }
            sanitize_results = sanitize_sender.send_batch_to_sanitize(log_data)
            
        return {
            "status": "success",
            "log_entries_scraped": len(log_entries),
            "patterns_extracted": patterns['summary']['pattern_counts'],
            "intelligence_report": report,
            "sanitize_results": sanitize_results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Agent log scraping failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Agent log scraping failed: {str(e)}")


@app.get("/scrape/blogs")
async def scrape_blogs(hours_back: int = 24, send_to_sanitize: bool = True):
    """
    Scrape development blogs only
    """
    try:
        logger.info(f"Scraping blogs for last {hours_back} hours")
        
        blog_posts = web_scraper.scrape_dev_blogs(hours_back)
        
        # Send to sanitize if requested
        sanitize_results = None
        if send_to_sanitize and blog_posts:
            blog_data = {'blog_posts': blog_posts}
            sanitize_results = sanitize_sender.send_batch_to_sanitize(blog_data)
            
        return {
            "status": "success",
            "blog_posts_scraped": len(blog_posts),
            "sources": list(set(post['source'] for post in blog_posts)),
            "sanitize_results": sanitize_results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Blog scraping failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Blog scraping failed: {str(e)}")


@app.get("/scrape/github_trending")
async def scrape_github_trending(send_to_sanitize: bool = True):
    """
    Scrape GitHub trending repositories
    """
    try:
        logger.info("Scraping GitHub trending repositories")
        
        trending_repos = web_scraper.scrape_github_trending()
        
        # Send to sanitize if requested
        sanitize_results = None
        if send_to_sanitize and trending_repos:
            trending_data = {'github_trending': trending_repos}
            sanitize_results = sanitize_sender.send_batch_to_sanitize(trending_data)
            
        return {
            "status": "success",
            "trending_repos_scraped": len(trending_repos),
            "categories": list(set(repo['category'] for repo in trending_repos)),
            "sanitize_results": sanitize_results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"GitHub trending scraping failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"GitHub trending scraping failed: {str(e)}")


@app.get("/reloop/{task_id}")
async def reloop_finding(task_id: str, send_to_sanitize: bool = True):
    """
    Reloop a specific finding back to Whis training queue
    """
    try:
        logger.info(f"Relooping finding {task_id}")
        
        # This would typically retrieve a specific finding from storage
        # For now, we'll return a placeholder response
        return {
            "status": "success",
            "task_id": task_id,
            "action": "relooped_to_training",
            "message": f"Finding {task_id} has been relooped to Whis training queue",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Reloop failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Reloop failed: {str(e)}")


@app.get("/sanitize/health")
async def check_sanitize_health():
    """
    Check if whis_sanitize service is healthy
    """
    try:
        is_healthy = sanitize_sender.check_sanitize_health()
        return {
            "sanitize_service_healthy": is_healthy,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "sanitize_service_healthy": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@app.get("/sanitize/stats")
async def get_sanitize_stats():
    """
    Get statistics from whis_sanitize service
    """
    try:
        stats = sanitize_sender.get_sanitize_stats()
        return {
            "sanitize_stats": stats,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "sanitize_stats": {"error": str(e)},
            "timestamp": datetime.now().isoformat()
        }


@app.get("/capabilities")
def get_capabilities():
    """
    Get Whis WebScraper capabilities and supported sources
    """
    return {
        "service": "whis_webscraper",
        "version": "2.0.0",
        "capabilities": {
            "web_scraping": {
                "dev_blogs": "Development blog posts and articles",
                "github_trending": "Trending GitHub repositories",
                "kubernetes_docs": "Kubernetes documentation updates",
                "terraform_guides": "Terraform guides and best practices"
            },
            "agent_intelligence": {
                "log_scraping": "Scrape logs from LinkOps agents",
                "pattern_extraction": "Extract intelligence patterns from logs",
                "insight_generation": "Generate insights and recommendations"
            },
            "whis_integration": {
                "sanitize_sending": "Send scraped data to whis_sanitize",
                "training_queue": "Auto-add to Whis training queue",
                "reloop_findings": "Reloop specific findings for retraining"
            }
        },
        "supported_sources": list(web_scraper.dev_sources.keys()) + list(web_scraper.github_trending.keys()),
        "supported_agents": list(log_scraper.agent_patterns.keys())
    }
