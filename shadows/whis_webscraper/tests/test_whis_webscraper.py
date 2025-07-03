"""
Test suite for Whis WebScraper
"""

import os
import sys
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app
from scrape_sources import WhisWebScraper
from send_to_sanitize import WhisSanitizeSender
from scrape_agent_logs import AgentLogScraper

client = TestClient(app)


class TestHealthEndpoint:
    def test_health_check(self):
        """Test health endpoint returns correct service info"""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "whis_webscraper"
        assert "Intelligence Harvester" in data["role"]
        assert len(data["capabilities"]) > 0
        assert data["version"] == "2.0.0"


class TestIntelligenceScraping:
    def test_scrape_intelligence_complete(self):
        """Test complete intelligence scraping pipeline"""
        scrape_request = {
            "sources": ["blogs", "github", "agent_logs"],
            "hours_back": 24,
            "send_to_sanitize": True,
        }

        with (
            patch.object(WhisWebScraper, "scrape_dev_blogs") as mock_blogs,
            patch.object(WhisWebScraper, "scrape_github_trending") as mock_github,
            patch.object(AgentLogScraper, "scrape_agent_logs") as mock_logs,
            patch.object(WhisSanitizeSender, "send_batch_to_sanitize") as mock_sanitize,
        ):

            mock_blogs.return_value = [{"title": "Test Blog", "source": "test"}]
            mock_github.return_value = [{"title": "Test Repo", "category": "test"}]
            mock_logs.return_value = [{"message": "Test Log", "agent": "test"}]
            mock_sanitize.return_value = {"success_count": 3, "error_count": 0}

            response = client.post("/scrape/intelligence", json=scrape_request)
            assert response.status_code == 200

            data = response.json()
            assert data["status"] == "completed"
            assert "blogs" in data["sources_scraped"]
            assert "github" in data["sources_scraped"]
            assert "agent_logs" in data["sources_scraped"]
            assert data["total_items"] == 3
            assert data["sanitize_results"] is not None

    def test_scrape_intelligence_partial_sources(self):
        """Test scraping with only some sources"""
        scrape_request = {
            "sources": ["blogs"],
            "hours_back": 12,
            "send_to_sanitize": False,
        }

        with patch.object(WhisWebScraper, "scrape_dev_blogs") as mock_blogs:
            mock_blogs.return_value = [{"title": "Test Blog", "source": "test"}]

            response = client.post("/scrape/intelligence", json=scrape_request)
            assert response.status_code == 200

            data = response.json()
            assert data["status"] == "completed"
            assert data["sources_scraped"] == ["blogs"]
            assert data["total_items"] == 1
            assert data["sanitize_results"] is None


class TestWebSourcesScraping:
    def test_scrape_web_sources(self):
        """Test web sources scraping endpoint"""
        with (
            patch.object(WhisWebScraper, "scrape_all_sources") as mock_scrape,
            patch.object(WhisSanitizeSender, "send_batch_to_sanitize") as mock_sanitize,
        ):

            mock_scrape.return_value = {
                "blog_posts": [{"title": "Blog 1"}],
                "github_trending": [{"title": "Repo 1"}],
                "kubernetes_docs": [{"title": "Doc 1"}],
                "terraform_guides": [{"title": "Guide 1"}],
            }
            mock_sanitize.return_value = {"success_count": 4, "error_count": 0}

            response = client.post(
                "/scrape/web_sources?hours_back=24&send_to_sanitize=true"
            )
            assert response.status_code == 200

            data = response.json()
            assert data["status"] == "success"
            assert len(data["web_sources_scraped"]) == 4
            assert data["total_items"] == 4

    def test_scrape_blogs_only(self):
        """Test blog scraping endpoint"""
        with (
            patch.object(WhisWebScraper, "scrape_dev_blogs") as mock_blogs,
            patch.object(WhisSanitizeSender, "send_batch_to_sanitize") as mock_sanitize,
        ):

            mock_blogs.return_value = [
                {"title": "Blog 1", "source": "kubernetes_blog"},
                {"title": "Blog 2", "source": "terraform_blog"},
            ]
            mock_sanitize.return_value = {"success_count": 2, "error_count": 0}

            response = client.get("/scrape/blogs?hours_back=24&send_to_sanitize=true")
            assert response.status_code == 200

            data = response.json()
            assert data["status"] == "success"
            assert data["blog_posts_scraped"] == 2
            assert "kubernetes_blog" in data["sources"]
            assert "terraform_blog" in data["sources"]

    def test_scrape_github_trending(self):
        """Test GitHub trending scraping endpoint"""
        with (
            patch.object(WhisWebScraper, "scrape_github_trending") as mock_github,
            patch.object(WhisSanitizeSender, "send_batch_to_sanitize") as mock_sanitize,
        ):

            mock_github.return_value = [
                {"title": "repo1", "category": "kubernetes"},
                {"title": "repo2", "category": "terraform"},
            ]
            mock_sanitize.return_value = {"success_count": 2, "error_count": 0}

            response = client.get("/scrape/github_trending?send_to_sanitize=true")
            assert response.status_code == 200

            data = response.json()
            assert data["status"] == "success"
            assert data["trending_repos_scraped"] == 2
            assert "kubernetes" in data["categories"]
            assert "terraform" in data["categories"]


