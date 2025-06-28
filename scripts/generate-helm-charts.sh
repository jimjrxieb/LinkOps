#!/bin/bash

# Generate Helm charts for all LinkOps-MLOps services
# This script creates a complete Helm chart structure for each service

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# List of services
SERVICES=("whis" "james" "katie" "igris" "auditguard" "sanitizer" "scraperdash" "data_collector" "ficknury")

# Function to create Helm chart for a service
create_helm_chart() {
    local service=$1
    local chart_dir="helm/$service"
    
    print_status "Creating Helm chart for $service..."
    
    # Create directory structure
    mkdir -p "$chart_dir/templates"
    
    # Create Chart.yaml
    cat > "$chart_dir/Chart.yaml" << EOF
apiVersion: v2
name: $service
description: A Helm chart for the $service service
type: application
version: 0.1.0
appVersion: "1.0.0"
keywords:
  - mlops
  - ai
  - microservice
home: https://github.com/your-org/LinkOps-MLOps
sources:
  - https://github.com/your-org/LinkOps-MLOps
maintainers:
  - name: LinkOps Team
    email: team@linkops.com
EOF

    # Create values.yaml
    cat > "$chart_dir/values.yaml" << EOF
# Default values for $service service
replicaCount: 1

image:
  repository: ghcr.io/your-org/LinkOps-MLOps-$service
  tag: latest
  pullPolicy: IfNotPresent

imagePullSecrets: []
nameOverride: ""
fullnameOverride: ""

serviceAccount:
  create: true
  annotations: {}
  name: ""

podAnnotations: {}

podSecurityContext: {}

securityContext: {}

service:
  type: ClusterIP
  port: 80
  targetPort: 8000

ingress:
  enabled: false
  className: ""
  annotations: {}
  hosts:
    - host: $service.local
      paths:
        - path: /
          pathType: ImplementationSpecific
  tls: []

resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 100
  targetCPUUtilizationPercentage: 80
  targetMemoryUtilizationPercentage: 80

nodeSelector: {}

tolerations: []

affinity: {}

# Environment variables
env:
  - name: ENVIRONMENT
    value: "production"
  - name: LOG_LEVEL
    value: "INFO"

# ConfigMap and Secret references
configMap:
  enabled: false
  name: ""

secret:
  enabled: false
  name: ""

# Health check configuration
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
EOF

    # Create deployment.yaml
    cat > "$chart_dir/templates/deployment.yaml" << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "SERVICE.fullname" . }}
  labels:
    {{- include "SERVICE.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "SERVICE.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      labels:
        {{- include "SERVICE.selectorLabels" . | nindent 8 }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "SERVICE.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
        - name: {{ .Chart.Name }}
          securityContext:
            {{- toYaml .Values.securityContext | nindent 12 }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          {{- if .Values.env }}
          env:
            {{- range .Values.env }}
            - name: {{ .name }}
              value: {{ .value | quote }}
            {{- end }}
          {{- end }}
          {{- if .Values.configMap.enabled }}
          envFrom:
            - configMapRef:
                name: {{ .Values.configMap.name }}
          {{- end }}
          {{- if .Values.secret.enabled }}
          envFrom:
            - secretRef:
                name: {{ .Values.secret.name }}
          {{- end }}
          ports:
            - name: http
              containerPort: {{ .Values.service.targetPort }}
              protocol: TCP
          {{- if .Values.livenessProbe }}
          livenessProbe:
            {{- toYaml .Values.livenessProbe | nindent 12 }}
          {{- end }}
          {{- if .Values.readinessProbe }}
          readinessProbe:
            {{- toYaml .Values.readinessProbe | nindent 12 }}
          {{- end }}
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
{{- if .Values.autoscaling.enabled }}
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{ include "SERVICE.fullname" . }}
  labels:
    {{- include "SERVICE.labels" . | nindent 4 }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ include "SERVICE.fullname" . }}
  minReplicas: {{ .Values.autoscaling.minReplicas }}
  maxReplicas: {{ .Values.autoscaling.maxReplicas }}
  metrics:
    {{- if .Values.autoscaling.targetCPUUtilizationPercentage }}
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: {{ .Values.autoscaling.targetCPUUtilizationPercentage }}
    {{- end }}
    {{- if .Values.autoscaling.targetMemoryUtilizationPercentage }}
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: {{ .Values.autoscaling.targetMemoryUtilizationPercentage }}
    {{- end }}
{{- end }}
EOF

    # Create service.yaml
    cat > "$chart_dir/templates/service.yaml" << 'EOF'
apiVersion: v1
kind: Service
metadata:
  name: {{ include "SERVICE.fullname" . }}
  labels:
    {{- include "SERVICE.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: {{ .Values.service.targetPort }}
      protocol: TCP
      name: http
  selector:
    {{- include "SERVICE.selectorLabels" . | nindent 4 }}
EOF

    # Create serviceaccount.yaml
    cat > "$chart_dir/templates/serviceaccount.yaml" << 'EOF'
{{- if .Values.serviceAccount.create -}}
apiVersion: v1
kind: ServiceAccount
metadata:
  name: {{ include "SERVICE.serviceAccountName" . }}
  labels:
    {{- include "SERVICE.labels" . | nindent 4 }}
  {{- with .Values.serviceAccount.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
{{- end }}
EOF

    # Create ingress.yaml
    cat > "$chart_dir/templates/ingress.yaml" << 'EOF'
{{- if .Values.ingress.enabled -}}
{{- $fullName := include "SERVICE.fullname" . -}}
{{- $svcPort := .Values.service.port -}}
{{- if and .Values.ingress.className (not (hasKey .Values.ingress.annotations "kubernetes.io/ingress.class")) }}
  {{- $_ := set .Values.ingress.annotations "kubernetes.io/ingress.class" .Values.ingress.className}}
{{- end }}
{{- if semverCompare ">=1.19-0" .Capabilities.KubeVersion.GitVersion -}}
apiVersion: networking.k8s.io/v1
{{- else if semverCompare ">=1.14-0" .Capabilities.KubeVersion.GitVersion -}}
apiVersion: networking.k8s.io/v1beta1
{{- else -}}
apiVersion: extensions/v1beta1
{{- end }}
kind: Ingress
metadata:
  name: {{ $fullName }}
  labels:
    {{- include "SERVICE.labels" . | nindent 4 }}
  {{- with .Values.ingress.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  {{- if and .Values.ingress.className (semverCompare ">=1.18-0" .Capabilities.KubeVersion.GitVersion) }}
  ingressClassName: {{ .Values.ingress.className }}
  {{- end }}
  {{- if .Values.ingress.tls }}
  tls:
    {{- range .Values.ingress.tls }}
    - hosts:
        {{- range .hosts }}
        - {{ . | quote }}
        {{- end }}
      secretName: {{ .secretName }}
    {{- end }}
  {{- end }}
  rules:
    {{- range .Values.ingress.hosts }}
    - host: {{ .host | quote }}
      http:
        paths:
          {{- range .paths }}
          - path: {{ .path }}
            {{- if and .pathType (semverCompare ">=1.18-0" $.Capabilities.KubeVersion.GitVersion) }}
            pathType: {{ .pathType }}
            {{- end }}
            backend:
              {{- if semverCompare ">=1.19-0" $.Capabilities.KubeVersion.GitVersion }}
              service:
                name: {{ $fullName }}
                port:
                  number: {{ $svcPort }}
              {{- else }}
              serviceName: {{ $fullName }}
              servicePort: {{ $svcPort }}
              {{- end }}
          {{- end }}
    {{- end }}
{{- end }}
EOF

    # Create _helpers.tpl
    cat > "$chart_dir/templates/_helpers.tpl" << 'EOF'
{{/*
Expand the name of the chart.
*/}}
{{- define "SERVICE.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "SERVICE.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "SERVICE.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "SERVICE.labels" -}}
helm.sh/chart: {{ include "SERVICE.chart" . }}
{{ include "SERVICE.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "SERVICE.selectorLabels" -}}
app.kubernetes.io/name: {{ include "SERVICE.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "SERVICE.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "SERVICE.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
EOF

    # Replace SERVICE placeholder with actual service name in all template files
    find "$chart_dir/templates" -name "*.yaml" -o -name "*.tpl" | xargs sed -i "s/SERVICE/$service/g"
    
    print_success "Helm chart created for $service"
}

# Main execution
print_status "Starting Helm chart generation for LinkOps-MLOps services..."

# Create helm directory if it doesn't exist
mkdir -p helm

# Generate charts for all services
for service in "${SERVICES[@]}"; do
    create_helm_chart "$service"
done

print_success "All Helm charts generated successfully!"
print_status "Generated charts:"
for service in "${SERVICES[@]}"; do
    echo "  - helm/$service/"
done

print_status "Next steps:"
echo "  1. Review and customize the generated charts"
echo "  2. Update image repositories in values.yaml files"
echo "  3. Configure environment-specific values"
echo "  4. Test deployment with: helm install test-release ./helm/whis" 