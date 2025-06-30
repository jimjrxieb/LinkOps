"""
Whis WebScraper - External Intelligence Harvester
Scrapes top posts from dev blogs, K8s docs, Terraform guides for Whis training
"""

import requests
import yaml
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import feedparser
import time

logger = logging.getLogger(__name__)

class WhisWebScraper:
    """Intelligence harvester for Whis training data"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Whis-WebScraper/2.0 (LinkOps MLOps Platform)'
        })
        
        # Target sources for intelligence gathering
        self.dev_sources = {
            'kubernetes_blog': {
                'url': 'https://kubernetes.io/blog/feed.xml',
                'type': 'rss',
                'category': 'kubernetes'
            },
            'terraform_blog': {
                'url': 'https://www.hashicorp.com/blog/feed.xml',
                'type': 'rss', 
                'category': 'terraform'
            },
            'devops_weekly': {
                'url': 'https://www.devopsweekly.com/rss/',
                'type': 'rss',
                'category': 'devops'
            },
            'cncf_blog': {
                'url': 'https://www.cncf.io/feed/',
                'type': 'rss',
                'category': 'cloud_native'
            },
            'helm_blog': {
                'url': 'https://helm.sh/blog/feed.xml',
                'type': 'rss',
                'category': 'helm'
            }
        }
        
        # GitHub trending repositories
        self.github_trending = {
            'kubernetes': 'https://github.com/trending?q=kubernetes&since=weekly',
            'terraform': 'https://github.com/trending?q=terraform&since=weekly',
            'helm': 'https://github.com/trending?q=helm&since=weekly',
            'mlops': 'https://github.com/trending?q=mlops&since=weekly'
        }

    def scrape_dev_blogs(self, hours_back: int = 24) -> List[Dict[str, Any]]:
        """Scrape recent posts from development blogs"""
        logger.info(f"Scraping dev blogs for last {hours_back} hours")
        
        scraped_data = []
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        for source_name, source_config in self.dev_sources.items():
            try:
                logger.info(f"Scraping {source_name}")
                
                if source_config['type'] == 'rss':
                    feed_data = self._scrape_rss_feed(source_config['url'])
                    
                    for entry in feed_data:
                        # Parse publication date
                        pub_date = self._parse_date(entry.get('published', ''))
                        
                        if pub_date and pub_date >= cutoff_time:
                            scraped_item = {
                                'source': source_name,
                                'category': source_config['category'],
                                'title': entry.get('title', ''),
                                'link': entry.get('link', ''),
                                'summary': entry.get('summary', ''),
                                'published': pub_date.isoformat(),
                                'content_type': 'blog_post',
                                'scraped_at': datetime.now().isoformat()
                            }
                            scraped_data.append(scraped_item)
                            
                time.sleep(1)  # Be respectful to servers
                
            except Exception as e:
                logger.error(f"Error scraping {source_name}: {str(e)}")
                continue
                
        logger.info(f"Scraped {len(scraped_data)} blog posts")
        return scraped_data

    def scrape_github_trending(self) -> List[Dict[str, Any]]:
        """Scrape trending GitHub repositories"""
        logger.info("Scraping GitHub trending repositories")
        
        trending_data = []
        
        for category, url in self.github_trending.items():
            try:
                logger.info(f"Scraping GitHub trending for {category}")
                
                response = self.session.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find repository entries
                repo_entries = soup.find_all('article', class_='Box-row')
                
                for entry in repo_entries[:10]:  # Top 10 repos
                    repo_name_elem = entry.find('h2', class_='h3')
                    if repo_name_elem:
                        repo_name = repo_name_elem.get_text().strip()
                        
                        # Get description
                        desc_elem = entry.find('p')
                        description = desc_elem.get_text().strip() if desc_elem else ''
                        
                        # Get stars
                        stars_elem = entry.find('a', href=lambda x: x and 'stargazers' in x)
                        stars = stars_elem.get_text().strip() if stars_elem else '0'
                        
                        trending_item = {
                            'source': 'github_trending',
                            'category': category,
                            'title': repo_name,
                            'description': description,
                            'stars': stars,
                            'link': f"https://github.com/{repo_name}",
                            'content_type': 'github_repo',
                            'scraped_at': datetime.now().isoformat()
                        }
                        trending_data.append(trending_item)
                        
                time.sleep(2)  # Be respectful to GitHub
                
            except Exception as e:
                logger.error(f"Error scraping GitHub trending for {category}: {str(e)}")
                continue
                
        logger.info(f"Scraped {len(trending_data)} trending repositories")
        return trending_data

    def scrape_kubernetes_docs(self) -> List[Dict[str, Any]]:
        """Scrape latest Kubernetes documentation updates"""
        logger.info("Scraping Kubernetes documentation")
        
        k8s_docs = []
        
        try:
            # Scrape K8s concepts page
            concepts_url = "https://kubernetes.io/docs/concepts/"
            response = self.session.get(concepts_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find main content sections
            content_sections = soup.find_all('div', class_='content')
            
            for section in content_sections[:5]:  # Top 5 sections
                title_elem = section.find('h1') or section.find('h2')
                if title_elem:
                    title = title_elem.get_text().strip()
                    
                    # Get first paragraph
                    para_elem = section.find('p')
                    summary = para_elem.get_text().strip() if para_elem else ''
                    
                    doc_item = {
                        'source': 'kubernetes_docs',
                        'category': 'kubernetes',
                        'title': title,
                        'summary': summary,
                        'link': concepts_url,
                        'content_type': 'documentation',
                        'scraped_at': datetime.now().isoformat()
                    }
                    k8s_docs.append(doc_item)
                    
        except Exception as e:
            logger.error(f"Error scraping Kubernetes docs: {str(e)}")
            
        logger.info(f"Scraped {len(k8s_docs)} K8s documentation items")
        return k8s_docs

    def scrape_terraform_guides(self) -> List[Dict[str, Any]]:
        """Scrape Terraform best practices and guides"""
        logger.info("Scraping Terraform guides")
        
        terraform_data = []
        
        try:
            # Scrape Terraform docs
            tf_docs_url = "https://www.terraform.io/docs"
            response = self.session.get(tf_docs_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find guide links
            guide_links = soup.find_all('a', href=lambda x: x and '/guides/' in x)
            
            for link in guide_links[:10]:  # Top 10 guides
                title = link.get_text().strip()
                href = link.get('href', '')
                
                if title and href:
                    guide_item = {
                        'source': 'terraform_docs',
                        'category': 'terraform',
                        'title': title,
                        'link': f"https://www.terraform.io{href}",
                        'content_type': 'guide',
                        'scraped_at': datetime.now().isoformat()
                    }
                    terraform_data.append(guide_item)
                    
        except Exception as e:
            logger.error(f"Error scraping Terraform guides: {str(e)}")
            
        logger.info(f"Scraped {len(terraform_data)} Terraform guides")
        return terraform_data

    def _scrape_rss_feed(self, feed_url: str) -> List[Dict[str, Any]]:
        """Scrape RSS feed and return entries"""
        try:
            feed = feedparser.parse(feed_url)
            return feed.entries
        except Exception as e:
            logger.error(f"Error parsing RSS feed {feed_url}: {str(e)}")
            return []

    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse various date formats"""
        if not date_str:
            return None
            
        # Common date formats
        formats = [
            '%Y-%m-%dT%H:%M:%S%z',
            '%Y-%m-%dT%H:%M:%SZ',
            '%a, %d %b %Y %H:%M:%S %z',
            '%Y-%m-%d %H:%M:%S'
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
                
        return None

    def scrape_all_sources(self, hours_back: int = 24) -> Dict[str, List[Dict[str, Any]]]:
        """Scrape all intelligence sources"""
        logger.info("Starting comprehensive intelligence gathering")
        
        all_data = {
            'blog_posts': self.scrape_dev_blogs(hours_back),
            'github_trending': self.scrape_github_trending(),
            'kubernetes_docs': self.scrape_kubernetes_docs(),
            'terraform_guides': self.scrape_terraform_guides()
        }
        
        total_items = sum(len(items) for items in all_data.values())
        logger.info(f"Total intelligence gathered: {total_items} items")
        
        return all_data 