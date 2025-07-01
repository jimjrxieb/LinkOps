import os
import tempfile
import shutil
import re
from typing import Dict, List, Any
from pathlib import Path
import git
from urllib.parse import urlparse

class RepoAnalyzer:
    def __init__(self):
        self.temp_dir = None
        self.repo_path = None
        
    async def analyze_repository(self, repo_url: str, branch: str = "main") -> Dict[str, Any]:
        """Clone and analyze a GitHub repository"""
        try:
            # Clone the repository
            self.temp_dir = tempfile.mkdtemp()
            self.repo_path = os.path.join(self.temp_dir, "repo")
            
            print(f"Cloning {repo_url} to {self.repo_path}")
            repo = git.Repo.clone_from(repo_url, self.repo_path, branch=branch)
            
            # Extract repo name from URL
            repo_name = self._extract_repo_name(repo_url)
            
            # Perform analysis
            analysis = {
                "repo_name": repo_name,
                "languages": self._detect_languages(),
                "structure": self._analyze_structure(),
                "ci_configs": self._detect_ci_configs(),
                "helm_charts": self._detect_helm_charts(),
                "dockerfiles": self._detect_dockerfiles(),
                "gitops_tools": self._detect_gitops_tools(),
                "architecture_patterns": self._detect_architecture_patterns(),
                "security_issues": self._detect_security_issues(),
                "recommendations": self._generate_recommendations()
            }
            
            return analysis
            
        except Exception as e:
            raise Exception(f"Failed to analyze repository: {str(e)}")
        finally:
            # Cleanup
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)

    def _extract_repo_name(self, repo_url: str) -> str:
        """Extract repository name from URL"""
        parsed = urlparse(repo_url)
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) >= 2:
            return path_parts[-1].replace('.git', '')
        return "unknown-repo"

    def _detect_languages(self) -> List[str]:
        """Detect programming languages used in the repository"""
        languages = set()
        
        # Common file extensions and their languages
        lang_extensions = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.go': 'Go',
            '.rs': 'Rust',
            '.cpp': 'C++',
            '.c': 'C',
            '.cs': 'C#',
            '.php': 'PHP',
            '.rb': 'Ruby',
            '.scala': 'Scala',
            '.kt': 'Kotlin',
            '.swift': 'Swift',
            '.sh': 'Shell',
            '.yaml': 'YAML',
            '.yml': 'YAML',
            '.json': 'JSON',
            '.xml': 'XML',
            '.html': 'HTML',
            '.css': 'CSS',
            '.sql': 'SQL',
            '.dockerfile': 'Dockerfile',
            '.tf': 'Terraform',
            '.hcl': 'HCL'
        }
        
        for root, dirs, files in os.walk(self.repo_path):
            # Skip hidden directories and common exclusions
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'vendor', '__pycache__']]
            
            for file in files:
                if file.startswith('.'):
                    continue
                    
                file_path = Path(file)
                extension = file_path.suffix.lower()
                
                if extension in lang_extensions:
                    languages.add(lang_extensions[extension])
                elif file_path.name.lower() in ['dockerfile', 'makefile', 'docker-compose.yml']:
                    languages.add(file_path.name.upper())
        
        return sorted(list(languages))

    def _analyze_structure(self) -> Dict[str, Any]:
        """Analyze the repository structure"""
        structure = {
            "root_files": [],
            "directories": [],
            "total_files": 0,
            "depth": 0
        }
        
        for root, dirs, files in os.walk(self.repo_path):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            rel_path = os.path.relpath(root, self.repo_path)
            if rel_path == '.':
                # Root level
                structure["root_files"] = [f for f in files if not f.startswith('.')]
            else:
                # Subdirectories
                structure["directories"].append({
                    "path": rel_path,
                    "files": [f for f in files if not f.startswith('.')],
                    "subdirs": dirs
                })
            
            structure["total_files"] += len([f for f in files if not f.startswith('.')])
            structure["depth"] = max(structure["depth"], rel_path.count(os.sep) if rel_path != '.' else 0)
        
        return structure

    def _detect_ci_configs(self) -> List[Dict[str, Any]]:
        """Detect CI/CD configuration files"""
        ci_configs = []
        
        ci_patterns = [
            ('.github/workflows/*.yml', 'GitHub Actions'),
            ('.github/workflows/*.yaml', 'GitHub Actions'),
            ('.gitlab-ci.yml', 'GitLab CI'),
            ('.gitlab-ci.yaml', 'GitLab CI'),
            ('Jenkinsfile', 'Jenkins'),
            ('azure-pipelines.yml', 'Azure DevOps'),
            ('azure-pipelines.yaml', 'Azure DevOps'),
            ('bitbucket-pipelines.yml', 'Bitbucket Pipelines'),
            ('circle.yml', 'CircleCI'),
            ('.circleci/config.yml', 'CircleCI'),
            ('travis.yml', 'Travis CI'),
            ('.travis.yml', 'Travis CI'),
            ('buildkite.yml', 'Buildkite'),
            ('drone.yml', 'Drone CI'),
            ('appveyor.yml', 'AppVeyor')
        ]
        
        for pattern, ci_type in ci_patterns:
            if '*' in pattern:
                # Handle glob patterns
                import glob
                matches = glob.glob(os.path.join(self.repo_path, pattern))
                for match in matches:
                    rel_path = os.path.relpath(match, self.repo_path)
                    ci_configs.append({
                        "type": ci_type,
                        "file": rel_path,
                        "content_preview": self._get_file_preview(match)
                    })
            else:
                # Handle specific files
                file_path = os.path.join(self.repo_path, pattern)
                if os.path.exists(file_path):
                    ci_configs.append({
                        "type": ci_type,
                        "file": pattern,
                        "content_preview": self._get_file_preview(file_path)
                    })
        
        return ci_configs

    def _detect_helm_charts(self) -> List[Dict[str, Any]]:
        """Detect Helm charts in the repository"""
        helm_charts = []
        
        for root, dirs, files in os.walk(self.repo_path):
            # Look for Chart.yaml files
            if 'Chart.yaml' in files:
                chart_dir = os.path.relpath(root, self.repo_path)
                chart_info = {
                    "path": chart_dir,
                    "files": [],
                    "has_values": False,
                    "has_templates": False
                }
                
                # Check for related files
                for file in files:
                    if file in ['values.yaml', 'values.yml']:
                        chart_info["has_values"] = True
                    elif file in ['Chart.yaml', 'Chart.yml']:
                        chart_info["files"].append(file)
                
                # Check for templates directory
                templates_dir = os.path.join(root, 'templates')
                if os.path.exists(templates_dir):
                    chart_info["has_templates"] = True
                    chart_info["files"].extend(os.listdir(templates_dir))
                
                helm_charts.append(chart_info)
        
        return helm_charts

    def _detect_dockerfiles(self) -> List[Dict[str, Any]]:
        """Detect Dockerfiles and Docker-related files"""
        dockerfiles = []
        
        docker_patterns = [
            'Dockerfile',
            'Dockerfile.*',
            'docker-compose.yml',
            'docker-compose.yaml',
            '.dockerignore'
        ]
        
        for root, dirs, files in os.walk(self.repo_path):
            for file in files:
                if any(file.startswith(pattern.replace('*', '')) for pattern in docker_patterns):
                    rel_path = os.path.relpath(os.path.join(root, file), self.repo_path)
                    dockerfiles.append({
                        "file": rel_path,
                        "type": "Dockerfile" if file.startswith("Dockerfile") else file,
                        "content_preview": self._get_file_preview(os.path.join(root, file))
                    })
        
        return dockerfiles

    def _detect_gitops_tools(self) -> List[Dict[str, Any]]:
        """Detect GitOps tools and configurations"""
        gitops_tools = []
        
        # Look for ArgoCD Application manifests
        for root, dirs, files in os.walk(self.repo_path):
            for file in files:
                if file.endswith('.yml') or file.endswith('.yaml'):
                    file_path = os.path.join(root, file)
                    content = self._get_file_preview(file_path)
                    
                    if 'kind: Application' in content and 'argoproj.io' in content:
                        gitops_tools.append({
                            "name": "argocd",
                            "file": os.path.relpath(file_path, self.repo_path),
                            "type": "Application"
                        })
                    elif 'kind: Flux' in content or 'fluxcd.io' in content:
                        gitops_tools.append({
                            "name": "flux",
                            "file": os.path.relpath(file_path, self.repo_path),
                            "type": "Flux"
                        })
                    elif 'kind: Tekton' in content or 'tekton.dev' in content:
                        gitops_tools.append({
                            "name": "tekton",
                            "file": os.path.relpath(file_path, self.repo_path),
                            "type": "Pipeline"
                        })
        
        return gitops_tools

    def _detect_architecture_patterns(self) -> List[Dict[str, Any]]:
        """Detect architecture patterns in the codebase"""
        patterns = []
        
        # Look for common architecture indicators
        for root, dirs, files in os.walk(self.repo_path):
            # Check directory structure for patterns
            dir_names = [d.lower() for d in dirs]
            
            if any('service' in d for d in dir_names):
                patterns.append({
                    "type": "microservice",
                    "confidence": "high",
                    "evidence": f"Found service directories: {[d for d in dirs if 'service' in d.lower()]}"
                })
            
            if any('api' in d for d in dir_names):
                patterns.append({
                    "type": "api-gateway",
                    "confidence": "medium",
                    "evidence": f"Found API directories: {[d for d in dirs if 'api' in d.lower()]}"
                })
            
            if any('gateway' in d for d in dir_names):
                patterns.append({
                    "type": "api-gateway",
                    "confidence": "high",
                    "evidence": f"Found gateway directories: {[d for d in dirs if 'gateway' in d.lower()]}"
                })
            
            # Check for health check endpoints
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.java', '.go')):
                    file_path = os.path.join(root, file)
                    content = self._get_file_preview(file_path)
                    
                    if '/health' in content or '/healthz' in content:
                        patterns.append({
                            "type": "health-check",
                            "confidence": "high",
                            "evidence": f"Health check endpoint found in {os.path.relpath(file_path, self.repo_path)}"
                        })
                        break
        
        return patterns

    def _detect_security_issues(self) -> List[Dict[str, Any]]:
        """Detect potential security issues"""
        security_issues = []
        
        # Look for hardcoded secrets
        secret_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
            r'private_key\s*=\s*["\'][^"\']+["\']'
        ]
        
        for root, dirs, files in os.walk(self.repo_path):
            # Skip certain directories
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__']]
            
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.java', '.go', '.yml', '.yaml', '.json')):
                    file_path = os.path.join(root, file)
                    content = self._get_file_preview(file_path)
                    
                    for pattern in secret_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            security_issues.append({
                                "type": "hardcoded_secret",
                                "severity": "high",
                                "file": os.path.relpath(file_path, self.repo_path),
                                "description": "Potential hardcoded secret found"
                            })
                            break
        
        return security_issues

    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        # This would be enhanced based on the actual analysis results
        recommendations.extend([
            "Consider implementing GitOps practices with ArgoCD or Flux",
            "Add comprehensive CI/CD pipeline with security scanning",
            "Implement proper secrets management",
            "Add health checks and monitoring",
            "Consider breaking down into microservices if monolithic",
            "Implement proper RBAC and access controls"
        ])
        
        return recommendations

    def _get_file_preview(self, file_path: str, max_lines: int = 50) -> str:
        """Get a preview of file content"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()[:max_lines]
                return ''.join(lines)
        except Exception:
            return "" 