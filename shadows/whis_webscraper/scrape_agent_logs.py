"""
Whis WebScraper - Agent Log Intelligence Harvester
Scrapes logs from LinkOps agents for intelligence and pattern analysis
"""

import os
import re
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import glob

logger = logging.getLogger(__name__)


class AgentLogScraper:
    """Scrapes logs from LinkOps agents for intelligence gathering"""

    def __init__(self, logs_base_path: str = "/app/logs"):
        self.logs_base_path = logs_base_path
        self.agent_patterns = {
            "katie": {
                "log_pattern": "katie*.log",
                "keywords": ["kubernetes", "deployment", "scale", "error", "success"],
                "category": "kubernetes_operations",
            },
            "igris": {
                "log_pattern": "igris*.log",
                "keywords": [
                    "infrastructure",
                    "security",
                    "analysis",
                    "recommendation",
                ],
                "category": "infrastructure_analysis",
            },
            "james": {
                "log_pattern": "james*.log",
                "keywords": ["assistant", "voice", "image", "task"],
                "category": "ai_assistant",
            },
            "ficknury": {
                "log_pattern": "ficknury*.log",
                "keywords": ["deployment", "evaluation", "model", "performance"],
                "category": "ml_deployment",
            },
            "whis": {
                "log_pattern": "whis*.log",
                "keywords": ["training", "sanitize", "smithing", "enhance"],
                "category": "ml_training",
            },
        }

    def scrape_agent_logs(self, hours_back: int = 24) -> List[Dict[str, Any]]:
        """Scrape logs from all LinkOps agents"""
        logger.info(f"Scraping agent logs for last {hours_back} hours")

        all_log_data = []
        cutoff_time = datetime.now() - timedelta(hours=hours_back)

        for agent_name, config in self.agent_patterns.items():
            try:
                agent_logs = self._scrape_single_agent_logs(
                    agent_name, config, cutoff_time
                )
                all_log_data.extend(agent_logs)
                logger.info(f"Scraped {len(agent_logs)} log entries from {agent_name}")

            except Exception as e:
                logger.error(f"Error scraping {agent_name} logs: {str(e)}")
                continue

        logger.info(f"Total agent log entries scraped: {len(all_log_data)}")
        return all_log_data

    def _scrape_single_agent_logs(
        self, agent_name: str, config: Dict[str, Any], cutoff_time: datetime
    ) -> List[Dict[str, Any]]:
        """Scrape logs from a single agent"""
        log_entries = []

        # Find log files matching pattern
        log_pattern = os.path.join(self.logs_base_path, config["log_pattern"])
        log_files = glob.glob(log_pattern)

        if not log_files:
            logger.warning(
                f"No log files found for {agent_name} with pattern {log_pattern}"
            )
            return log_entries

        for log_file in log_files:
            try:
                file_entries = self._parse_log_file(
                    log_file, agent_name, config, cutoff_time
                )
                log_entries.extend(file_entries)

            except Exception as e:
                logger.error(f"Error parsing log file {log_file}: {str(e)}")
                continue

        return log_entries

    def _parse_log_file(
        self,
        log_file: str,
        agent_name: str,
        config: Dict[str, Any],
        cutoff_time: datetime,
    ) -> List[Dict[str, Any]]:
        """Parse individual log file for relevant entries"""
        entries = []

        try:
            with open(log_file, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        # Parse log line
                        parsed_entry = self._parse_log_line(line, line_num)

                        if parsed_entry:
                            # Check if entry is within time window
                            if (
                                parsed_entry.get("timestamp")
                                and parsed_entry["timestamp"] >= cutoff_time
                            ):
                                # Check if entry contains relevant keywords
                                if self._is_relevant_entry(
                                    parsed_entry.get("message", ""), config["keywords"]
                                ):
                                    # Add agent-specific metadata
                                    parsed_entry.update(
                                        {
                                            "agent": agent_name,
                                            "category": config["category"],
                                            "log_file": os.path.basename(log_file),
                                            "line_number": line_num,
                                        }
                                    )
                                    entries.append(parsed_entry)

                    except Exception as e:
                        logger.debug(
                            f"Error parsing line {line_num} in {log_file}: {str(e)}"
                        )
                        continue

        except Exception as e:
            logger.error(f"Error reading log file {log_file}: {str(e)}")

        return entries

    def _parse_log_line(self, line: str, line_num: int) -> Optional[Dict[str, Any]]:
        """Parse a single log line into structured data"""
        line = line.strip()
        if not line:
            return None

        # Common log formats
        log_patterns = [
            # ISO timestamp format
            r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2}))"
            r"\s+(\w+)\s+(.+)",
            # Standard timestamp format
            r"(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(\w+)\s+(.+)",
            # Simple timestamp
            r"(\d{2}:\d{2}:\d{2})\s+(.+)",
        ]

        for pattern in log_patterns:
            match = re.match(pattern, line)
            if match:
                groups = match.groups()

                if len(groups) >= 2:
                    timestamp_str = groups[0]
                    level = groups[1] if len(groups) > 2 else "INFO"
                    message = groups[-1]

                    # Parse timestamp
                    timestamp = self._parse_timestamp(timestamp_str)

                    return {
                        "timestamp": timestamp,
                        "level": level,
                        "message": message,
                        "raw_line": line,
                    }

        # If no pattern matches, create basic entry
        return {
            "timestamp": datetime.now(),
            "level": "UNKNOWN",
            "message": line,
            "raw_line": line,
        }

    def _parse_timestamp(self, timestamp_str: str) -> datetime:
        """Parse various timestamp formats"""
        try:
            # ISO format
            if "T" in timestamp_str:
                return datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            # Standard format
            elif len(timestamp_str) > 10:
                return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            # Time only (assume today)
            else:
                today = datetime.now().date()
                time_part = datetime.strptime(timestamp_str, "%H:%M:%S").time()
                return datetime.combine(today, time_part)
        except Exception:
            return datetime.now()

    def _is_relevant_entry(self, message: str, keywords: List[str]) -> bool:
        """Check if log entry contains relevant keywords"""
        message_lower = message.lower()
        return any(keyword.lower() in message_lower for keyword in keywords)

    def extract_intelligence_patterns(
        self, log_entries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Extract intelligence patterns from log entries"""
        logger.info("Extracting intelligence patterns from agent logs")

        patterns = {
            "error_patterns": [],
            "success_patterns": [],
            "performance_patterns": [],
            "usage_patterns": [],
            "recommendations": [],
        }

        for entry in log_entries:
            message = entry.get("message", "").lower()
            level = entry.get("level", "").upper()

            # Error patterns
            if level in ["ERROR", "CRITICAL"] or "error" in message:
                patterns["error_patterns"].append(
                    {
                        "agent": entry.get("agent"),
                        "pattern": message,
                        "timestamp": entry.get("timestamp"),
                        "category": entry.get("category"),
                    }
                )

            # Success patterns
            elif level == "INFO" and any(
                word in message for word in ["success", "completed", "finished"]
            ):
                patterns["success_patterns"].append(
                    {
                        "agent": entry.get("agent"),
                        "pattern": message,
                        "timestamp": entry.get("timestamp"),
                        "category": entry.get("category"),
                    }
                )

            # Performance patterns
            elif any(
                word in message
                for word in ["performance", "latency", "throughput", "cpu", "memory"]
            ):
                patterns["performance_patterns"].append(
                    {
                        "agent": entry.get("agent"),
                        "pattern": message,
                        "timestamp": entry.get("timestamp"),
                        "category": entry.get("category"),
                    }
                )

            # Usage patterns
            elif any(
                word in message for word in ["request", "api", "endpoint", "call"]
            ):
                patterns["usage_patterns"].append(
                    {
                        "agent": entry.get("agent"),
                        "pattern": message,
                        "timestamp": entry.get("timestamp"),
                        "category": entry.get("category"),
                    }
                )

            # Recommendations
            elif any(
                word in message
                for word in ["recommend", "suggest", "advice", "best practice"]
            ):
                patterns["recommendations"].append(
                    {
                        "agent": entry.get("agent"),
                        "pattern": message,
                        "timestamp": entry.get("timestamp"),
                        "category": entry.get("category"),
                    }
                )

        # Add summary
        patterns["summary"] = {
            "total_entries_analyzed": len(log_entries),
            "pattern_counts": {
                "errors": len(patterns["error_patterns"]),
                "successes": len(patterns["success_patterns"]),
                "performance": len(patterns["performance_patterns"]),
                "usage": len(patterns["usage_patterns"]),
                "recommendations": len(patterns["recommendations"]),
            },
            "analysis_timestamp": datetime.now().isoformat(),
        }

        logger.info(f"Extracted patterns: {patterns['summary']['pattern_counts']}")
        return patterns

    def generate_intelligence_report(self, hours_back: int = 24) -> Dict[str, Any]:
        """Generate comprehensive intelligence report from agent logs"""
        logger.info(f"Generating intelligence report for last {hours_back} hours")

        # Scrape logs
        log_entries = self.scrape_agent_logs(hours_back)

        # Extract patterns
        patterns = self.extract_intelligence_patterns(log_entries)

        # Generate report
        report = {
            "report_type": "agent_intelligence",
            "time_period": f"Last {hours_back} hours",
            "generated_at": datetime.now().isoformat(),
            "log_entries": log_entries,
            "patterns": patterns,
            "insights": self._generate_insights(patterns),
            "recommendations": self._generate_recommendations(patterns),
        }

        logger.info("Intelligence report generated successfully")
        return report

    def _generate_insights(self, patterns: Dict[str, Any]) -> List[str]:
        """Generate insights from patterns"""
        insights = []

        # Error insights
        error_count = len(patterns["error_patterns"])
        if error_count > 0:
            insights.append(
                f"Found {error_count} error patterns that may need attention"
            )

        # Success insights
        success_count = len(patterns["success_patterns"])
        if success_count > 0:
            insights.append(f"Identified {success_count} successful operation patterns")

        # Performance insights
        perf_count = len(patterns["performance_patterns"])
        if perf_count > 0:
            insights.append(
                f"Detected {perf_count} performance-related patterns for optimization"
            )

        # Usage insights
        usage_count = len(patterns["usage_patterns"])
        if usage_count > 0:
            insights.append(
                f"Tracked {usage_count} usage patterns for capacity planning"
            )

        # Recommendation insights
        rec_count = len(patterns["recommendations"])
        if rec_count > 0:
            insights.append(f"Collected {rec_count} recommendations for improvement")

        return insights

    def _generate_recommendations(self, patterns: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on patterns"""
        recommendations = []

        # Error-based recommendations
        if patterns["error_patterns"]:
            recommendations.append(
                "Review error patterns and implement error handling improvements"
            )

        # Performance-based recommendations
        if patterns["performance_patterns"]:
            recommendations.append(
                "Analyze performance patterns for optimization opportunities"
            )

        # Usage-based recommendations
        if patterns["usage_patterns"]:
            recommendations.append(
                "Monitor usage patterns for capacity planning and scaling"
            )

        # Success-based recommendations
        if patterns["success_patterns"]:
            recommendations.append(
                "Document successful operation patterns for best practices"
            )

        return recommendations