class TestAgentLogScraping:
    def test_scrape_agent_logs(self):
        """Test agent log scraping endpoint"""
        with (
            patch.object(AgentLogScraper, "scrape_agent_logs") as mock_logs,
            patch.object(
                AgentLogScraper, "extract_intelligence_patterns"
            ) as mock_patterns,
            patch.object(
                AgentLogScraper, "generate_intelligence_report"
            ) as mock_report,
            patch.object(WhisSanitizeSender, "send_batch_to_sanitize") as mock_sanitize,
        ):

            mock_logs.return_value = [
                {"message": "Error in deployment", "agent": "katie"},
                {"message": "Successfully scaled", "agent": "katie"},
            ]
            mock_patterns.return_value = {
                "error_patterns": [{"pattern": "Error in deployment"}],
                "success_patterns": [{"pattern": "Successfully scaled"}],
                "summary": {"pattern_counts": {"errors": 1, "successes": 1}},
            }
            mock_report.return_value = {
                "report_type": "agent_intelligence",
                "insights": ["Found 1 error patterns"],
                "recommendations": ["Review error patterns"],
            }
            mock_sanitize.return_value = {"success_count": 2, "error_count": 0}

            response = client.post(
                "/scrape/agent_logs?hours_back=24&send_to_sanitize=true"
            )
            assert response.status_code == 200

            data = response.json()
            assert data["status"] == "success"
            assert data["log_entries_scraped"] == 2
            assert data["patterns_extracted"]["errors"] == 1
            assert data["patterns_extracted"]["successes"] == 1
            assert "intelligence_report" in data


class TestReloopFunctionality:
    def test_reloop_finding(self):
        """Test reloop finding endpoint"""
        response = client.get("/reloop/test-task-123?send_to_sanitize=true")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "success"
        assert data["task_id"] == "test-task-123"
        assert "relooped_to_training" in data["action"]


class TestSanitizeIntegration:
    def test_check_sanitize_health(self):
        """Test sanitize health check endpoint"""
        with patch.object(WhisSanitizeSender, "check_sanitize_health") as mock_health:
            mock_health.return_value = True

            response = client.get("/sanitize/health")
            assert response.status_code == 200

            data = response.json()
            assert data["sanitize_service_healthy"] is True

    def test_get_sanitize_stats(self):
        """Test sanitize stats endpoint"""
        with patch.object(WhisSanitizeSender, "get_sanitize_stats") as mock_stats:
            mock_stats.return_value = {"total_processed": 100, "success_rate": 0.95}

            response = client.get("/sanitize/stats")
            assert response.status_code == 200

            data = response.json()
            assert "sanitize_stats" in data
            assert data["sanitize_stats"]["total_processed"] == 100


class TestCapabilities:
    def test_get_capabilities(self):
        """Test capabilities endpoint"""
        response = client.get("/capabilities")
        assert response.status_code == 200

        data = response.json()
        assert data["service"] == "whis_webscraper"
        assert data["version"] == "2.0.0"
        assert "web_scraping" in data["capabilities"]
        assert "agent_intelligence" in data["capabilities"]
        assert "whis_integration" in data["capabilities"]


