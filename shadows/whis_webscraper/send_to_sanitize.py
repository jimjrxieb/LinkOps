"""
Whis WebScraper - Send to Sanitize Module
Sends scraped intelligence to whis_sanitize for processing and training queue
"""

import requests
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import yaml

logger = logging.getLogger(__name__)


class WhisSanitizeSender:
    """Sends scraped data to whis_sanitize for processing"""

    def __init__(self, sanitize_service_url: str = "http://whis_sanitize:8003"):
        self.sanitize_url = sanitize_service_url
        self.session = requests.Session()
        self.session.headers.update(
            {"Content-Type": "application/json", "User-Agent": "Whis-WebScraper/2.0"}
        )

    def format_for_sanitize(
        self, scraped_data: Dict[str, List[Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
        """Format scraped data for whis_sanitize processing"""
        logger.info("Formatting scraped data for sanitize processing")

        formatted_items = []

        for source_type, items in scraped_data.items():
            for item in items:
                # Create standardized format for Whis processing
                formatted_item = {
                    "source": "whis_webscraper",
                    "content_type": item.get("content_type", "unknown"),
                    "category": item.get("category", "general"),
                    "title": item.get("title", ""),
                    "content": self._extract_content(item),
                    "metadata": {
                        "original_source": item.get("source", ""),
                        "link": item.get("link", ""),
                        "published": item.get("published", ""),
                        "scraped_at": item.get("scraped_at", ""),
                        "stars": item.get("stars", ""),
                        "summary": item.get("summary", ""),
                    },
                    "priority": self._calculate_priority(item),
                    "tags": self._generate_tags(item),
                    "processing_notes": f"Auto-scraped by Whis WebScraper from {item.get('source', 'unknown')}",
                }

                formatted_items.append(formatted_item)

        logger.info(f"Formatted {len(formatted_items)} items for sanitize processing")
        return formatted_items

    def send_to_sanitize(self, formatted_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Send formatted data to whis_sanitize service"""
        logger.info(f"Sending {len(formatted_items)} items to whis_sanitize")

        results = {
            "success_count": 0,
            "error_count": 0,
            "errors": [],
            "processed_items": [],
        }

        for item in formatted_items:
            try:
                # Send to sanitize endpoint
                sanitize_endpoint = f"{self.sanitize_url}/api/process_external"

                payload = {
                    "data": item,
                    "source": "whis_webscraper",
                    "auto_process": True,
                    "add_to_training_queue": True,
                }

                response = self.session.post(sanitize_endpoint, json=payload)
                response.raise_for_status()

                result = response.json()

                if result.get("status") == "success":
                    results["success_count"] += 1
                    results["processed_items"].append(
                        {
                            "id": result.get("id"),
                            "title": item.get("title"),
                            "status": "processed",
                        }
                    )
                else:
                    results["error_count"] += 1
                    results["errors"].append(
                        {
                            "title": item.get("title"),
                            "error": result.get("error", "Unknown error"),
                        }
                    )

            except requests.exceptions.RequestException as e:
                results["error_count"] += 1
                results["errors"].append(
                    {"title": item.get("title"), "error": f"Network error: {str(e)}"}
                )
                logger.error(f"Error sending item to sanitize: {str(e)}")

            except Exception as e:
                results["error_count"] += 1
                results["errors"].append(
                    {"title": item.get("title"), "error": f"Processing error: {str(e)}"}
                )
                logger.error(f"Unexpected error processing item: {str(e)}")

        logger.info(
            f"Sanitize processing complete: {results['success_count']} success, {results['error_count']} errors"
        )
        return results

    def send_batch_to_sanitize(
        self, scraped_data: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """Complete pipeline: format and send to sanitize"""
        logger.info("Starting batch processing pipeline")

        # Format data for sanitize
        formatted_items = self.format_for_sanitize(scraped_data)

        # Send to sanitize
        results = self.send_to_sanitize(formatted_items)

        # Add summary
        results["summary"] = {
            "total_items_formatted": len(formatted_items),
            "source_breakdown": {
                source: len(items) for source, items in scraped_data.items()
            },
            "processing_timestamp": datetime.now().isoformat(),
        }

        return results

    def _extract_content(self, item: Dict[str, Any]) -> str:
        """Extract main content from scraped item"""
        content_parts = []

        # Add title
        if item.get("title"):
            content_parts.append(f"Title: {item['title']}")

        # Add summary/description
        if item.get("summary"):
            content_parts.append(f"Summary: {item['summary']}")
        elif item.get("description"):
            content_parts.append(f"Description: {item['description']}")

        # Add stars for GitHub repos
        if item.get("stars"):
            content_parts.append(f"Stars: {item['stars']}")

        # Add link
        if item.get("link"):
            content_parts.append(f"Source: {item['link']}")

        return "\n\n".join(content_parts)

    def _calculate_priority(self, item: Dict[str, Any]) -> int:
        """Calculate processing priority (1-10, 10 being highest)"""
        priority = 5  # Default priority

        # Boost priority for recent content
        if item.get("published"):
            try:
                pub_date = datetime.fromisoformat(
                    item["published"].replace("Z", "+00:00")
                )
                days_old = (datetime.now() - pub_date).days
                if days_old <= 1:
                    priority += 2
                elif days_old <= 7:
                    priority += 1
            except:
                pass

        # Boost priority for trending GitHub repos
        if item.get("stars"):
            try:
                stars = int(item["stars"].replace(",", ""))
                if stars > 1000:
                    priority += 2
                elif stars > 100:
                    priority += 1
            except:
                pass

        # Boost priority for official docs
        if item.get("source") in ["kubernetes_docs", "terraform_docs"]:
            priority += 1

        return min(priority, 10)

    def _generate_tags(self, item: Dict[str, Any]) -> List[str]:
        """Generate tags for content categorization"""
        tags = []

        # Add category tag
        if item.get("category"):
            tags.append(item["category"])

        # Add content type tag
        if item.get("content_type"):
            tags.append(item["content_type"])

        # Add source tag
        if item.get("source"):
            tags.append(f"source_{item['source']}")

        # Add auto-generated tags
        tags.extend(["auto_scraped", "whis_training"])

        return list(set(tags))  # Remove duplicates

    def check_sanitize_health(self) -> bool:
        """Check if whis_sanitize service is healthy"""
        try:
            response = self.session.get(f"{self.sanitize_url}/health")
            return response.status_code == 200
        except:
            return False

    def get_sanitize_stats(self) -> Dict[str, Any]:
        """Get statistics from whis_sanitize service"""
        try:
            response = self.session.get(f"{self.sanitize_url}/api/stats")
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "Failed to get stats"}
        except Exception as e:
            return {"error": f"Network error: {str(e)}"}