class TestWhisWebScraper:
    def test_web_scraper_initialization(self):
        """Test WhisWebScraper initialization"""
        scraper = WhisWebScraper()
        assert scraper.session is not None
        assert "kubernetes_blog" in scraper.dev_sources
        assert "kubernetes" in scraper.github_trending

    def test_scrape_dev_blogs(self):
        """Test dev blog scraping"""
        with patch.object(WhisWebScraper, "_scrape_rss_feed") as mock_rss:
            mock_rss.return_value = [
                {
                    "title": "Test Blog Post",
                    "link": "https://test.com/post",
                    "summary": "Test summary",
                    "published": "2024-01-01T10:00:00Z",
                }
            ]

            scraper = WhisWebScraper()
            results = scraper.scrape_dev_blogs(hours_back=24)

            assert len(results) > 0
            assert results[0]["title"] == "Test Blog Post"

    def test_scrape_github_trending(self):
        """Test GitHub trending scraping"""
        with patch.object(WhisWebScraper, "session") as mock_session:
            mock_response = MagicMock()
            mock_response.content = (
                '<html><body><article class="Box-row"><h2 class="h3">test/repo</h2>'
                "<p>Test description</p></article></body></html>"
            )
            mock_response.raise_for_status.return_value = None
            mock_session.get.return_value = mock_response

            scraper = WhisWebScraper()
            results = scraper.scrape_github_trending()

            assert len(results) > 0


class TestWhisSanitizeSender:
    def test_sanitize_sender_initialization(self):
        """Test WhisSanitizeSender initialization"""
        sender = WhisSanitizeSender("http://test:8003")
        assert sender.sanitize_url == "http://test:8003"
        assert sender.session is not None

    def test_format_for_sanitize(self):
        """Test data formatting for sanitize"""
        sender = WhisSanitizeSender()

        scraped_data = {
            "blog_posts": [
                {
                    "title": "Test Blog",
                    "source": "test_blog",
                    "category": "test",
                    "link": "https://test.com",
                }
            ]
        }

        formatted = sender.format_for_sanitize(scraped_data)
        assert len(formatted) == 1
        assert formatted[0]["title"] == "Test Blog"
        assert formatted[0]["source"] == "whis_webscraper"

    def test_send_to_sanitize(self):
        """Test sending data to sanitize"""
        with patch.object(WhisSanitizeSender, "session") as mock_session:
            mock_response = MagicMock()
            mock_response.json.return_value = {"status": "success", "id": "test-123"}
            mock_response.raise_for_status.return_value = None
            mock_session.post.return_value = mock_response

            sender = WhisSanitizeSender()
            formatted_items = [{"title": "Test", "content": "Test content"}]

            results = sender.send_to_sanitize(formatted_items)
            assert results["success_count"] == 1
            assert results["error_count"] == 0


class TestAgentLogScraper:
    def test_log_scraper_initialization(self):
        """Test AgentLogScraper initialization"""
        scraper = AgentLogScraper("/test/logs")
        assert scraper.logs_base_path == "/test/logs"
        assert "katie" in scraper.agent_patterns
        assert "igris" in scraper.agent_patterns

    def test_extract_intelligence_patterns(self):
        """Test pattern extraction from logs"""
        scraper = AgentLogScraper()

        log_entries = [
            {
                "message": "Error in deployment scaling",
                "level": "ERROR",
                "agent": "katie",
                "category": "kubernetes_operations",
            },
            {
                "message": "Successfully completed analysis",
                "level": "INFO",
                "agent": "igris",
                "category": "infrastructure_analysis",
            },
        ]

        patterns = scraper.extract_intelligence_patterns(log_entries)
        assert patterns["summary"]["pattern_counts"]["errors"] == 1
        assert patterns["summary"]["pattern_counts"]["successes"] == 1

    def test_generate_intelligence_report(self):
        """Test intelligence report generation"""
        with (
            patch.object(AgentLogScraper, "scrape_agent_logs") as mock_logs,
            patch.object(
                AgentLogScraper, "extract_intelligence_patterns"
            ) as mock_patterns,
        ):

            mock_logs.return_value = [{"message": "Test log", "agent": "test"}]
            mock_patterns.return_value = {
                "error_patterns": [],
                "success_patterns": [],
                "summary": {"pattern_counts": {"errors": 0, "successes": 0}},
            }

            scraper = AgentLogScraper()
            report = scraper.generate_intelligence_report(hours_back=24)

            assert report["report_type"] == "agent_intelligence"
            assert "insights" in report
            assert "recommendations" in report
